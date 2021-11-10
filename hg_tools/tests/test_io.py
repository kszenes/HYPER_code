from hg_tools.io import read_hypergraph
from hg_tools.algorithm import random_partitioner


_SAMPLE_FILE = "data/sample.mtx"


def test_read_hypergraph():
    matrix = read_hypergraph(_SAMPLE_FILE)

    assert matrix.shape == (4, 5), "Shape of matrix must match"


def test_read_hypergraph_element():
    matrix = read_hypergraph(_SAMPLE_FILE)

    assert matrix.tolil()[3, 4] == 1, "Element (3, 4) must equal to one"


def test_random_partition_is_one_balanced():
    hypegraph = read_hypergraph(_SAMPLE_FILE)
    epsilon = 1.0
    partition = random_partitioner(hypegraph, 2, epsilon)

    assert partition.is_balanced(epsilon), "Partition must be balanced"


def test_partition_is_not_perfectly_balanced():
    hypegraph = read_hypergraph(_SAMPLE_FILE)
    epsilon = 0.001
    partition = random_partitioner(hypegraph, 2, epsilon)

    assert not partition.is_balanced(epsilon), f"Partition less than {epsilon}-balanced"
