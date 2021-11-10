FROM python:3.8

LABEL Author="Hyper Challenge Authors"

RUN mkdir /app
COPY docker/entrypoint.sh /
COPY hg_tools /app
WORKDIR /app

# Build
RUN pip install -e .


ENTRYPOINT ["/entrypoint.sh"]

# Run partitioner
#RUN hg_tools split data/sample.mtx --K 2

# Validate partition
#RUN hg_tools check data/sample.mtx sample.2.output.mtx --epsilon 1.0
