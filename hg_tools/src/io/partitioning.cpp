#include"includes.hpp"


/**
 * @brief Reads mtx file
 * 
 * @param filename 
 * @return tuple containing number of rows, cols and matrix
 */
void mtx2matrix(const std::string& filename, Hypergraph &graph) {
  std::ifstream file(filename);
  int num_nets, num_nodes, num_pins;

  // Ignore comments headers
  while (file.peek() == '%') file.ignore(2048, '\n');

  // Read number of rows and columns
  file >> num_nets >> num_nodes >> num_pins;

  std::vector<std::vector<int>> incident_nets(num_nodes);

  graph.offset.num_pins = num_pins;
  std::vector<int> offsets(num_nets+1, 0);
  std::vector<int> sizes(num_nets+1, 0);
  std::vector<int> pins(num_pins, 0);

  std::vector<std::vector<int>> temp_pins(num_pins);

  // Set incident_nets and sizes
  double data = 1.0;
  for (int l = 0; l < num_pins; l++)
  {
      int edge, node;
      file >> edge >> node;
      // matrix[(edge -1) + (node -1) * num_nets] = data;
      incident_nets[node-1].push_back(edge-1);
      temp_pins[edge-1].push_back(node-1);
      sizes[edge-1]++;
  }

  // Set offsets
  std::partial_sum(sizes.begin(), sizes.end(), offsets.begin()+1);
  graph.offset.offsets = offsets;

  // Set pins
  int counter = 0;
  for (int i = 0; i < num_nets; i++) {
    for (const auto j : temp_pins[i]) {
      pins[counter] = j;
      counter++;
    }
  }

  file.close();
  graph.num_nodes = num_nodes;
  graph.num_pins = num_nets;
  // graph.matrix = matrix;
  graph.num_pins = num_pins;

  graph.incident_nets = incident_nets;
  graph.offset.sizes = sizes;
  graph.offset.pins = pins;
  graph.node_active = std::vector<bool>(num_nodes, 1);
}


/**
 * @brief Creates epsilon balanced random partition
 * 
 * @param part: vector containing partitions
 * @param num_partitions 
 * @param num_vertices 
 * @param condition: max amount of vertex allowed in cluster (for epsilon-balanced partitioning)
 */
void random_partitions(std::vector<std::vector<int>> &part, int num_partitions, int num_vertices, int condition) {
  std::random_device rand_dev;
  std::mt19937 generator(rand_dev());
  std::uniform_int_distribution<int> distr(0, num_partitions-1);


  int rand_int = 0;
  bool move_accepted = false;
  for (int vertex = 0; vertex < num_vertices; vertex++) {
    move_accepted = false;
    while (!move_accepted) {
      rand_int = distr(generator);
      if (part[rand_int].size() < condition) {
        part[rand_int].push_back(vertex);
        move_accepted = true;
      }
    }
  }

}

/**
 * @brief Compute max number of vertices allowed in cluster
 * 
 * @param num_vertices 
 * @param num_partitions 
 * @param epsilon 
 * @return max number of vertices allowed in cluster
 */
double compute_condition(int num_vertices, int num_partitions, double epsilon) {
  return (1. + epsilon) * num_vertices / num_partitions;
}

// void compute_connectivity(std::vector<std::vector<int>> &part, Hypergraph &graph){
//   int cost = 0;

//   for (int i = 0; i < graph.num_nets; i++) {
//     std::vector<double> lambda;
//     for (auto j : graph.edges[i]) {
//       for (int k = 0; k < part.size(); k++) {
//         if (std::find(part[k].begin(), part[k].end(), j) != part[k].end()) {
//           if (std::find(lambda.begin(), lambda.end(), k) != lambda.end()) {
//           } else {
//             cost++;
//             // std::cout << "cost increased" << std::endl;
//             lambda.push_back(k);
//           }
//           break;
//       }

//       }
//     }
//   }

//   std::cout << "Cost = " << cost - graph.num_rows << std::endl;

// }

template <typename T>
void print_vec(const std::vector<T>& vec)
{
    for (auto x : vec) {
         std::cout << ' ' << x;
    }
    std::cout << '\n';
}


int main(int argc, char* argv[]) {
  if (argc < 2) {
    std::cerr << "Please provide .mtx file (e.g. $ ./a.out ../../../HYPER_PUBLIC/bcsstk21.mtx)" << std::endl;
    return 0;
  }
  // std::unique_ptr<double[]> matrix;
  // std::tie(num_nets, num_nodes, matrix) = mtx2matrix(argv[1]);

  Hypergraph graph;

  std::vector<std::vector<double>> hmetis;
  mtx2matrix(argv[1], graph);
  int num_nets = graph.num_nets;
  int num_nodes = graph.num_nodes;
  int num_pins = graph.num_pins;
  
  std::cout << "pins" << std::endl;
  print_vec(graph.offset.pins);
  std::cout << "offsets" << std::endl;
  print_vec(graph.offset.offsets);
  std::cout << "sizes" << std::endl;
  print_vec(graph.offset.sizes);
  std::cout << "active" << std::endl;
  print_vec(graph.node_active);
  std::cout << std::endl;

  graph.print_incident_list();

  graph.coarsen(2, 0);

  std::cout << std::endl;
  std::cout << "pins" << std::endl;
  print_vec(graph.offset.pins);
  std::cout << "offsets" << std::endl;
  print_vec(graph.offset.offsets);
  std::cout << "sizes" << std::endl;
  print_vec(graph.offset.sizes);
  std::cout << "active" << std::endl;
  print_vec(graph.node_active);

  graph.print_incident_list();


  // std::cout << "in
  // graph.print_edges();

  // Print out matrix; rows = hyperedges, cols = vertices
  /* for (int edge = 0; edge < num_nets; edge++) {
     for (int node = 0; node < num_nodes; node++) {
       std::cout << matrix[edge + node * num_nets] << " ";
     }
     std::cout << std::endl;
   }*/

  // std::cout << "Num Edges (rows): " << num_nets << ";  Num Vertices (cols): " << num_nodes << "; Num nodes (lines): " << num_pins << std::endl;

  // int num_partitions = 2;
  // double epsilon = 0.2;
  // int condition = compute_condition(num_nodes, num_partitions, epsilon);

  // std::cout << "Clusters can have at most " << condition << " vertices!" << std::endl;

  // std::vector<std::vector<int>> part(num_partitions); 

  // random_partitions(part, num_partitions, num_nodes, condition);
  // compute_connectivity(part, graph);

  // for (int i = 0; i < num_partitions; i++) {
  //   std::cout << "\nCluster " << i << " has " << part[i].size() << " vertices" << std::endl;
  //   for (auto j : part[i]) {
  //     std::cout << j << " ";
  //   }
  //   std::cout << std::endl;
  // }



}