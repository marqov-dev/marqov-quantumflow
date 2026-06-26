"""Install-and-import verification for the marqov-quantumflow wheel.

Run inside a venv that has the built wheel installed. `packaging` is installed
explicitly alongside it (see the install commands) so the import below never
relies on a transitive dependency happening to provide it.
"""
import importlib.metadata as md
import sys
from packaging.requirements import Requirement  # standard PEP 508 parser

# 1. Distribution name is the fork's
dist = md.distribution("marqov-quantumflow")
assert dist.metadata["Name"] == "marqov-quantumflow", dist.metadata["Name"]

# 2. No direct-URL dependencies in the RESOLVED metadata (the exact thing PyPI
#    validates). A PEP 508 direct reference is precisely a requirement whose
#    `.url` is non-None — this is the standard, regex-free way to detect them,
#    and it scans the built artifact's Requires-Dist rather than the source TOML.
bad = []
for r in (dist.requires or []):
    try:
        if Requirement(r).url is not None:
            bad.append(r)
    except Exception:
        bad.append(f"<unparseable: {r}>")
assert not bad, f"direct-URL deps present: {bad}"

import quantumflow as qf  # noqa: E402

# Guard against cwd/sys.path shadowing. If this script is run from the repo root,
# `import quantumflow` resolves to ./quantumflow (the source tree) and
# importlib.metadata reads a local *.egg-info — so the check would verify the
# SOURCE, not the installed wheel under test. Require that the imported package
# lives in this interpreter's site-packages.
import os                       # noqa: E402
import sysconfig               # noqa: E402
_site = os.path.realpath(sysconfig.get_paths()["purelib"])
_qf = os.path.realpath(getattr(qf, "__file__", "") or "")
assert _qf.startswith(_site), (
    f"imported quantumflow from {_qf!r}, not site-packages ({_site!r}). "
    "Run verify_wheel.py from a NEUTRAL cwd (e.g. /tmp), not the source repo "
    "root, so it verifies the INSTALLED package and not the source tree."
)

# The SDK's QuantumFlow contract has TWO parts, derived from marqov/circuits.py.
# 3a. MODULE-LEVEL `qf.*` symbols (17): the gate classes, Circuit, State,
#     transpile, and the two braket interop functions.
module_syms = ["Circuit", "State", "transpile",
               "braket_to_circuit", "circuit_to_braket",
               "CNot", "CZ", "H", "Rx", "Ry", "Rz", "S", "Swap", "T", "X", "Y", "Z"]
missing = [s for s in module_syms if not hasattr(qf, s)]
assert not missing, f"missing module symbols: {missing}"

# 3b. Circuit-INSTANCE members the SDK accesses on a qf.Circuit() object (NOT
#     module functions): `run()` (circuits.py:278), `qubit_nb` (743), and the
#     PRIVATE `_elements` (694, iterated as `self._qf._elements`). `_elements`
#     is genuine fragility — a leading-underscore attribute a fork/upstream bump
#     can remove without deprecation — so we assert it explicitly here, where a
#     break surfaces in the fork's gate rather than at SDK runtime. (See notes.)
c = qf.Circuit([qf.H(0), qf.CNot(0, 1), qf.Rz(0.5, 1)])
inst_members = ["run", "qubit_nb", "_elements"]
missing_inst = [m for m in inst_members if not hasattr(c, m)]
assert not missing_inst, f"missing Circuit-instance members: {missing_inst}"

# 4. Functional smoke: exercise exactly what circuits.py does
c.run()                  # circuits.py:278
list(c._elements)        # circuits.py:694 — the private-attr iteration
_ = c.qubit_nb           # circuits.py:743

n = len(module_syms) + len(inst_members)
print(f"OK: marqov-quantumflow {dist.version}, import quantumflow, "
      f"{len(module_syms)} module symbols + {len(inst_members)} Circuit members ({n} total) present")
sys.exit(0)
