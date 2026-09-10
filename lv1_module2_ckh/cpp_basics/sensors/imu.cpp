#include "imu.hpp"
#include <vector>
#include <iostream>

std::vector<double> IMU::read()
{
    return {0.2, 0.2, 0.2};
}
IMU::~IMU()
{
    std::cout << "IMU 소멸" << std::endl;
}