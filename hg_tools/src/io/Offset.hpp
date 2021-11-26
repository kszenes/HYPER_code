#ifndef HYPER_CODE_OFFSET_H
#define HYPER_CODE_OFFSET_H

#include"includes.hpp"

class Offset {

public:

    int num_pins = 0;

    std::vector<int> offsets;
    std::vector<int> sizes;

    std::vector<int> pins;

};


#endif //HYPER_CODE_OFFSET_H