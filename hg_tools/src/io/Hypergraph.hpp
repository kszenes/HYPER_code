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
    std::vector<bool> node_active;
    // std::vector<std::vector<std::vector<int>>> *vertex_list;

    // first: coarsend into node; second: coarsend node
    std::vector<std::pair<int, int>> coarsen_list;
    
    Offset offset;

    void print_incident_list() const;
    void coarsen(int u, int v);



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

void Hypergraph::coarsen(int u, int v) {
  coarsen_list.push_back(std::make_pair(u, v));
  // loop over incident nets
  for (const int v_net : incident_nets[v]) {
    bool relink = true;
    // find first and last element corresponding to net 
    int first = offset.offsets[v_net];
    int last = offset.offsets[v_net] + offset.sizes[v_net] - 1;
    // std::cout << "first = " << first << " last = " << last << std::endl; 
    // loop over pins in net
    for (int net_pin = first; net_pin < last; net_pin++) {
      int current_pin = offset.adjacency[net_pin];
      // std::cout << "current_pin = " << current_pin << std::endl;
      if (current_pin == u) {
        relink = false;
        std::cout << "u found" << std::endl;
      } else if (current_pin == v) {
        std::swap(offset.adjacency[current_pin], offset.adjacency[last]);
        std::cout << "v found" << std::endl;
        if (offset.adjacency[current_pin] == u) {
          relink = false;
          std::cout << "u found" << std::endl;
        }
      }
    }
    
    if (relink) {
      // relink operation
      offset.adjacency[last] = u;
      incident_nets[u].push_back(v_net);
    } else {
      // delete operation
      offset.sizes[v_net]--; 
    }
    node_active[v] = 0;
    std::cout << "Relink needed for net " << v_net << " : " << relink << std::endl;


  }

}

#endif //HYPER_CODE_HYPERGRAPH_H
