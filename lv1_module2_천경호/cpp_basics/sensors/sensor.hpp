#include<vector>

# ifndef SENSOR_H
# define SENSOR_H

class Sensor {
public:
    virtual ~Sensor() = default;          // 가상 소멸자 (상속 시 필수!)
    /*
    {
        std::cout << "Sensor 소멸" << std::endl;
    }
        */
    virtual std::vector<double> read() = 0;  // = 0: 순수 가상 (자식이 반드시 구현)
    bool isConnected() const;
protected:
    bool connected_ = false;
};

#endif