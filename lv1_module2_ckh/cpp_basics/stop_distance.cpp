#include <iostream>
#include <array>

double computeStopDistance(double speed, double decel = 1.5)
{
    return speed * speed / (2.0 * decel);
}

int main(int argc, char *argv[])
{
    
    if (argc < 3)
    {
        std::cout << "사용법: " << argv[0] << "<속도 실수> <감속도 실수>\n";
        return 1;
    }

    std::array<double, 2> values;
    double value;
    double distance;

    for (int i = 1; i <= argc - 1; i++)
    {
        
        try
        {
            std::size_t pos;
            // 문자열을 double로 변환 시도
            value = std::stod(argv[i], &pos);
            // 문자열에 숫자가 아닌 문자가 섞인 경우
            if (pos != std::string(argv[i]).size())
            {
                throw std::invalid_argument("입력에 숫자가 아닌 값이 있습니다.");
            }            
            
            values[i - 1] = value;
        }
        catch (const std::invalid_argument &e)
        {
            // 숫자로 변환할 수 없는 문자열인 경우 (예: "abc")
            std::cerr << "오류: 숫자가 아닙니다.\n";
        }
        catch (const std::out_of_range &e)
        {
            // double 범위를 벗어난 숫자인 경우
            std::cerr << "오류: 표현 가능한 double 범위를 초과했습니다.\n";
        }
    }

    distance = computeStopDistance(values[0], values[1]);
    std::cout << "velocity: " << values[0] << " m/s   decle: " << values[1] << " m/s^2     stop distance: " << distance << " m\n";
}