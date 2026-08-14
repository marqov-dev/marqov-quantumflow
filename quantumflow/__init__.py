# Copyright 2020-, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.


# Design Notes:
#
# We import the entire public interface to the top level so that users
# don't need to know the internal package layout.
# e.g. `from quantumflow import something`
# or `import quantumflow as qf; qf.something`
#
# We don't include `.utils` since those are internal utility routines.
#
# Submodules for interfacing with external resources (e.g. .xcirq, .xforest, etc.)
# are not imported at top level, since they have external dependencies that
# often break, and need not be installed by default.
#
# We use a star import here (which necessitates suppressing lint messages)
# so that the public API can be specified in the individual submodules.
# Each of these submodules should define __all__.
#
#
# Import hierarchy:
#
#   utils
#   config
#   tensors
#   var
#   qubits
#   states
#   paulialgebra
#   ops
#   gates
#   stdgates
#   channels
#   stdops
#   circuits
#   dagcircuit
#   gatesets
#   decompositions
#   gradients
#   info
#   transform
#   translate
#   visualization
#   deprecated
#   transpile
#   ext


# Fork guard: the marqov-quantumflow distribution installs this same top-level
# "quantumflow" package as upstream's quantumflow distribution. pip performs no
# file-conflict detection, so if BOTH distributions are installed the second
# silently overwrites the first and the survivor is half-broken. Detect that
# state and warn. Two targeted metadata lookups — not a scan of all installed
# distributions — so the import-time cost is negligible.


def _warn_if_upstream_coinstalled() -> None:
    import importlib.metadata
    import warnings

    try:
        importlib.metadata.version("quantumflow")
        importlib.metadata.version("marqov-quantumflow")
    except importlib.metadata.PackageNotFoundError:
        return  # zero or one distribution present: healthy
    warnings.warn(
        "Both 'marqov-quantumflow' and upstream 'quantumflow' distributions are "
        "installed in this environment. They provide the same top-level "
        "'quantumflow' package and overwrite each other's files. Uninstall both "
        "('pip uninstall quantumflow marqov-quantumflow') and reinstall exactly "
        "one.",
        RuntimeWarning,
        stacklevel=2,
    )


_warn_if_upstream_coinstalled()
del _warn_if_upstream_coinstalled


from .channels import *
from .circuits import *
from .config import *
from .dagcircuit import *
from .decompositions import *
from .deprecated import *
from .gates import *
from .gatesets import *
from .gradients import *
from .info import *
from .ops import *
from .paulialgebra import *
from .qubits import *
from .states import *
from .stdgates import *
from .stdops import *
from .tensors import *
from .transform import *
from .translate import *
from .transpile import *
from .var import *
from .visualization import *
from .xbraket import *
from .xcirq import *
from .xforest import *
from .xqiskit import *
from .xqsim import *
from .xquirk import *
from .xqutip import *

# fin
