> **Note:** This is `marqov-quantumflow`, a fork of
> [QuantumFlow](https://github.com/gecrooks/quantumflow) (Apache-2.0) maintained
> by Marqov, based on upstream `v1.4.0`. The import package name remains
> `quantumflow`. See `NOTICE` for details.
>
> **Warning:** Do not install `marqov-quantumflow` and upstream `quantumflow`
> in the same environment. Both distributions install the same top-level
> `quantumflow` package; pip performs no file-conflict detection, so the second
> install silently overwrites the first and uninstalling either leaves the
> survivor broken. Install exactly one.

#  QuantumFlow: A Quantum Algorithms Development Toolkit

A cross-compiler for gate based models of quantum computing

[![Build Status](https://github.com/marqov-dev/marqov-quantumflow/actions/workflows/marqov-fork-ci.yml/badge.svg)](https://github.com/marqov-dev/marqov-quantumflow/actions/workflows/marqov-fork-ci.yml) [![Documentation Status](https://readthedocs.org/projects/quantumflow/badge/?version=latest)](https://quantumflow.readthedocs.io/en/latest/?badge=latest) [![PyPi version](https://img.shields.io/pypi/v/marqov-quantumflow?color=brightgreen)](https://pypi.org/project/marqov-quantumflow/)


* [Tutorial](https://github.com/marqov-dev/marqov-quantumflow/tree/main/tutorial)
* [Source Code](https://github.com/marqov-dev/marqov-quantumflow)
* [Issue Tracker](https://github.com/marqov-dev/marqov-quantumflow/issues)
* [API Documentation](https://quantumflow.readthedocs.io/) (upstream)
* [Upstream Project](https://github.com/gecrooks/quantumflow)


## Installation

To install the latest stable release:
```
$ pip install marqov-quantumflow
```

In addition, install all of the external quantum libraries that QuantumFlow can interact with (such as cirq, qiskit, braket, ect.):
```
$ pip install 'marqov-quantumflow[ext]'
```


To install the latest code from github ready for development:
```
$ git clone https://github.com/marqov-dev/marqov-quantumflow.git
$ cd marqov-quantumflow
$ pip install -e '.[dev]'
```


