#!/bin/sh

echo "Running paritioning"
echo "Dataset: ${1}"
echo "K: ${2}"
echo "EPSILON: ${3}"

# Run hypegraph partitioner
hg_tools split ${1} --K ${2} --epsilon ${3}
