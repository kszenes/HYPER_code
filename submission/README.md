# Running code

The implementation is built on top of the python skeleton that was provided in the repository. Therefore, we have only modified the function your awesome partitioner. Our code does not rely on any additional packages and hence the package can be installed and run using the same commands as the ones you have outlined in the README.md that you have provided (you can find a copy of it in the src directory)

# Algorithm

The heuristic that we use for our algorithm is to try and put vertices pertaining to the same net into the same partition. We start by adding the largest nets into a partition until the partition has reached its maximum size determined by the $\epsilon$-balanced condition. Once a partition is completely filled, we move to the next partition. Nets can also be only partially attributed to a single partition in the case that the whole net does not fit into the current partition.