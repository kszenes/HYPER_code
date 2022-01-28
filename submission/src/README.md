# Hypergraph Partitioner Starter Kit

Starter kit to implement a hypergraph partitioner in Python.

You need to declare all your Python dependencies in the `requirements` variable in `setup.py` 
file. You code must work with at least one of Python 3.{7,8,9}.

You can define your hypegraph partitioner under `hg_tools.algorithm` module, e.g., method `your_awesome_partitioner`.

The Python package is pip installable (see below).

### Development

To install the package locally, you need to clone the repo, move to the `hg_tools/` folder and type

```
pip install -e .
```

## Available Commands

There are two commands available after installation:

* `hg_tools split --help` to partition the input hypegraph.
* `hg_tools check --help` to validate your partitioning.

### Partitioning

To run the random partitioner, type

```bash
hg_tools split data/sample.mtx --K 2
```

should output

```
*********************************************************************
* Hypergraph partitioner
* Hypergraph used           : data/sample.mtx
* Size of partition (K)     : 2
* Imbalance ratio (epsilon) : 1.0
*********************************************************************
Reading file data/sample.mtx...
Run partitioner
Write 2-partition to file: sample.2.output.mtx
```

The above also dumps the output using pickle to a file `output/sample.2.output.mtx`.

### Validate your partition

To validate your output partition, type

```bash
hg_tools check data/sample.mtx output/sample.2.output.mtx --epsilon 0.1
```

should output

```
hg_tools check data/sample.mtx sample.2.output.mtx --epsilon 0.1
*********************************************************************
* Hypergraph partitioner
* Hypergraph file          : data/sample.mtx
* Partition file           : sample.2.output.mtx
*********************************************************************
Reading hypergraph from data/sample.mtx...
Reading partition from sample.2.output.mtx...
*********************************************************************
* Is input partition 0.1-balanced? False
*********************************************************************
* Partition imbalance : 0.2
*********************************************************************
* Partition cost : 2
*********************************************************************
```
You need to first generate a valid partition via `hg_tools split data/sample.mtx --K 2`

### Datasets

The development datasets are listed in the challenge document.



