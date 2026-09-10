#include<memory>
#include<vector>

struct Position
{
    double x;
    double y;
};

int main()
{
    /*
    // 누수검출
    for (int i = 0; i < 1000000; i++)
    {
        Position *ptr = new Position;
    }
    */
    for (int i = 0; i < 1000000; i++)
    {
        std::vector<std::unique_ptr<Position>>ptrs;
        ptrs.push_back(std::make_unique<Position>());
    }
}