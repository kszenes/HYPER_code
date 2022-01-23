from pathlib import Path

import click

from hg_tools.algorithm import random_partitioner, your_awesome_partitioner
from hg_tools.io import Partition, read_hypergraph
from hg_tools.evaluate import (
    calculate_load_imbalance,
    calculate_communication_volume,
)


@click.command()
@click.argument(
    "hg-filename", type=click.Path(exists=True), required=True
)
# @click.option(
#     "hg-filename", type=click.Path(exists=True), required=True, default=Path("/Users/kalmanszenes/code/HYPER_code/HYPER_PUBLIC/bcsstk21.mtx")
# )
@click.option("--K", type=int, help="Size of partition", required=True, default=2)
@click.option(
    "--epsilon",
    type=float,
    default=0.05,
    required=True,
    help="Imbalanced ratio (epsilon)",
)
def split(hg_filename, k, epsilon):
    """Hypergraph partitioner that returns a partition of size K that is epsilon-balanced."""
    click.echo("*********************************************************************")
    click.echo("* Hypergraph partitioner")
    click.echo(f"* Hypergraph used           : {hg_filename}")
    click.echo(f"* Size of partition (K)     : {k}")
    click.echo(f"* Imbalance ratio (epsilon) : {epsilon}")
    click.echo("*********************************************************************")
    filename = click.format_filename(hg_filename)
    graph_name = Path(filename).stem

    print(f"Reading file {filename}...")
    hg_coo_matrix = read_hypergraph(filename)

    print("Run partitionerer")
    # partition = random_partitioner(hg_coo_matrix, k, epsilon)
    partition = your_awesome_partitioner(hg_coo_matrix, k, epsilon)

    output_file = f"{graph_name}.{k}.output"
    print(f"Write {k}-partition to file: {output_file}.mtx")
    partition.write(f"output/{output_file}")

    return 0


@click.command()
@click.argument(
    "hg-filename", type=click.Path(exists=True), required=True,
)
@click.argument(
    "partition-filename", type=click.Path(exists=True), required=True,
)
@click.option(
    "--epsilon",
    type=float,
    default=0.05,
    required=True,
    help="Imbalanced ratio (epsilon)",
)
def check(hg_filename, partition_filename, epsilon):
    """Hypergraph partitioner checker.

    It checks if the input partition is balanced and computes its cost.
    """
    click.echo("*********************************************************************")
    click.echo("* Hypergraph partitioner")
    click.echo(f"* Hypergraph file          : {hg_filename}")
    click.echo(f"* Partition file           : {partition_filename}")
    click.echo("*********************************************************************")
    filename = click.format_filename(hg_filename)
    part_filename = click.format_filename(partition_filename)

    print(f"Reading hypergraph from {filename}...")
    hg_coo_matrix = read_hypergraph(filename)

    print(f"Reading partition from {part_filename}...")
    partition = Partition.read(part_filename)

    print("*********************************************************************")
    print(f"* Is input partition {epsilon}-balanced? {partition.is_balanced(epsilon)}")

    imbalance = calculate_load_imbalance(partition)
    print("*********************************************************************")
    print(f"* Partition imbalance : {imbalance}")

    cost = calculate_communication_volume(partition, hg_coo_matrix)
    print("*********************************************************************")
    print(f"* Partition cost : {cost}")
    print("*********************************************************************")

    return 0
