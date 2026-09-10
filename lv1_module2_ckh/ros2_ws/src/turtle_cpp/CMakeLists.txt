cmake_minimum_required(VERSION 3.8)
project(turtle_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(turtlesim REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 2. Publisher 노드 빌드 설정 (ex03_distance_publisher)
add_executable(ex04_distance_publisher src/ex04_distance_publisher.cpp)
ament_target_dependencies(ex04_distance_publisher
  rclcpp
  std_msgs
  turtlesim
)
# 3. Subscriber 노드 빌드 설정 (ex03_distance_subscriber)
add_executable(ex04_distance_subscriber src/ex04_distance_subscriber.cpp)
ament_target_dependencies(ex04_distance_subscriber
  rclcpp
  std_msgs
)

# 4. 실행 파일 설치 경로 지정 (ros2 run 으로 실행 가능하게 만듦)
install(TARGETS
  ex04_distance_publisher
  ex04_distance_subscriber
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
