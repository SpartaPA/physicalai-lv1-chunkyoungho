"""문제 3 — 쿼터니언 변환과 SLERP. (학생 작성용 템플릿)

규약
----
- 쿼터니언은 길이 4 배열 **(x, y, z, w)** 다. 모듈 ③ 의 `quaternion_from_axis_angle` 과
  SciPy `Rotation.as_quat()` 와 같은 순서다. w 가 스칼라(실수부)다.
- q 와 -q 는 같은 회전이다 (이중 덮개). 비교할 때는 부호를 무시하거나 |q . q_ref| 를 본다.
- 보간은 항상 **짧은 호**를 택한다: q0 . q1 < 0 이면 q1 의 부호를 뒤집고 시작한다.

SciPy 는 검산(비교) 용도로만 쓴다. 이 파일 안에서는 numpy 만 사용한다.
"""

from __future__ import annotations

import numpy as np
from .vectors import norm, dot

__all__ = ["matrix_to_quaternion", "quaternion_to_matrix", "slerp", "lerp_quat", "quat_angle"]


def matrix_to_quaternion(R) -> np.ndarray:
    """회전행렬 (3,3) -> 단위 쿼터니언 (x, y, z, w).

    권장 방법 (Shepperd): trace 가 양수이면 w 부터, 아니면 대각성분이 가장 큰 축부터 계산해
    0 으로 나누는 일을 피한다. 180도 회전(trace = -1)에서도 동작해야 한다.

        t = trace(R)
        t > 0        : s = 2 sqrt(1 + t);      w = s/4; x = (R21 - R12)/s; ...
        R00 이 최대  : s = 2 sqrt(1 + R00 - R11 - R22);  x = s/4; w = (R21 - R12)/s; ...
        (R11, R22 최대인 경우도 같은 꼴)

    반환값은 반드시 정규화하고, w >= 0 이 되도록 부호를 맞춘다 (비교가 편해진다).
    """
    # TODO: 문제 3-1
    
    """회전행렬 (3,3) -> 단위 쿼터니언 (x, y, z, w)."""
    R = np.asarray(R, dtype=float)
    if R.shape != (3, 3):
        raise ValueError(f"회전행렬 R의 shape는 (3,3)이어야 합니다. 입력: {R.shape}")

    trace = np.trace(R)

    if trace > 0.0:
        s = 2.0 * np.sqrt(1.0 + trace)
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    elif (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):
        s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s

    q = np.array([x, y, z, w], dtype=float)

    # w >= 0 이 되도록 부호 맞춤 (q와 -q는 동일한 회전)
    if q[3] < 0.0:
        q = -q

    # 단위 쿼터니언으로 정규화
    q_norm = norm(q)
    if q_norm > 0:
        q = q / q_norm

    return q


def quaternion_to_matrix(q) -> np.ndarray:
    """단위 쿼터니언 (x, y, z, w) -> 회전행렬 (3,3).

        R = [[1 - 2(y^2 + z^2),   2(xy - zw),        2(xz + yw)],
             [2(xy + zw),         1 - 2(x^2 + z^2),  2(yz - xw)],
             [2(xz - yw),         2(yz + xw),        1 - 2(x^2 + y^2)]]

    입력이 정확히 단위가 아닐 수 있으므로 먼저 정규화한다. q 와 -q 는 같은 R 을 준다.
    """
    # TODO: 문제 3-1
    """단위 쿼터니언 (x, y, z, w) -> 회전행렬 (3,3)."""
    q = np.asarray(q, dtype=float)
    if q.shape != (4,):
        raise ValueError(f"쿼터니언 q의 shape는 (4,)이어야 합니다. 입력: {q.shape}")

    # 입력 쿼터니언 정규화
    q_norm = norm(q)
    if q_norm == 0:
        raise ValueError("크기가 0인 쿼터니언은 회전행렬로 변환할 수 없습니다.")
    q = q / q_norm

    x, y, z, w = q

    R = np.array([
        [1.0 - 2.0 * (y**2 + z**2), 2.0 * (x * y - z * w), 2.0 * (x * z + y * w)],
        [2.0 * (x * y + z * w), 1.0 - 2.0 * (x**2 + z**2), 2.0 * (y * z - x * w)],
        [2.0 * (x * z - y * w), 2.0 * (y * z + x * w), 1.0 - 2.0 * (x**2 + y**2)]
    ], dtype=float)

    return R


def quat_angle(q0, q1) -> float:
    """두 단위 쿼터니언이 나타내는 회전 사이의 각도 [rad], 0 <= angle <= pi.

        angle = 2 * arccos(|q0 . q1|)
    """
    # TODO: 문제 3-2 (slerp 안에서 재사용)
    """두 단위 쿼터니언이 나타내는 회전 사이의 각도 [rad], 0 <= angle <= pi."""
    q0 = np.asarray(q0, dtype=float)
    q1 = np.asarray(q1, dtype=float)

    # 내적 계산 및 부동소수점 오차 클리핑
    q_dot = dot(q0, q1)
    dot_clipped = np.clip(np.abs(q_dot), 0.0, 1.0)

    # angle = 2 * arccos(|q0 . q1|)
    angle = 2.0 * np.arccos(dot_clipped)
    return float(angle)


def slerp(q0, q1, t: float, eps: float = 1e-8) -> np.ndarray:
    """구면 선형 보간 (Spherical Linear intERPolation).

        d = q0 . q1                      (d < 0 이면 q1 = -q1, d = -d 로 짧은 호 선택)
        omega = arccos(d)
        q(t) = [sin((1-t) omega) q0 + sin(t omega) q1] / sin(omega)

    경계 상황
    - 두 자세가 거의 같아 d > 1 - eps 이면 sin(omega) ~ 0 이라 나눗셈이 불안정하다.
      이때는 선형 보간 후 정규화로 대체한다.
    - d 는 부동소수점 오차로 1 을 살짝 넘을 수 있으므로 clip 한다.

    반환값은 단위 쿼터니언이어야 한다. t = 0 이면 q0, t = 1 이면 (부호를 맞춘) q1.
    """
    # TODO: 문제 3-2 · 3-5
    """구면 선형 보간 (Spherical Linear intERPolation)."""
    q0 = np.asarray(q0, dtype=float)
    q1 = np.asarray(q1, dtype=float)

    # 단위 쿼터니언 정규화
    q0 = q0 / norm(q0)
    q1 = q1 / norm(q1)

    # 내적 계산
    q_dot = dot(q0, q1)

    # 최단 경로(짧은 호) 선택: 내적이 음수이면 q1의 부호를 반대로 변경
    if q_dot < 0.0:
        q1 = -q1
        q_dot = -q_dot

    # 부동소수점 오차 방지를 위해 [0.0, 1.0] 범위로 클리핑
    q_dot = np.clip(q_dot, 0.0, 1.0)

    # 두 쿼터니언이 거의 같은 경우 (선형 보간 후 정규화 대체)
    if q_dot > 1.0 - eps:
        res = (1.0 - t) * q0 + t * q1
        return res / norm(res)

    # 구면 보간 계산
    omega = np.arccos(q_dot)
    sin_omega = np.sin(omega)

    scale0 = np.sin((1.0 - t) * omega) / sin_omega
    scale1 = np.sin(t * omega) / sin_omega

    q_t = scale0 * q0 + scale1 * q1

    # 단위 쿼터니언 정규화
    return q_t / norm(q_t)


def lerp_quat(q0, q1, t: float, normalize: bool = False) -> np.ndarray:
    """성분별 단순 선형 보간 (비교용).

        q(t) = (1 - t) q0 + t q1          (q0 . q1 < 0 이면 q1 부호를 먼저 뒤집는다)

    normalize=False 이면 정규화하지 않은 값을 그대로 돌려준다 — 크기가 1 에서 얼마나
    벗어나는지 관찰하는 데 쓴다. normalize=True 이면 정규화한다 (NLERP).
    """
    # TODO: 문제 3-4
    """성분별 단순 선형 보간 (비교용)."""
    q0 = np.asarray(q0, dtype=float)
    q1 = np.asarray(q1, dtype=float)

    # 최단 경로(짧은 호) 선택
    if dot(q0, q1) < 0.0:
        q1 = -q1

    # 단순 선형 보간
    q_t = (1.0 - t) * q0 + t * q1

    # normalize 옵션에 따른 정규화 처리
    if normalize:
        q_norm = norm(q_t)
        if q_norm > 0:
            q_t = q_t / q_norm

    return q_t
