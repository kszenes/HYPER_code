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
