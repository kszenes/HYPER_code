# University Challenge 2021

This repository contains:

* The TeX file of the technical write-up describing the University / HYPER Challenge 2021 under `latex-doc/` 
* The Python starter-kit for the competition
* The Docker starter-kit for the competition with the Python starter-kit inside

## Option 1: Hypergraph partitioning using Python

The Python starter-kit is located under `hg_tools/`. Please see the README.md file within that folder for further instructions. 
The partition output file is written under `hg_tools/output/`.

## Option 2: Hypergraph partitioning using Docker 

The following instructions show a reproducible execution of the Docker starter-kit.

#### Dependencies

You must first have installed [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

#### Datasets

You need to copy your datasets under `hg_tools/data/` folder.

### Build and run within a docker container

To build, type

```bash
docker-compose build
```

To run, type

```bash
docker-compose run hg_tools data/sample.mtx 2 0.01
# docker-compose run hg_tools data/CurlCurl_4.mtx.gz 10 0.01
# docker-compose run hg_tools data/wikipedia-20070206.mtx.gz 10 0.01
```

The partition output file is written under `docker-output/`.
