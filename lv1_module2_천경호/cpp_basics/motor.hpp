#ifndef MOTOR_H
#define MOTOR_H

class Motor{
    public:
    void setSpeed(double map);
    private:
    double current_speed_ = 0.0;
};

#endif