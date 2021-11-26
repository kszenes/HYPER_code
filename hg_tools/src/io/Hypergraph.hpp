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

    
    Offset offset;

    void print_incident_list() const;



};

void Hypergraph::print_incident_list() const {
  std::cout << "incident_nets" << std::endl;
  for (int i = 0; i < incident_nets.size(); i++)
  {
    std::cout << "node " << i << ":\t";
    for (auto j : incident_nets[i])
    {
      std::cout << j << " ";
    }
    std::cout << std::endl;
  }
}

#endif //HYPER_CODE_HYPERGRAPH_H
