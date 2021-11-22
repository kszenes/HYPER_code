#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include <random>
#include <algorithm>


class Hypergraph {



  public:
    void print_edges() {
      for (int i = 0; i < num_rows; i++) {
        for (auto j : edges[i]) {
          std::cout << j << " ";
        }
        std::cout << std::endl;
      }
    }

    int num_rows = 0;
    int num_cols = 0;
    int num_nodes = 0;
    std::shared_ptr<double[]> matrix;
    std::vector<std::vector<double>> edges;
};

/**
 * @brief Reads mtx file
 * 
 * @param filename 
 * @return tuple containing number of rows, cols and matrix
 */
void mtx2matrix(const std::string& filename, Hypergraph &graph) {
  std::ifstream file(filename);
  int num_row, num_col, num_lines;

  // Ignore comments headers
  while (file.peek() == '%') file.ignore(2048, '\n');

  // Read number of rows and columns
  file >> num_row >> num_col >> num_lines;

  // Create 2D array and fill with zeros
  std::shared_ptr<double[]> matrix(new double[num_row * num_col]);
  std::vector<std::vector<double>> edges(num_row);

  // fill the matrix with data
  double data = 1.0;
  for (int l = 0; l < num_lines; l++)
  {
      int row, col;
      file >> row >> col;
      matrix[(row -1) + (col -1) * num_row] = data;
      edges[row-1].push_back(col-1);
  }

  file.close();
  graph.num_cols = num_col;
  graph.num_rows = num_row;
  graph.matrix = matrix;
  graph.edges = edges;
  graph.num_nodes = num_lines;
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

void compute_connectivity(std::vector<std::vector<int>> &part, Hypergraph &graph){
  int cost = 0;

  for (int i = 0; i < graph.num_rows; i++) {
    std::vector<double> lambda;
    for (auto j : graph.edges[i]) {
      for (int k = 0; k < part.size(); k++) {
        if (std::find(part[k].begin(), part[k].end(), j) != part[k].end()) {
          if (std::find(lambda.begin(), lambda.end(), k) != lambda.end()) {
          } else {
            cost++;
            // std::cout << "cost increased" << std::endl;
            lambda.push_back(k);
          }
          break;
      }

      }
    }
  }

  std::cout << "Cost = " << cost - graph.num_rows << std::endl;

}

int main(int argc, char* argv[]) {
  if (argc < 2) {
    std::cerr << "Please provide .mtx file (e.g. $ ./a.out ../../../HYPER_PUBLIC/bcsstk21.mtx)" << std::endl;
    return 0;
  }
  // std::unique_ptr<double[]> matrix;
  // std::tie(num_row, num_col, matrix) = mtx2matrix(argv[1]);

  Hypergraph graph;

  std::vector<std::vector<double>> hmetis;
  mtx2matrix(argv[1], graph);
  int num_rows = graph.num_rows;
  int num_cols = graph.num_cols;
  int num_nodes = graph.num_nodes;

  // graph.print_edges();

  // Print out matrix; rows = hyperedges, cols = vertices
  /* for (int row = 0; row < num_row; row++) {
     for (int col = 0; col < num_col; col++) {
       std::cout << matrix[row + col * num_row] << " ";
     }
     std::cout << std::endl;
   }*/

  std::cout << "Num Edges (rows): " << num_rows << ";  Num Vertices (cols): " << num_cols << "; Num nodes (lines): " << num_nodes << std::endl;

  int num_partitions = 2;
  double epsilon = 0.2;
  int condition = compute_condition(num_cols, num_partitions, epsilon);

  std::cout << "Clusters can have at most " << condition << " vertices!" << std::endl;

  std::vector<std::vector<int>> part(num_partitions); 

  random_partitions(part, num_partitions, num_cols, condition);
  compute_connectivity(part, graph);

  // for (int i = 0; i < num_partitions; i++) {
  //   std::cout << "\nCluster " << i << " has " << part[i].size() << " vertices" << std::endl;
  //   for (auto j : part[i]) {
  //     std::cout << j << " ";
  //   }
  //   std::cout << std::endl;
  // }



}