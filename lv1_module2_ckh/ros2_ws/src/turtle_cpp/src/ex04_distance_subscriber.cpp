#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
#include "rcl_interfaces/msg/parameter_descriptor.hpp"
#include "std_msgs/msg/float32.hpp"

class DistanceSubscriber : public rclcpp::Node
{
public:
  DistanceSubscriber()
  : Node("turtle_distance_subscriber")
  {
    // ---------- 파라미터 선언 ----------
    rcl_interfaces::msg::ParameterDescriptor descriptor;
    descriptor.description = "이 거리[m]를 넘으면 경고 로그";
    this->declare_parameter<double>("warn_distance", 2.5, descriptor);

    warn_distance_ = this->get_parameter("warn_distance").as_double();

    // ---------- 구독 설정 ----------
    // QoS 설정: Reliable, Volatile, Depth 10
    rclcpp::QoS qos(10);
    qos.reliability(rclcpp::ReliabilityPolicy::Reliable);
    qos.durability(rclcpp::DurabilityPolicy::Volatile);

    sub_ = this->create_subscription<std_msgs::msg::Float32>(
      "turtle_distance",
      qos,
      std::bind(&DistanceSubscriber::on_distance, this, std::placeholders::_1));

    // ---------- 파라미터 변경 콜백 ----------
    param_callback_handle_ = this->add_on_set_parameters_callback(
      std::bind(&DistanceSubscriber::on_set_parameters, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "turtle_distance_subscriber 시작: warn_distance=%.2f", warn_distance_);
  }

private:
  // 거리 수신 콜백
  void on_distance(const std_msgs::msg::Float32::SharedPtr msg)
  {
    double d = msg->data;
    if (d > warn_distance_) {
      RCLCPP_WARN(
        this->get_logger(),
        "경고: 원점 거리 %.2f m > 임계 %.2f m", d, warn_distance_);
    } else {
      RCLCPP_DEBUG(this->get_logger(), "거리 %.2f m", d);
    }
  }

  // 파라미터 동적 변경 콜백
  rcl_interfaces::msg::SetParametersResult on_set_parameters(
    const std::vector<rclcpp::Parameter> & parameters)
  {
    rcl_interfaces::msg::SetParametersResult result;
    result.successful = true;

    for (const auto & param : parameters) {
      if (param.get_name() == "warn_distance") {
        if (param.get_type() != rclcpp::ParameterType::PARAMETER_DOUBLE) {
          result.successful = false;
          result.reason = "warn_distance 는 double 이어야 합니다 (예: 0.8)";
          return result;
        }

        double new_val = param.as_double();
        if (new_val < 0.0) {
          result.successful = false;
          result.reason = "warn_distance 는 음수일 수 없습니다";
          return result;
        }

        warn_distance_ = new_val;
        RCLCPP_INFO(this->get_logger(), "warn_distance 변경 → %.2f", warn_distance_);
      }
    }
    return result;
  }

  // 멤버 변수
  double warn_distance_;
  rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr sub_;
  OnSetParametersCallbackHandle::SharedPtr param_callback_handle_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<DistanceSubscriber>();

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