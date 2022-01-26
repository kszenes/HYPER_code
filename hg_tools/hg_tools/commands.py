from pathlib import Path

import click
import os
import numpy as np

from hg_tools.algorithm import random_partitioner, your_awesome_partitioner
from hg_tools.io import Partition, read_hypergraph
from hg_tools.evaluate import (
    calculate_load_imbalance,
    calculate_communication_volume,
)
from numpy import partition


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
    #partition = random_partitioner(hg_coo_matrix, k, epsilon)
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

@click.command()
@click.argument(
    "hg-folder-name", type=click.Path(), required=True
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
def quality(hg_folder_name, k, epsilon):
    """Compute the quality score with respect to the graphs in the given folder (size K that is epsilon-balanced)."""
    click.echo("*********************************************************************")
    click.echo("* Hypergraph partitioner")
    click.echo(f"* Hypergraph folder           : {hg_folder_name}")
    click.echo(f"* Size of partition (K)     : {k}")
    click.echo(f"* Imbalance ratio (epsilon) : {epsilon}")
    click.echo("*********************************************************************")

    cost = 0.0

    directory = os.fsencode(hg_folder_name)

    #go through every files in the directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".mtx"): 

            filen = click.format_filename(hg_folder_name + filename)
            graph_name = Path(filen).stem

            print(f"Reading file {filen}...")
            hg_coo_matrix = read_hypergraph(filen)

            print("Run partitioner")
            partition_random = random_partitioner(hg_coo_matrix, k, epsilon)
            partition_awesome = your_awesome_partitioner(hg_coo_matrix, k, epsilon)

            C_random = calculate_communication_volume(partition_random,hg_coo_matrix)
            C_awesome = calculate_communication_volume(partition_awesome,hg_coo_matrix)

            cost += np.log(C_random/C_awesome)
            print(f"Current cost : {cost} \n")
    
    print(f"Total cost : {cost}")

    return 0
