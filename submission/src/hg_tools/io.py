"""Input/output module."""

from typing import List, Set

import numpy as np
from scipy.io import mmread, mmwrite
from scipy.sparse import coo_matrix


def read_hypergraph(mtx_filename: str):
    return mmread(mtx_filename)


class Partition:
    """A hypergraph partition writer."""

    def __init__(self, num_vertices: int, k: int, partition: List[Set[int]]):
        self.num_vertices = num_vertices
        self.k = k
        self.partition = partition

    def is_balanced(self, epsilon: float) -> bool:
        """Returns true if the partition is balanced.

        Parameters
        ----------
        epsilon : float
            Imbalance ratio

        Returns
        -------
        bool
            True iff partition is balanced
        """

        # Return true if all element of partition are epsilon-balanced
        # added <= instead of < since that's the definition of balanced according to PaToh!
        avg_size = self.num_vertices / self.k
        return all(len(part) <= (1 + epsilon) * avg_size for part in self.partition)

    @staticmethod
    def read(filename: str):
        """Read Partition from Market Matrix format."""
        m = mmread(filename)
        num_vertices, k = m.shape

        part_set = []
        for part_id in range(k):
            part_set.append(set(m.row[m.col == part_id]))

        return Partition(num_vertices, k, part_set)

    def write(self, filename: str):
        """Writes partition to file

        Parameters
        ----------
        filename : str
            Filename to persist partition as a Matrix Market format
        """
        # Number of non-zeros
        nnz = sum(len(part) for part in self.partition)

        # Hacky code to convert List[Set[int]] partition representation
        # to coo_matrix
        row, col = np.zeros(nnz), np.zeros(nnz)
        data = np.ones(nnz)
        idx = 0
        for part_id, part_element in enumerate(self.partition):
            # For each element of the partition
            for item in part_element:
                row[idx] = item
                col[idx] = part_id
                idx += 1

        matrix = coo_matrix(
            (data, (row, col)), shape=(self.num_vertices, self.k), dtype=np.int8
        )

        # write partition to matrix market format
        mmwrite(filename, matrix, field="pattern")
