#include <vector>
#include <memory>
#include <iostream>
#include <typeinfo>

#include "sensor.hpp"

bool Sensor::isConnected() const { return connected_; }