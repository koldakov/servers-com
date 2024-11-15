# Servers test task

https://servers.com tech task.

## Description

You're given a set of unstructured data (key -> value),
where key is a node of the graph and the value is the connected to this node next node.

You need:
- generate random data (~100 records total), where 80% of node connected to more than one other node,
- build a graph,
- represent it graphically.

## Getting Started

### Requirements

* Python3.12

### Installation

* `git clone git@github.com:koldakov/servers-com.git && cd servers-com`
* Install [poetry](https://python-poetry.org/)
* `poetry install`

### Installation (without poetry)

* `git clone git@github.com:koldakov/servers-com.git && cd servers-com`
* `python3 -m venv .venv`
* `source .venv/bin/activate`
* `pip install .`

### Usage

* To run with poetry run `poetry run python -m servers_com`
* To run without poetry activate virtual env with `source .venv/bin/activate`
and run with `python -m servers_com`

For detailed information run `poetry run python -m servers_com --help` or
`python -m servers_com --help` with activated environment.

#### Development

* `poetry run pre-commit install`

#### Testing

* `poetry run pytest`

## Help

Issue tracker: https://github.com/koldakov/servers-com/issues.
