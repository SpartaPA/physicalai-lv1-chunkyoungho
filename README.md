# ROS 2 학습 기록

이 저장소는 ROS 2를 공부하면서 직접 실습한 내용을 정리하고 기록하는 공간입니다. 단순한 예제 코드 모음이 아니라, 핵심 개념을 이해하고 나서 그것을 실제로 실행해 보며 남기는 학습 로그로 구성하고 있습니다.

## 목적

- ROS 2의 기본 개념을 정리한다.
- Publisher / Subscriber, Topic, Parameter 등 실습 내용을 기록한다.
- Python 기반 `rclpy` 예제를 직접 실행하며 이해를 깊게 한다.
- 추후 로봇 제어, 시뮬레이션, URDF 활용으로 확장할 수 있는 기반을 만든다.

## 학습 범위

- ROS 2 기본 구조
- Node / Topic / Message
- Publisher / Subscriber
- Parameter 사용
- CLI 명령어 활용
- Python ROS 2 개발 (`rclpy`)
- URDF / 로봇 모델
- 로봇 제어와 실험 기록

## 저장소 구조

```text
.
├── LICENSE
├── README.md
├── demo_python/
│   └── demo_python/
│       ├── __init__.py
│       ├── publisher.py
│       ├── subscriber.py
│       └── talker.py
├── URDF/
│   └── robot.urdf
└── .gitignore
```

### 주요 파일 설명

- `demo_python/demo_python/publisher.py`
  - `/cmd_vel` 토픽에 Twist 메시지를 발행하는 예제
  - 속도 명령을 주고받는 기본 동작을 확인하는 데 사용

- `demo_python/demo_python/subscriber.py`
  - `/cmd_vel` 토픽을 구독하여 수신한 메시지를 로그로 출력
  - Topic 통신 흐름을 이해하는 데 적합

- `demo_python/demo_python/talker.py`
  - 문자열 메시지를 게시하는 기본 ROS 2 노드 예제
  - Parameter로 발행 주기와 메시지 prefix를 설정하는 연습

- `URDF/robot.urdf`
  - 로봇 형태를 설명하는 URDF 파일
  - 이후 TF, 시뮬레이션, 모델링 실습에 확장 가능

## 개발 환경

- Ubuntu 22.04
- ROS 2 (Humble)
- Python 3
- `rclpy`
- Git / GitHub


## 기본 실행 방법

ROS 2 환경을 먼저 활성화합니다.


```bash
source /opt/ros/humble/setup.bash
```

```markdown
## 실습 제목

- 날짜:
- 목표:
- 핵심 개념:
- 구현 내용:
- 실행 결과:
- 문제점과 해결 방법:
- 추가 학습 사항:
```

예시:

```markdown
## Topic 통신 실습

- 날짜: 2026-08-14
- ROS 2 버전: Humble
- 목표: Publisher와 Subscriber 간 메시지 흐름 이해
- 핵심 개념: Topic, Message, Queue, rclpy node
- 구현 내용: `/cmd_vel` 토픽에 Twist 메시지 발행 및 수신
- 실행 결과: subscriber에서 속도 값 로그 확인
- 문제점과 해결 방법: 환경 변수 미설정 -> source /opt/ros/humble/setup.bash
- 추가 학습 사항: qos depth, timeout, multi-node 구조
```

## 목표

ROS 2의 기본 구조와 동작 원리를 이해하고, 작은 노드부터 로봇 제어까지 확장할 수 있는 기반을 만드는 것이 이 저장소의 최종 목표입니다.

꾸준히 실습을 기록하면서, 단순한 코드 실험이 아니라 학습 과정 자체를 남기는 저장소로 발전시키고자 합니다.

