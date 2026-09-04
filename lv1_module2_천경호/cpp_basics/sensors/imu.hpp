#include "sensor.hpp"

#ifndef IMU_H
#define IMU_H

class IMU : public Sensor {             // public 상속
public:
    std::vector<double> read() override;  // override: 재정의임을 명시        
    ~IMU();
};

#endif