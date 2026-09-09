"""문제 5 — 4x4 동차변환 모듈. (학생 작성용 템플릿)

동차변환 생성/역변환, 점과 방향의 구분, 벡터화된 점군 변환,
정규방정식 기반 최소자승법을 직접 구현한다.
"""

from __future__ import annotations

import numpy as np

from .vectors import inverse_gauss_jordan

__all__ = [
    "make_T",
    "inv_T",
    "inv_T_batch",
    "to_homogeneous",
    "transform_point",
    "transform_direction",
    "transform_points",
    "least_squares_normal_equation",
    "rmse",
]


def make_T(R, t) -> np.ndarray:
    """회전 R(3x3)과 병진 t(3,)로 4x4 동차변환을 만든다.

        T = [[R, t],
             [0, 1]]

    R 이 3x3 이 아니면 ValueError.
    """
    # TODO: 문제 5-1
    R=np.asarray(R)
    m,n=R.shape    
    if m != 3 and n != 3:
        raise ValueError("회전은 3X3 행렬이어야 함.")
    t=np.asarray(t)    
    if t.ndim != 1 or len(t)!=3:
        raise ValueError("병진의 크기가 잘못 됨")

    T=np.hstack([R,t.reshape(-1,1)])
    T=np.vstack([T,[0,0,0,1]])
    return T


def inv_T(T) -> np.ndarray:
    """동차변환의 역변환. **일반 역행렬 함수를 쓰지 않고** 공식으로 구한다.

        T^-1 = [[R^T, -R^T t],
                [  0,      1]]

    유도: T^-1 을 [[S, u], [0, 1]] 로 두고 T T^-1 = I 를 풀면
          R S = I -> S = R^T (R 이 직교),  R u + t = 0 -> u = -R^T t.

    4x4 가 아니면 ValueError.
    """
    # TODO: 문제 5-1
    T = np.asarray(T)
    m,n = T.shape
    if m!=4 and n!=4:
        raise ValueError("T는 4 X 4 행렬이어야 함.")
    R=T[0:3,0:3]
    t=T[0:3,3]    
    S=R.T
    u=-R.T@t
    invT=np.hstack([S,u.reshape(-1,1)])
    invT=np.vstack([invT,[0,0,0,1]])
    return invT



def inv_T_batch(Ts) -> np.ndarray:
    """(N, 4, 4) 동차변환 묶음을 **반복문 없이** 한 번에 역변환한다.

    `inv_T` 와 같은 공식을 배치 축으로 확장한 것이다.
    문제 5-4 의 속도 비교에서 쓴다 — 단건 호출은 파이썬/NumPy 호출 오버헤드가
    지배해서 연산량 차이가 드러나지 않기 때문이다.

    힌트: 전치는 `np.swapaxes(..., 1, 2)`, 배치 행렬-벡터 곱은
          `np.einsum("nij,nj->ni", ...)` 로 쓸 수 있다.
    """
    # TODO: 문제 5-4
    Ts= np.asarray(Ts)
    l,m,n = Ts.shape
    if m!=4 and n!=4:
        raise ValueError("T는 4 X 4 행렬이어야 함.")
    # 역행렬을 담을 빈 배열 생성
    inv_T = np.zeros_like(Ts)
    inv_T[:,3,3]=1.0
    # 회전 행렬 파트 (N,3,3)추출 후 전치
    R_T = np.swapaxes(Ts[:,:3,:3],1,2)
    inv_T[:,:3,:3] = R_T


    t=Ts[:,:3,3]
    inv_t = -np.einsum('nij,nj->ni',R_T,t)
    inv_T[:,:3,3] = inv_t

    return inv_T
    


def to_homogeneous(P, w: float = 1.0) -> np.ndarray:
    """(3,) 또는 (N,3) 좌표에 마지막 성분 w 를 붙인다.

    w = 1 이면 점(위치), w = 0 이면 방향(벡터).
    """
    # TODO: 문제 5-2
    P=np.asarray(P,dtype=float,copy=True)    
    i:int=0
    if P.ndim == 1:
        i=1
        m=len(P)
        if m!=3:
            raise ValueError("3차원상의 좌표만 허용합니다.")
    else:
        m,n=P.shape
        i=m
        if n!=3:
            raise ValueError("3차원상의 좌표만 허용합니다.")
    if not(w == 1.0 or w == 0.0):
        raise ValueError("w는 1.0 혹은 0.0 만 허용합니다.")
    ws=np.full(shape=(i,), fill_value=w)
    if P.ndim ==1:
        P=np.hstack([P,ws])
    else:
        P=np.hstack([P,ws.reshape(-1,1)])    
    return P
    


def transform_point(T, p) -> np.ndarray:
    """점 변환 (w = 1): 회전과 병진이 모두 적용된다. 반환은 (3,)."""
    # TODO: 문제 5-2
    T = np.asarray(T)
    m,n = T.shape
    if m!=4 and n!=4:
        raise ValueError("T는 4 X 4 행렬이어야 함.")
    # 위치는 뒤에 1을 붙인다.
    p_h=to_homogeneous(p,1.0)    
    Tp = T@p_h
    return Tp[0:3]



def transform_direction(T, v) -> np.ndarray:
    """방향 변환 (w = 0): 회전만 적용되고 병진은 무시된다. 반환은 (3,)."""
    # TODO: 문제 5-2
    T = np.asarray(T)
    m,n = T.shape
    if m!=4 and n!=4:
        raise ValueError("T는 4 X 4 행렬이어야 함.")
    # 방향는 뒤에 0을 붙인다.
    v_h=to_homogeneous(v,0.0)
    Tv = T@v_h
    
    return Tv[0:3]


def transform_points(T, P, w: float = 1.0) -> np.ndarray:
    """(N,3) 점군을 **반복문 없이** 한 번에 변환한다. (3,) 입력도 받아야 한다.

    힌트: (T @ P_h.T).T 대신 P_h @ T.T 를 쓰면 전치가 한 번으로 끝나고
          메모리 접근도 행 방향이라 캐시에 유리하다.
    """
    # TODO: 문제 5-2 / 6-2
    T=np.asarray(T)
    m,n = T.shape
    if m!=4 and n!=4:
        raise ValueError("T는 4 X 4 행렬이어야 함.")
    P_h=to_homogeneous(P,w)
    TP = P_h @ T.T
    is_1d = (P.ndim==1)
    if is_1d:
        return TP[0:3]
    else:
        return TP[:,0:3]


def least_squares_normal_equation(A, b):
    """정규방정식 (A^T A) x = A^T b 를 직접 세워 최소자승해를 구한다.

    - (A^T A) 의 역행렬은 문제 4 에서 만든 `inverse_gauss_jordan` 으로 구한다
      (`np.linalg.lstsq` 는 노트북에서 **비교 대상**으로만 쓴다).
    - 근거: 잔차 r = b - A x 가 최소일 때 r 은 A 의 열공간에 수직이므로 A^T r = 0.

    Returns
    -------
    x : 최소자승해
    residual : b - A x
    """
    # TODO: 문제 5-5    
    
    A, b = np.asarray(A), np.asarray(b)

    if A.ndim==2:
        AtA = np.einsum('ji,jk->ik',A,A)
        Atb = np.einsum('ji,j->i',A,b)
        inv_AtA = inverse_gauss_jordan(AtA)
        # x 계산
        x=np.einsum('ij,j->i', inv_AtA, Atb)
        Ax=np.einsum('ij,j->i',A,x)
        residual = b-Ax
        return x , residual
    elif A.ndim==3:
        AtA = np.einsum('nji,njk->nik',A,A)
        Atb = np.einsum('nji,nj->ni',A,b)
        # 배치 차원 만큼 반복문 돌기
        num_batches = AtA.shape[0]
        # 결과를 담을 배열
        inv_AtA = np.zeros_like(AtA)
        for n in range(num_batches):
            # AtA[n]은 (K,K) 크기의 단일 행렬이므로 기존 함수 사용 가능
            inv_AtA = inverse_gauss_jordan(AtA[n])
        # x 계산
        x=np.einsum('nij,nj->ni',inv_AtA, Atb)
        Ax = np.einsum('nij,nj->ni',A,x)
        residual = b-Ax
        return x, residual
    else:
        raise ValueError("A행렬 배열 차원 오류")

def rmse(residual) -> float:
    """잔차의 RMSE = sqrt(mean(r^2))."""
    # TODO: 문제 5-5
    r=np.asarray(residual)
    return np.sqrt(np.mean(r*r))
