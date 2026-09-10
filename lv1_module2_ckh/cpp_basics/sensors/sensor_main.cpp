#include <vector>
#include <unordered_map>
#include <algorithm>
#include <memory>
#include <iostream>
#include <typeinfo>
#include <string>

#include "sensor.hpp"
#include "lidar.hpp"
#include "imu.hpp"
using namespace std;


int main()
{
    // 동적할당 및 지역변수로 Sensor 객체 생성
    cout << "2-2 동적할당 및 지역변수선언" << endl;
    vector<unique_ptr<Sensor>> sensors;
    sensors.push_back(make_unique<Lidar>());
    sensors.push_back(make_unique<IMU>());
    IMU imu;
    // 다형성 루프로 출력
    for (auto &s : sensors)
    {
        auto data = s->read();
        cout << "2-1 ";
        for (double val : data)
        { // vector<double> 하나씩 출력하기
            cout << val << " ";
        }
        cout << "\n";
    }
    // 동적할당 종료 테스트
    cout << "2-2 동적할당 종료" << endl;
    for (auto &s : sensors)
    {
        sensors.pop_back();
    }

    //count_if 결과 만들기
    unordered_map<string, unique_ptr<Sensor>> uo_sensors;
    uo_sensors.insert(make_pair("lidar", make_unique<Lidar>()));
    vector<double> lidar_output = uo_sensors.find("lidar")->second->read();
    auto count = count_if(lidar_output.begin(),lidar_output.end(),[](double dist){
        return dist <= 0.35;
    });
    cout << "2-4 lidar 0.35 이내 점: " << count << " 개\n";


    
    // 마지막 종료시에 지역변수 객체 소멸 확인
    cout << "2-2 프로그램 종료" << endl;
}
