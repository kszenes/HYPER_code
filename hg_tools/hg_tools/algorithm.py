"""Main module."""

import numpy as np
from numba import njit
import time
from numpy.random import shuffle
from scipy.sparse import coo_matrix,csr_matrix

from hg_tools.io import Partition

def your_awesome_partitioner_jit(
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

    #transpose the matrix so that we can quickly compute the nonzeros columns values in csr format
    m_csr = m.tocsr()
    #needs this computationally ineffecient way to recompute the csr arrays for a sparse matrix
    m_csr_T = csr_matrix(m_csr.toarray().transpose())

    num_vertices, num_edges = m.shape
    max_partition_size = (1 + epsilon) * num_vertices / k

    vertex_partitioned_flag = np.ones(num_vertices, dtype=bool)
    edge_partitioned_flag = np.ones(num_edges, dtype=bool)


    edge_degree = m_csr.sum(axis=0).flatten() # degree of edges
    edge_indices_sorted = np.flip(edge_degree.argsort()) # sort edges; largest first

    current_largest_sorted_edge_index = 0
    current_largest_unsorted_edge_index = edge_indices_sorted[0, current_largest_sorted_edge_index]
    num_partitioned = 0
    current_partition_space = max_partition_size

    print(f'max_partition_size = {max_partition_size}')

    # print(m_csr.toarray(), '\n')

    start = time.perf_counter()
    @njit(cache=True,parallel = True)
    def partition(m_csr_Tindptr, m_csr_Tindices, k, num_partitioned, num_vertices, num_edges, max_partition_size, vertex_partitioned_flag, current_largest_unsorted_edge_index,current_partition_space, current_largest_sorted_edge_index, edge_partitioned_flag, edge_indices_sorted):
        print("IN")
        part = np.empty(0, dtype=np.int64) # needed placeholder
        partition_list = []

        while True:

            # if last partition put remaining vertices in
            if len(partition_list) == k - 1:
                diff = np.argwhere(vertex_partitioned_flag == 1).copy().reshape(-1)
                num_partitioned = num_partitioned + len(diff)
                partition_list.append(diff)
                break
            
            #get row indices of nonzeros values in column
            tmp = m_csr_Tindices[m_csr_Tindptr[current_largest_unsorted_edge_index]:m_csr_Tindptr[current_largest_unsorted_edge_index+1]]
            #tmp = m_csr[:, current_largest_unsorted_edge_index].nonzero()[0] # get vertices pertaining to net
            current_largest_edge_array = tmp[vertex_partitioned_flag[tmp] == 1] # only select unpartitioned vertices

            # diff = np.setdiff1d(current_largest_edge_array, part, assume_unique=True) # find 
            diff = current_largest_edge_array

            # debug
            if len(partition_list) > k or num_partitioned > num_vertices or len(diff) > num_vertices - num_partitioned:
                print(f'num_partitioned = {num_partitioned}')
                print(f'num_partitions = {len(partition_list)}')
                raise Exception('Partition list too large')

            # if the whole edge fits into the partition
            if diff.shape[0] <= current_partition_space:

                l = len(part)
                part_temp = np.zeros(l + len(diff),dtype = np.int64)
                part_temp[:l] = part
                part_temp[l:] = diff
                part = part_temp

                vertex_partitioned_flag[diff] = 0
                edge_partitioned_flag[current_largest_unsorted_edge_index] = 0
                current_partition_space = current_partition_space - diff.shape[0]


                # increment the largest edge index if not arrived at the end
                if current_largest_sorted_edge_index + 1 < num_edges:
                    current_largest_sorted_edge_index = current_largest_sorted_edge_index + 1
                    current_largest_unsorted_edge_index = edge_indices_sorted[0, current_largest_sorted_edge_index]

                else:
                    break

            # else put as much as does fit hence filling partition and create new one
            else:
                rounded_space = int(current_partition_space)

                l = len(part)
                part_temp = np.zeros(l + len(diff[:rounded_space]),dtype = np.int64)
                part_temp[:l] = part
                part_temp[l:] = diff[:rounded_space]
                part = part_temp

                vertex_partitioned_flag[diff[:rounded_space]] = 0
                # print(vertex_partitioned_flag)
                partition_list.append(part)
                num_partitioned = num_partitioned + len(part)
                # print(partition_list)
                print(f'new partition size: {len(part)}; partition_list: {len(partition_list)}; num_partitioned: {num_partitioned}')

                # create new part
                part = np.empty(0, dtype=np.int64)
                current_partition_space = max_partition_size

                # if vertex_partitioned_flag.sum() == 0:
                #     break

        return partition_list, part, num_partitioned

    # print(partition_list)
    # partition_list.append(part)

    partition_list, part, num_partitioned = partition(np.array(m_csr_T.indptr,dtype = np.int64), np.array(m_csr_T.indices,dtype = np.int64), k, num_partitioned, num_vertices, num_edges, 
        max_partition_size, vertex_partitioned_flag, current_largest_unsorted_edge_index, current_partition_space, 
        current_largest_sorted_edge_index, edge_partitioned_flag, edge_indices_sorted)
    
    print(f"Time to partition : {time.perf_counter()-start} s.")
    print(f'num_partitioned = {num_partitioned}')
    partition_list = [set(partitions) for partitions in partition_list]
    print(f'num_partitions = {len(partition_list)}')
    return Partition(num_vertices, k, partition_list)

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
    num_vertices, num_edges = m.shape
    max_partition_size = (1 + epsilon) * num_vertices / k

    vertex_partitioned_flag = np.ones(num_vertices, dtype=bool)
    edge_partitioned_flag = np.ones(num_edges, dtype=bool)


    edge_degree = m_csr.sum(axis=0).flatten() # degree of edges
    edge_indices_sorted = np.flip(edge_degree.argsort()) # sort edges; largest first

    current_largest_sorted_edge_index = 0
    current_largest_unsorted_edge_index = edge_indices_sorted[0, current_largest_sorted_edge_index]
    num_partitioned = 0
    current_partition_space = max_partition_size

    print(f'max_partition_size = {max_partition_size}')

    # print(m_csr.toarray(), '\n')

    start = time.perf_counter()
    #@jit(nopython = True, cache=True)
    def partition(m_csr, k, num_partitioned, num_vertices, num_edges, max_partition_size, vertex_partitioned_flag, 
        current_largest_unsorted_edge_index, current_partition_space, current_largest_sorted_edge_index, edge_partitioned_flag, edge_indices_sorted):

        part = np.empty(0, dtype=int) # needed placeholder
        partition_list = []

        while True:

            # if last partition put remaining vertices in
            if len(partition_list) == k - 1:
                diff = np.argwhere(vertex_partitioned_flag == 1).reshape(-1)
                num_partitioned = num_partitioned + len(diff)
                partition_list.append(diff)
                break

            tmp = m_csr[:, current_largest_unsorted_edge_index].nonzero()[0] # get vertices pertaining to net
            current_largest_edge_array = tmp[vertex_partitioned_flag[tmp] == 1] # only select unpartitioned vertices

            # diff = np.setdiff1d(current_largest_edge_array, part, assume_unique=True) # find 
            diff = current_largest_edge_array



            # debug
            if len(partition_list) > k or num_partitioned > num_vertices or len(diff) > num_vertices - num_partitioned:
                print(f'num_partitioned = {num_partitioned}')
                print(f'num_partitions = {len(partition_list)}')
                raise Exception('Partition list too large')

            # if the whole edge fits into the partition
            if diff.shape[0] <= current_partition_space:
                part = np.concatenate((part, diff), axis=None)
                vertex_partitioned_flag[diff] = 0
                edge_partitioned_flag[current_largest_unsorted_edge_index] = 0
                current_partition_space = current_partition_space - diff.shape[0]


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
                partition_list.append(part)
                num_partitioned = num_partitioned + len(part)
                # print(partition_list)
                print(f'new partition size: {len(part)}; partition_list: {len(partition_list)}; num_partitioned: {num_partitioned}')

                # create new part
                part = np.empty(0, dtype=int)
                current_partition_space = max_partition_size

                # if vertex_partitioned_flag.sum() == 0:
                #     break

        return partition_list, part, num_partitioned

    # print(partition_list)
    # partition_list.append(part)

    partition_list, part, num_partitioned = partition(m_csr, k, num_partitioned, num_vertices, num_edges, max_partition_size, vertex_partitioned_flag, 
        current_largest_unsorted_edge_index, current_partition_space, current_largest_sorted_edge_index, edge_partitioned_flag, edge_indices_sorted)
    
    print(f"Time to partition : {time.perf_counter()-start} s.")
    print(f'num_partitioned = {num_partitioned}')
    partition_list = [set(partitions) for partitions in partition_list]
    print(f'num_partitions = {len(partition_list)}')
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
