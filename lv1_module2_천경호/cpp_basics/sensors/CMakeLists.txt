# CMakeLists.txt
cmake_minimum_required(VERSION 3.16)
project(robot_controller CXX)

set(CMAKE_CXX_STANDARD 17)             # C++17 사용

add_executable(sensor.out                    # 실행파일 sensor.out 아래의 소스들로 만든다
    sensor_main.cpp
    sensor.cpp
    imu.cpp
    lidar.cpp
)
target_include_directories(sensor.out PRIVATE include)   # 헤더 위치
# target_link_libraries(robot PRIVATE rclcpp::rclcpp)  # 외부 라이브러리 (ROS2에서)
