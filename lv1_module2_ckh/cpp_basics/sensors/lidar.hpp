#include "sensor.hpp"


#ifndef LIDAR_H
#define LIDAR_H

class Lidar : public Sensor {             // public 상속
public:
    std::vector<double> read() override;  // override: 재정의임을 명시
    ~Lidar();
};

#endif