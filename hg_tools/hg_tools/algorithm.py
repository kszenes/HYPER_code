"""Main module."""

import numpy as np
from numpy.random import shuffle
from scipy.sparse import coo_matrix

from hg_tools.io import Partition


def your_awesome_partitioner(
    m: coo_matrix, k: int, epsilon: float  # noqa
) -> Partition:
    """Here you can define your awesome hypegraph partitioner

    Parameters
    ----------
    m : scipy.sparse.coo_matrix
        Hypergraph represented as a sparse matrix.
    k : int
        Size of partition to be returned
    epsilon : float
        Imbalance ratio, i.e., all partition element must have size  at most (1+epsilon)* |V| / k
        where V is the vertex-set

    Returns
    -------
    Partition
        A `Partition` object
    """
    m_csr = m.tocsr()
    num_vertices, num_edges = m.shape;
    max_partition_size = (1 + epsilon) * num_vertices / k

    vertex_partitioned_flag = np.ones(num_vertices, dtype=bool)
    edge_partitioned_flag = np.ones(num_edges, dtype=bool)


    edge_degree = m_csr.sum(axis=0).flatten() # degree of edges
    edge_indices_sorted = np.flip(edge_degree.argsort()) # sort edges; largest first

    current_largest_sorted_edge_index = 0
    current_largest_unsorted_edge_index = edge_indices_sorted[0, current_largest_sorted_edge_index]
    partition_list = []
    part = np.empty(0, dtype=int) # needed placeholder
    current_partition_space = max_partition_size

    print(m_csr.toarray(), '\n')

    while True:
        tmp = m_csr[:, current_largest_unsorted_edge_index].nonzero()[0]
        current_largest_edge_array = tmp[vertex_partitioned_flag[tmp] == True]
        # current_largest_edge_array = m_csr[:, current_largest_unsorted_edge_index].nonzero()[0]
        diff = np.unique(np.concatenate((part, current_largest_edge_array), axis=None, dtype=int))

        print(f'current partition space = {current_partition_space}')

        # if the whole edge fits into the partition
        if diff.shape[0] <= current_partition_space:
            part = np.concatenate((part, diff), axis=None)
            vertex_partitioned_flag[diff] = 0
            edge_partitioned_flag[current_largest_unsorted_edge_index] = 0
            current_partition_space = max_partition_size - part.shape[0]

            # increment the largest edge index if not arrived at the end
            if current_largest_sorted_edge_index + 1 < num_edges:
                current_largest_sorted_edge_index = current_largest_sorted_edge_index + 1
                current_largest_unsorted_edge_index = edge_indices_sorted[0, current_largest_sorted_edge_index]

            else:
                break

        # else put as much as does fit hence filling partition and create new one
        else:
            rounded_space = int(current_partition_space)
            part = np.concatenate((part, diff[:rounded_space]), axis=None)
            vertex_partitioned_flag[diff[:rounded_space]] = 0
            # print(vertex_partitioned_flag)
            partition_list.append(set(part))
            print(partition_list)

            # create new part
            part = np.empty(0, dtype=int)
            current_partition_space = max_partition_size

            if vertex_partitioned_flag.sum() == 0:
                break


    print(partition_list)
    return Partition(num_vertices, k, partition_list)


def random_partitioner(m: coo_matrix, k: int, epsilon: float) -> Partition:  # noqa
    """Uniformly at random partitioner with almost equal size

    Parameters
    ----------
    m : scipy.sparse.coo_matrix
        Hypergraph represented as a sparse matrix.
    k : int
        Size of partition to be returned
    epsilon : float
        Imbalance ratio, i.e., all partition element must have size  at most (1+epsilon)* |V| / k
        where V is the vertex-set

    Returns
    -------
    Partition
        A `Partition` object
    """
    # Represent the vertex set with {0, 1, 2, ... , num_vertices} set
    num_vertices = m.shape[1]
    vertex_set = np.array(range(0, num_vertices))

    shuffle(vertex_set)
    partition = np.array_split(vertex_set, k)
    partition = [set(part) for part in partition]
    return Partition(num_vertices, k, partition)
