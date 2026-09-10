"""문제 4 — 궤적 보간. (학생 작성용 템플릿)

경유점(waypoint)을 지나는 궤적을 선형 보간 / 큐빅 스플라인으로 만들고,
시작·끝에서 속도와 가속도가 0 이 되는 5차 다항식 프로파일을 구현한다.

입력 규약
--------
- t_wp : (M,) 경유점 시각, 오름차순
- q_wp : (M,) 스칼라 궤적 또는 (M, D) 다차원 궤적 (예: 3차원 위치는 D = 3)
- t    : (N,) 평가할 시각 (t_wp[0] <= t <= t_wp[-1])
- 반환 : q_wp 가 (M,) 이면 (N,), (M, D) 이면 (N, D)

큐빅 스플라인은 `scipy.interpolate.CubicSpline` 을 써도 된다 (axis=0).
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline

__all__ = ["linear_interp", "cubic_spline_interp", "quintic_profile", "finite_diff"]


def linear_interp(t_wp, q_wp, t) -> np.ndarray:
    """경유점 사이를 직선으로 잇는 보간. 각 차원마다 `np.interp` 를 쓰면 된다.

    위치는 이어지지만 경유점에서 속도가 불연속(꺾임)이다.
    """
    # TODO: 문제 4-1
    t_wp = np.asarray(t_wp, dtype=float)
    q_wp = np.asarray(q_wp, dtype=float)
    t = np.asarray(t, dtype=float)

    if q_wp.ndim == 1:
        return np.interp(t, t_wp, q_wp)

    # (M, D) 입력인 경우 차원(D)별로 np.interp 수행
    N = len(t)
    D = q_wp.shape[1]
    q_interp = np.empty((N, D), dtype=float)

    for d in range(D):
        q_interp[:, d] = np.interp(t, t_wp, q_wp[:, d])

    return q_interp


def cubic_spline_interp(t_wp, q_wp, t, bc_type: str = "natural") -> np.ndarray:
    """경유점을 지나는 큐빅 스플라인 보간 (위치·속도·가속도가 모두 연속, C2).

    bc_type : 양끝 경계 조건. "natural" (양끝 가속도 0) 또는 "clamped" (양끝 속도 0).
    """
    # TODO: 문제 4-1
    t_wp = np.asarray(t_wp, dtype=float)
    q_wp = np.asarray(q_wp, dtype=float)
    t = np.asarray(t, dtype=float)

    # bc_type 변환 처리 ("clamped" -> ((1, 0.0), (1, 0.0)))
    if bc_type == "clamped":
        bc = ((1, 0.0), (1, 0.0))
    else:
        bc = bc_type

    cs = CubicSpline(t_wp, q_wp, axis=0, bc_type=bc)
    return cs(t)


def quintic_profile(t, t0: float, tf: float, q0, qf,
                    v0=0.0, vf=0.0, a0=0.0, af=0.0):
    """5차 다항식 궤적 q(t) 와 그 도함수 (q, qd, qdd) 를 돌려준다.

    경계 조건 6개 — q(t0)=q0, q(tf)=qf, qd(t0)=v0, qd(tf)=vf, qdd(t0)=a0, qdd(tf)=af —
    로 계수 6개 (c0 ~ c5) 를 정한다. 경계 속도·가속도가 모두 0 인 기본형은

        tau = (t - t0) / (tf - t0)
        s(tau) = 10 tau^3 - 15 tau^4 + 6 tau^5
        q(t) = q0 + (qf - q0) s(tau)

    로 닫힌 꼴이 있고, 일반형은 6x6 선형계를 풀면 된다. 어느 쪽으로 구현해도 된다.
    q0, qf 가 스칼라이면 (N,), (D,) 이면 (N, D) 를 돌려준다.

    Returns
    -------
    q, qd, qdd : 위치, 속도, 가속도 (해석적 미분. 유한차분이 아니다)
    """
    # TODO: 문제 4-4
    t = np.asarray(t, dtype=float)
    is_scalar = np.isscalar(q0) or (isinstance(q0, np.ndarray) and q0.ndim == 0)

    # (1, D) 형태 배열로 변환하여 다차원 계산 통일
    q0_arr = np.atleast_1d(q0).astype(float)
    qf_arr = np.atleast_1d(qf).astype(float)
    v0_arr = np.atleast_1d(v0).astype(float)
    vf_arr = np.atleast_1d(vf).astype(float)
    a0_arr = np.atleast_1d(a0).astype(float)
    af_arr = np.atleast_1d(af).astype(float)

    # 입력값 크기 broadcasting 맞춤
    D = len(q0_arr)
    v0_arr = np.broadcast_to(v0_arr, (D,))
    vf_arr = np.broadcast_to(vf_arr, (D,))
    a0_arr = np.broadcast_to(a0_arr, (D,))
    af_arr = np.broadcast_to(af_arr, (D,))

    T = float(tf - t0)
    if T <= 0:
        raise ValueError("tf 는 t0 보다 커야 합니다.")

    # 6x6 계수 행렬 구축 (tau = (t - t0)/T 공간에서 0 <= tau <= 1)
    A = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
        [0, 1, 2, 3, 4, 5],
        [0, 0, 2, 6, 12, 20]
    ], dtype=float)

    # 우변 경계조건 b: (6, D)
    b = np.vstack([
        q0_arr,
        v0_arr * T,
        a0_arr * (T**2),
        qf_arr,
        vf_arr * T,
        af_arr * (T**2)
    ])

    # 계수 c (6, D) 푸기
    c = np.linalg.solve(A, b)

    # tau, tau^2, ... 계산 (N,)
    tau = (t - t0) / T
    tau = np.clip(tau, 0.0, 1.0)  # 범위 제한

    tau2 = tau**2
    tau3 = tau**3
    tau4 = tau**4
    tau5 = tau**5

    # 위치 s(tau), 속도 s'(tau), 가속도 s''(tau) 계산 (N, 6)
    tau_p = np.column_stack([np.ones_like(tau), tau, tau2, tau3, tau4, tau5])
    tau_dp = np.column_stack([np.zeros_like(tau), np.ones_like(tau), 2*tau, 3*tau2, 4*tau3, 5*tau4])
    tau_ddp = np.column_stack([np.zeros_like(tau), np.zeros_like(tau), 2*np.ones_like(tau), 6*tau, 12*tau2, 20*tau3])

    # 행렬 곱을 통한 궤적 계산: (N, 6) @ (6, D) -> (N, D)
    q = tau_p @ c
    qd = (tau_dp @ c) / T
    qdd = (tau_ddp @ c) / (T**2)

    # 스칼라 입력이었으면 (N,) 크기로 리턴
    if is_scalar:
        return q.squeeze(-1), qd.squeeze(-1), qdd.squeeze(-1)

    return q, qd, qdd


def finite_diff(y, t) -> np.ndarray:
    """시간축(axis 0)에 대한 수치 미분. `np.gradient(y, t, axis=0)` 를 쓰면 된다.

    y : (N,) 또는 (N, D),  t : (N,)
    속도 = finite_diff(q, t),  가속도 = finite_diff(속도, t)
    """
    # TODO: 문제 4-2
    y = np.asarray(y, dtype=float)
    t = np.asarray(t, dtype=float)
    return np.gradient(y, t, axis=0)
