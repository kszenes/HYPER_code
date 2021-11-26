//
// Created by Kalman Szenes on 25.11.21.
//

#ifndef HYPER_CODE_HYPERGRAPH_H
#define HYPER_CODE_HYPERGRAPH_H

#include"includes.hpp"



class Hypergraph {

public:
    int num_nets = 0;
    int num_nodes = 0;
    int num_pins = 0;

    std::vector<std::vector<int>> incident_nets;
    // std::vector<std::vector<std::vector<int>>> *vertex_list;

    std::vector<int> pin_list;
    
    Offset offset;



};


#endif //HYPER_CODE_HYPERGRAPH_H
