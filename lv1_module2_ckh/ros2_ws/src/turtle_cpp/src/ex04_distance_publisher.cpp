#include <cmath>
#include <chrono>
#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "std_msgs/msg/float32.hpp"
#include "turtlesim/msg/pose.hpp"

using namespace std::chrono_literals;

class DistancePublisher : public rclcpp::Node
{
public:
  DistancePublisher()
  : Node("turtle_distance_publisher"),
    latest_pose_(nullptr)
  {
    // ---------- 파라미터 선언 ----------
    rcl_interfaces::msg::ParameterDescriptor descriptor;
    descriptor.description = "/turtle_distance 발행 주기 [Hz], 0 보다 커야 함";
    this->declare_parameter<double>("publish_rate", 10.0, descriptor);

    double rate = this->get_parameter("publish_rate").as_double();

    // ---------- 구독 ----------
    // QoS 설정: Reliable, Volatile, Depth 10
    rclcpp::QoS pose_qos(10);
    pose_qos.reliability(rclcpp::ReliabilityPolicy::Reliable);
    pose_qos.durability(rclcpp::DurabilityPolicy::Volatile);

    // 상대 이름 'turtle1/pose' 사용
    pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
      "turtle1/pose",
      pose_qos,
      std::bind(&DistancePublisher::on_pose, this, std::placeholders::_1));

    // ---------- 발행 ----------
    dist_pub_ = this->create_publisher<std_msgs::msg::Float32>("turtle_distance", 10);

    // ---------- 타이머 ----------
    auto timer_period = std::chrono::duration<double>(1.0 / rate);
    timer_ = this->create_wall_timer(
      timer_period,
      std::bind(&DistancePublisher::on_timer, this));

    // ---------- 파라미터 변경 콜백 ----------
    param_callback_handle_ = this->add_on_set_parameters_callback(
      std::bind(&DistancePublisher::on_set_parameters, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "turtle_distance_publisher 시작: publish_rate=%.1f Hz", rate);
  }

private:
  // 최신 자세 저장 콜백
  void on_pose(const turtlesim::msg::Pose::SharedPtr msg)
  {
    latest_pose_ = msg;
  }

  // 주기적 발행 타이머 콜백
  void on_timer()
  {
    if (!latest_pose_) {
      RCLCPP_WARN_THROTTLE(
        this->get_logger(),
        *this->get_clock(),
        1000,  // ms 단위 (1초)
        "아직 /turtle1/pose 를 받지 못했습니다");
      return;
    }

    auto msg = std_msgs::msg::Float32();
    msg.data = std::hypot(latest_pose_->x, latest_pose_->y);  // 원점(0,0)에서의 거리
    dist_pub_->publish(msg);
  }

  // 파라미터 동적 변경 콜백
  rcl_interfaces::msg::SetParametersResult on_set_parameters(
    const std::vector<rclcpp::Parameter> & parameters)
  {
    rcl_interfaces::msg::SetParametersResult result;
    result.successful = true;

    for (const auto & param : parameters) {
      if (param.get_name() == "publish_rate") {
        if (param.get_type() != rclcpp::ParameterType::PARAMETER_DOUBLE) {
          result.successful = false;
          result.reason = "publish_rate 는 double 이어야 합니다 (예: 5.0)";
          return result;
        }

        double new_rate = param.as_double();
        if (new_rate <= 0.0) {
          result.successful = false;
          result.reason = "publish_rate 는 0 보다 커야 합니다";
          return result;
        }

        // 기존 타이머 취소 후 새 타이머 생성
        timer_->cancel();
        auto timer_period = std::chrono::duration<double>(1.0 / new_rate);
        timer_ = this->create_wall_timer(
          timer_period,
          std::bind(&DistancePublisher::on_timer, this));

        RCLCPP_INFO(this->get_logger(), "publish_rate 변경 → %.1f Hz (타이머 재생성)", new_rate);
      }
    }
    return result;
  }

  // 멤버 변수
  turtlesim::msg::Pose::SharedPtr latest_pose_;
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
  rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr dist_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  OnSetParametersCallbackHandle::SharedPtr param_callback_handle_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<DistancePublisher>();

  try {
    rclcpp::spin(node);
  } catch (const std::exception & e) {
    RCLCPP_INFO(node->get_logger(), "정상 종료합니다: %s", e.what());
  } 
  
  // 2. Ctrl+C를 눌러 spin이 풀려난 바로 직후 실행됨
  RCLCPP_INFO(node->get_logger(), "Ctrl+C — 정상 종료합니다");

  rclcpp::shutdown();
  return 0;
}