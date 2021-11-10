from hg_tools.io import read_hypergraph
from hg_tools.algorithm import random_partitioner
from hg_tools.evaluate import (
    calculate_load_imbalance,
    calculate_communication_volume,
)

_SAMPLE_FILE = "data/sample.mtx"


def test_load_imbalance():
    hypegraph = read_hypergraph(_SAMPLE_FILE)
    epsilon = 1.0
    partition = random_partitioner(hypegraph, 2, epsilon)

    eps = calculate_load_imbalance(partition)

    assert eps >= 0, "Load imbalance must be positive"


def test_comm_volume():
    hypegraph = read_hypergraph(_SAMPLE_FILE)
    epsilon = 1.0
    partition = random_partitioner(hypegraph, 2, epsilon)

    cost = calculate_communication_volume(partition, hypegraph)

    assert cost > 0, "Communication volume cost must be positive"
