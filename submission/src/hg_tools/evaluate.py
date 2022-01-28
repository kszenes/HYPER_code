from hg_tools.io import Partition


def calculate_load_imbalance(partition: Partition) -> float:
    """Returns the load imbalance (epsilon) achieved by the partitioning.

    Parameters
    ----------
    partition : `hg_tools.io.Partition`
        A hypergraph partitioning

    Returns
    -------
    float
        Load imbalance (epsilon)
    """

    avg_size = partition.num_vertices / partition.k
    all_epsilons = [
        max((len(part) - avg_size) / avg_size, 0) for part in partition.partition
    ]
    return max(all_epsilons)


def calculate_communication_volume(partition: Partition, hypergraph) -> float:
    """Returns the communication volume c achieved by a partitioning.

    Parameters
    ----------
    partition : `hg_tools.io.Partition`
        A hypergraph partitioning
    hypergraph : scipy.sparse.coo_matrix
        A hypegraph represented as a coordinate sparse matrix

    Returns
    -------
    float
        The communication volume of the input partition.
    """

    node2part = {}

    for i, part in enumerate(partition.partition):
        for node in part:
            node2part[node] = i
    parts_per_edge = {i: set() for i in range(hypergraph.shape[0])}
    for i, j in zip(hypergraph.row, hypergraph.col):
        part = node2part[j]
        parts_per_edge[i].add(part)
    return sum(
        max(len(list(parts_in_edge)) - 1, 0)
        for parts_in_edge in parts_per_edge.values()
    )
