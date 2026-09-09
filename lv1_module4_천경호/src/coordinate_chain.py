"""문제 6 — 좌표 변환 체인 모듈. (학생 작성용 템플릿)

base -> link -> camera 로 이어지는 동차변환 체인을 구성하고,
카메라 기준 좌표를 로봇 base 기준으로 바꾼다.
모듈 4(픽앤플레이스 미니 프로젝트)에서 그대로 import 해 쓰게 되므로,
공개 함수 이름과 반환 형식을 이 템플릿 그대로 유지한다.
"""

from __future__ import annotations

import numpy as np

from .rotation import axis_angle_from_matrix, rot_x, rot_y, rot_z
from .transform import inv_T, make_T, transform_points

__all__ = ["CoordinateChain", "default_chain", "camera_point_to_base", "base_point_to_camera"]


class CoordinateChain:
    """부모 -> 자식 동차변환을 이름으로 등록하고, 임의의 두 프레임 사이 변환을 만든다.

    TF2 의 축소판이라고 보면 된다.

    Examples
    --------
    >>> chain = CoordinateChain("base")
    >>> chain.add("base", "link", T_base_link)
    >>> chain.add("link", "camera", T_link_camera)
    >>> T = chain.T("base", "camera")     # camera 좌표 -> base 좌표
    """

    def __init__(self, root: str = "base"):
        self.root = root
        self._parent: dict[str, str] = {}                 # child -> parent
        self._T: dict[tuple[str, str], np.ndarray] = {}   # (parent, child) -> T

    def add(self, parent: str, child: str, T) -> "CoordinateChain":
        """parent 기준으로 표현된 child 프레임의 자세 T(parent<-child) 를 등록한다.

        체이닝이 되도록 self 를 돌려준다. 4x4 가 아니면 ValueError.
        """
        T = np.asarray(T, dtype=float)
        if T.shape != (4, 4):
            raise ValueError(f"4x4 동차변환이 필요합니다. 받은 shape={T.shape}")
        self._parent[child] = parent
        self._T[(parent, child)] = T
        return self

    def get(self, parent: str, child: str) -> np.ndarray:
        """등록해 둔 T(parent <- child) 를 그대로 돌려준다."""
        return self._T[(parent, child)]

    def frames(self) -> list[str]:
        """등록된 프레임 이름 목록 (root 포함)."""
        return [self.root] + list(self._parent.keys())

    # ------------------------------------------------------ 여기부터 구현

    def _path_to_root(self, frame: str) -> list[str]:
        """frame 에서 root 까지의 경로 [frame, ..., root] 를 만든다.

        root 에 연결되어 있지 않으면 KeyError.        
        """
        # TODO: 문제 6-1
        if frame not in self.frames():
            raise KeyError(f"존재하지 않는 프레임입니다.: '{frame}'")

        path = [frame]
        current = frame

        while current != self.root:
            if current not in self._parent:
                #root에 도달하지 못했는데 더 이상 부모가 없는 경우 (고립된 노드)
                raise KeyError(f"프레임 '{frame}'이(가) root '{self.root}'에 연결되어 있지 않습니다.")
            current = self._parent[current]
            path.append(current)
        return path
    
    def T_from_root(self, frame: str) -> np.ndarray:
        """root 기준 frame 의 자세 T(root <- frame).
        경로를 따라가며 등록된 변환을 곱한다. 곱하는 **순서**에 주의할 것:
        윗첨자/아랫첨자가 이웃끼리 상쇄되도록 놓으면 틀리지 않는다.
            T(base<-camera) = T(base<-link) @ T(link<-camera)
        """
        # TODO: 문제 6-1
        path = self._path_to_root(frame)
        T_root_frame = np.identity(4, dtype=float)
        
        for cur in reversed(path[0:-1]):            
            T_root_frame=T_root_frame@self.get(self._parent[cur],cur)
        return T_root_frame

    def T(self, target: str, source: str) -> np.ndarray:
        """source 좌표를 target 좌표로 바꾸는 변환 T(target <- source).

        힌트: T(target<-source) = inv(T(root<-target)) @ T(root<-source)
        """
        # TODO: 문제 6-1

        return inv_T(self.T_from_root(target)) @ self.T_from_root(source)        

    def transform(self, target: str, source: str, P, w: float = 1.0) -> np.ndarray:
        """source 프레임의 점(w=1) 또는 방향(w=0)을 target 프레임으로 변환한다.

        (3,) 와 (N,3) 을 모두 지원해야 하고, **반복문을 쓰지 않는다**.

        """
        # TODO: 문제 6-2
        T = self.T(target, source)
        return transform_points(T,P,w)
        

    def axis_angle(self, target: str, source: str):
        """T(target <- source) 의 회전 부분에서 회전축과 회전각을 복원한다."""
        # TODO: 문제 6-4
        raise NotImplementedError("axis_angle 을 구현하세요")


def default_chain() -> CoordinateChain:
    """과제에서 쓸 기본 체인(base -> link -> camera)을 만든다.

    지시문은 '임의의 회전·병진'을 쓰라고 하지만, 채점 수치를 맞추기 위해
    아래 값을 그대로 쓰기를 권장한다. (바꾸려면 노트북에도 그 값을 명시할 것)

    base -> link   : z축 30도 회전 후 (0.30, 0.00, 0.40) m 이동
    link -> camera : y축 -20도, x축 90도 회전(y 먼저 곱함) 후 (0.10, 0.05, 0.15) m 이동
    """
    # TODO: 문제 6-1
    #   T_base_link   = make_T(rot_z(...), [...])
    #   T_link_camera = make_T(rot_y(...) @ rot_x(...), [...])
    #   return CoordinateChain("base").add(...).add(...)
    #T_base_link = make_T(rot_z(np.deg2rad(22.5)),[0.35,0.05,0.45])
    #T_link_camera = make_T(rot_y(np.deg2rad(-22.5))@rot_x(np.deg2rad(67.5)),[0.12,0.04,0.18])
    T_base_link = make_T(rot_z(np.deg2rad(30)),[0.30,0.0,0.40])
    T_link_cam = make_T(rot_y(np.deg2rad(-20))@rot_x(np.deg2rad(90)),[0.10,0.05,0.15])
    """Examples
        --------
        >>> chain = CoordinateChain("base")
        >>> chain.add("base", "link", T_base_link)
        >>> chain.add("link", "camera", T_link_camera)
        >>> T = chain.T("base", "camera")     # camera 좌표 -> base 좌표
        """
    return CoordinateChain("base").add("base", "link", T_base_link).add("link", "camera", T_link_cam)
    


def camera_point_to_base(p_cam, chain: CoordinateChain | None = None) -> np.ndarray:
    """카메라 기준 좌표 -> base 기준 좌표. (3,) 와 (N,3) 모두 지원.

    chain 이 None 이면 default_chain() 을 쓴다.
    """
    # TODO: 문제 6-1
    if chain == None:
        chain = default_chain()

    #Numpy변환
    p_cam = np.asarray(p_cam, dtype=float)
    p_cam_shape = p_cam.shape

    # camera -> base 동차변환행렬
    T_base_camera = chain.T("base","camera")

    return transform_points(T_base_camera,p_cam,1.0)


def base_point_to_camera(p_base, chain: CoordinateChain | None = None) -> np.ndarray:
    """base 기준 좌표 -> 카메라 기준 좌표. 왕복 검증(문제 6-2)에 쓴다."""
    # TODO: 문제 6-2

    if chain == None:
            chain = default_chain()
    p_base = np.asarray(p_base, dtype=float)

    # camera->base 동차변환행렬
    T_base_camera = chain.T("base","camera")
    T_camera_base = inv_T(T_base_camera)  

    return transform_points(T_camera_base,p_base)
