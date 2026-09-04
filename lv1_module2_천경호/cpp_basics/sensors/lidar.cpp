#include <iostream>
#include "lidar.hpp"

Lidar::~Lidar()
{
    std::cout << "Lidar 소멸" << std::endl;
}
std::vector<double> Lidar::read()
{ // override: 재정의임을 명시
    return {0.1, 0.1, 0.1};
}