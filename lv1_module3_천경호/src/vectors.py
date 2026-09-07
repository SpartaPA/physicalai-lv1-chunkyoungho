"""문제 1 — 벡터 연산 모듈. (학생 작성용 템플릿)

내적 · 사이각 · 정규화 · 정사영 · 반대칭행렬(외적) · 평면 법선과
가우스 소거 기반의 rank / 행렬식 / 역행렬을 **직접** 구현한다.

규칙
----
- `np.linalg` 는 노트북에서 **검산용으로만** 쓰고, 이 모듈 안에서는 쓰지 않는다.
  (`inverse_gauss_jordan` 이 던지는 `np.linalg.LinAlgError` 예외 타입만 예외)
- 각 함수의 docstring 에 적힌 계약(입력/출력/예외)을 그대로 지킨다.
  노트북의 검증 셀과 `tests/` 가 이 계약을 기준으로 채점된다.
- 구현을 마치면 `raise NotImplementedError(...)` 줄을 지운다.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "as_vector",
    "dot",
    "norm",
    "angle_between",
    "normalize",
    "project",
    "reject",
    "skew",
    "cross",
    "plane_normal",
    "row_echelon",
    "rank",
    "det",
    "gauss_eliminate",
    "inverse_gauss_jordan",
]


# ---------------------------------------------------------------- 기본 연산

def as_vector(v) -> np.ndarray:
    """입력(리스트/튜플/배열)을 1차원 float 배열로 변환한다.

    1차원이 아니면 ValueError 를 던진다.

    [구현 예시] 아래 세 줄이 이 파일에서 기대하는 코드 스타일이다.
    나머지 함수도 이런 식으로 채워 넣으면 된다.
    """
    arr = np.asarray(v, dtype=float)
    if arr.ndim != 1:
        raise ValueError("1차원 벡터가 필요합니다. 받은 shape=", arr.shape)
    return arr


def dot(a, b) -> float:
    """내적. sum(a_i * b_i) 를 직접 계산한다 (`np.dot` 사용 금지).

    두 벡터의 차원이 다르면 ValueError.
    """
    a, b = as_vector(a), as_vector(b)
    if a.shape != b.shape:
        raise ValueError(f"반드시 동일한 크기를 가진 배열일 것! {a.shape} vs {b.shape} ")
    return float(np.sum(a * b))


def norm(v) -> float:
    """유클리드 노름. sqrt(v·v) — 위에서 만든 dot 을 재사용한다."""
    # TODO: 문제 1-1
    return np.sqrt(dot(v, v))


def angle_between(a, b, degrees: bool = True) -> float:
    """두 벡터 사이각. degrees=True 면 도(°), False 면 라디안.

    cos(theta) = (a·b) / (|a||b|)

    주의 1. 영벡터가 들어오면 사이각이 정의되지 않는다 -> ValueError.
    주의 2. 부동소수점 오차로 |cos| 가 1 을 아주 조금 넘으면 arccos 가 nan 을 낸다.
            [-1, 1] 로 clip 해야 무작위 입력에서도 안전하다.
    """
    # TODO: 문제 1-1
    dot_product = dot(a, b)
    norm_a = norm(a)
    norm_b = norm(b)
    cos_theta = dot_product / (norm_a * norm_b)
    theta = np.arccos(cos_theta) 
    theta = np.degrees(theta) if degrees else theta
    return theta


def normalize(v, eps: float = 1e-12) -> np.ndarray:
    """단위벡터로 정규화한다. v / |v|

    영벡터를 어떻게 처리할지는 **문제 1-2 에서 직접 정한다.**
    노트북 1-2 에서 (1) 아무 처리 없이 나눴을 때 무슨 일이 나는지 관찰하고,
    (2) 선택한 처리 방식과 근거를 마크다운에 적은 뒤, 그 방식대로 여기에 구현한다.
    선택에 따라 노트북/테스트의 검증 코드도 그 방식에 맞춰 작성한다.
    """
    # TODO: 문제 1-2
    a = as_vector(v)
    norm_a = norm(a)
    if(norm_a<eps):
        raise ValueError("0벡터는 정규화 할 수 없습니다.")
    return a / norm_a


def project(a, b) -> np.ndarray:
    """a 를 b 방향으로 정사영한 성분.

        proj_b(a) = (a·b / b·b) * b

    분모가 |b|^2 이므로 b 를 미리 정규화할 필요는 없다.
    b 가 영벡터면 ValueError.
    """
    # TODO: 문제 1-3
    a,b = as_vector(a), as_vector(b)
    return (dot(a,b) / dot(b,b))*b


def reject(a, b) -> np.ndarray:
    """a 에서 b 방향 성분을 뺀 나머지(수직 성분). a = project + reject 가 성립해야 한다."""
    # TODO: 문제 1-3
    a,b = as_vector(a), as_vector(b)
    return a-project(a,b)


def skew(a) -> np.ndarray:
    """3차원 벡터 a 에 대응하는 반대칭행렬 [a]_x 를 만든다.

        [a]_x = [[  0, -a3,  a2],
                 [ a3,   0, -a1],
                 [-a2,  a1,   0]]

    만족해야 하는 성질: [a]_x @ b == a x b,  [a]_x.T == -[a]_x
    3차원이 아니면 ValueError.
    """
    # TODO: 문제 1-4
    a = as_vector(a)
    if len(a) != 3:
        raise ValueError ("3X3") # 3차원인 경우에 한하여 반대칭 행렬
    return np.array([
        [0,-a[2],a[1]],
        [a[2],0,-a[0]],
        [-a[1],a[0],0]
    ])


def cross(a, b) -> np.ndarray:
    """외적을 **반대칭행렬 곱으로** 계산한다 (`np.cross` 사용 금지)."""
    # TODO: 문제 1-4
    a_skew = skew(a)
    b=as_vector(b)
    return a_skew@b  # 반대칭 행렬 곱 리턴


def plane_normal(P1, P2, P3) -> np.ndarray:
    """세 점이 이루는 평면의 **단위** 법선 벡터.

    두 모서리 벡터(P2-P1, P3-P1)의 외적이 평면에 수직이다.
    세 점이 일직선이면 외적이 영벡터가 되어 평면이 하나로 정해지지 않는다 -> ValueError.
    """
    # TODO: 문제 1-5
    P1, P2, P3 = as_vector(P1), as_vector(P2), as_vector(P3)
    u=P2-P1
    v=P3-P1
    pn= cross(u,v)    
    if np.allclose(pn, 0, atol=1e-12):           # 부동소수점을 감안한 영벡터 검출
        raise ValueError("세 점이 일직선상에 있습니다.")
    pn=normalize(pn)    
    return pn


# ------------------------------------------------- 가우스 소거 기반 선형대수

def row_echelon(A, pivoting: bool = True):
    """행 사다리꼴(row echelon form) 로 만든다.

    Parameters
    ----------
    pivoting : True 면 부분 피벗팅(각 열에서 절댓값이 가장 큰 행을 피벗으로 올림)

    Returns
    -------
    U : (m, n) 상삼각 형태 행렬
    pivot_cols : 피벗이 선 열 인덱스 리스트
    n_swaps : 행 교환 횟수 (행렬식 부호 계산에 필요)

    힌트: 0 인지 판정할 때는 `== 0` 대신 허용오차(tol)를 쓴다.
          예) tol = max(m, n) * np.finfo(float).eps * max(1.0, np.max(np.abs(U)))
    """
    # TODO: 문제 1-6 / 문제 4
    tol = 1e-12
    a = np.asarray(A).astype(float, copy=True)
    m, n = a.shape
    n_swaps = 0
    pivot_cols: list[int] = []
    r = 0; # 현재 처리하는 행 인덱스
    for c in range(n):
        if c>=n: break #마지막 열까지 왔다면 멈춤
        if r>=m: break #마지막 행까지 왔다면 멈춤
        #피벗 찾기
        candidate_row = r + np.argmax(np.abs(a[r:,c]))
        if np.abs(a[candidate_row,c])<tol: # 피벗이 0에 가까우면 이번 열은 스킵
            continue
        
        #스왑
        if pivoting:
            if candidate_row != r:
                a[[r,candidate_row]]=a[[candidate_row,r]]
                n_swaps+=1            
        
        pivot_cols.append(c) #피벗 열 기록
        
        # 전방소거 - current_row 아래의 모든 행에서 col 열의 원소를 0으로 만들기
        for j in range(r + 1, m):
            if np.abs(a[j, c]) > tol:
                factor = a[j, c] / a[r, c]
                a[j, c:] -= factor * a[r, c:]
                a[j,c] = 0.0 # 부동소수점 오차 삭제

        r += 1 # 소거 완료 후 다음 행으로 이동
    
    return a, pivot_cols, n_swaps


def rank(A) -> int:
    """행 사다리꼴의 피벗 개수 = rank."""
    # TODO: 문제 1-6
    a, pivot_cols, n_swaps = row_echelon(A)
    return len(pivot_cols)


def det(A) -> float:
    """행렬식 = 행 사다리꼴 대각성분의 곱 x (-1)^(행 교환 횟수).

    피벗이 n 개보다 적으면(특이행렬) 0.0 을 돌려준다.
    정사각 행렬이 아니면 ValueError.
    """
    # TODO: 문제 1-6
    a = np.asarray(A)
    if a.ndim != 2:
        raise ValueError(f"2차원 행렬이 필요합니다. 받은 shape={a.shape}")
    m, n = a.shape
    if m != n:
        raise ValueError(f"정사각 행렬이 필요합니다. 받은 shape={a.shape}")
    
    # 행 사다리꼴로 변환
    u, pivot_cols, n_swaps = row_echelon(a)
    
    # 피벗의 개수가 n보다 적으면 특이행렬
    if len(pivot_cols) < n:
        return 0.0
    
    # 대각 성분의 곱
    det_value = 1.0
    for i in range(n):
        det_value *= u[i, i]
    
    # 행 교환 횟수에 따른 부호 조정: (-1)^n_swaps
    if n_swaps % 2 == 1:
        det_value *= -1
    
    return det_value


def gauss_eliminate(A, b, pivoting: bool = True, verbose: bool = False):
    """가우스 소거법 + 후진대입으로 Ax = b 를 푼다.

    Parameters
    ----------
    pivoting : True 면 부분 피벗팅을 적용한다. False 면 피벗을 그대로 쓴다
               (문제 4-4 에서 두 경우의 오차를 비교하므로 **둘 다 동작해야 한다**).
    verbose  : True 면 각 소거 단계의 첨가행렬 [A|b] 를 출력한다
               (문제 4-1 이 요구하는 '단계별 출력').

    Returns
    -------
    x : 해 벡터
    steps : 단계별 첨가행렬 [A|b] 스냅샷 리스트 (초기 상태 포함)

    피벗이 0 이면 해가 유일하지 않다 -> ZeroDivisionError.
    """
    # TODO: 문제 4-1
    A=np.asarray(A)
    b=np.asarray(b)
    
    if A.ndim != 2 or b.ndim != 1:
        raise ValueError("A는 2D, b는 1D 배열이어야 함")
    if A.shape[0] != b.shape[0]:
        raise ValueError("A의 행 수와 b의 길이가 맞지 않음")

    # [A|b] 확대 행렬 생성
    b=b[:,np.newaxis]
    agumented = np.hstack((A,b))

    
    # 전방소거 (row_echelon)
    tol = 1e-12
    a = agumented.astype(float, copy=True)
    m, n = a.shape
    n_swaps = 0
    steps = []
    if verbose:
        steps = a[np.newaxis,:,:]
        print(f"[초기] 첨가행렬 [A|b]\n{a}")

    r = 0
    for c in range(n):
        if c>=n: break #마지막 열까지 왔다면 멈춤
        if r>=m: break
        #피벗 찾기
        candidate_row = r + np.argmax(np.abs(a[r:,c]))
        if np.abs(a[candidate_row,c])<tol: # 피벗이 0에 가까우면 이번 열은 스킵
            continue
        
        #스왑
        if pivoting:
            if candidate_row != r:
                a[[r,candidate_row]]=a[[candidate_row,r]]
                n_swaps+=1
            
        # 전방소거 - current_row 아래의 모든 행에서 col 열의 원소를 0으로 만들기
        for j in range(r + 1, m):
            if np.abs(a[j, c]) > tol:
                factor = a[j, c] / a[r, c]
                a[j, c:] -= factor * a[r, c:]
                a[j,c] = 0.0 #부동소수점 오차 삭제
        r+=1 #소거 완료 후 다음 행으로 이동

        if verbose:
            steps = np.concatenate((steps,a[np.newaxis,:,:]), axis=0)
            print(f"[{c+1}단계]\n{a}")

 
    rank_A=rank(A)
    rank_agumented=rank(agumented)

    if rank_agumented > rank_A:
        raise ValueError("모순된 행렬")        
    if rank_agumented < n - 1:
        raise ValueError("무한 해")
    """
    후진대입
    """
    x=np.zeros(n-1)
    for c in reversed(range(m)):
        if(a[c]<=tol).sum() == n: #모두 0인 행 거르기
            continue
        x[c] = a[c,n-1]
        for j in reversed(range(c,n-1)):
            if c==j:
                x[c] = x[c] / a[c,j]
                continue
            else:
                x[c] = x[c] - (a[c,j] * x[j])
    return x, steps


def inverse_gauss_jordan(A) -> np.ndarray:
    """가우스-조던 소거로 역행렬을 구한다. [A|I] -> [I|A^-1].

    정사각이 아니면 ValueError, 특이행렬이면 np.linalg.LinAlgError.
    (`np.linalg.inv` 를 부르지 말고 소거로 직접 구한다)
    """
    # TODO: 문제 4-3
    A=np.asarray(A,dtype=float,copy=True)
    m,n = A.shape
    if m != n:
        raise ValueError("정사각 행렬이 아님")
    argumented = np.hstack([A,np.eye(m)])

    for i in range(n):
        candidate_row = i + np.argmax(np.abs(argumented[i:,i]))

        if np.abs(argumented[candidate_row,i]) < 1e-12:
            raise np.linalg.LinAlgError("특이행렬")

        if candidate_row != i:
            argumented[[i, candidate_row]] = argumented[[candidate_row,i]]

        # 피벗을 1로 만들기
        pivot = argumented[i,i]
        argumented[i] /= pivot

         # 현재 피벗이 있는 행으로 나머지 행을 0으로 소거
        for j in range(n):
            if i!=j:
                factor = argumented[j,i]
                argumented[j] -= factor * argumented[i]
    
    return argumented[:,n:]