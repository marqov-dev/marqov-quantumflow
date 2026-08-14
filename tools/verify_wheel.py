"""Install-and-import verification for the marqov-quantumflow wheel.

Run inside a venv that has the built wheel installed, from a NEUTRAL cwd
(e.g. $RUNNER_TEMP), never the repo root. `packaging` is installed explicitly
alongside it (see the install commands) so the import below never relies on a
transitive dependency happening to provide it.

Checks use explicit exits rather than `assert` so they survive `python -O`.
"""
import importlib.metadata as md
import os
import sys
import sysconfig

from packaging.requirements import InvalidRequirement, Requirement  # PEP 508 parser


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


import quantumflow as qf

# 1. Guard against cwd/sys.path shadowing FIRST. If this script is run from the
# repo root, `import quantumflow` resolves to ./quantumflow (the source tree)
# and importlib.metadata reads a local *.egg-info — every check below would
# then verify the SOURCE, not the installed wheel under test. Require that the
# imported package lives in this interpreter's site-packages. commonpath (not a
# string prefix test) so a sibling path like ".../site-packages-other" can't pass.
_site = os.path.realpath(sysconfig.get_paths()["purelib"])
_qf = os.path.realpath(getattr(qf, "__file__", "") or "")
if not _qf or os.path.commonpath([_site, _qf]) != _site:
    fail(
        f"imported quantumflow from {_qf!r}, not site-packages ({_site!r}). "
        "Run verify_wheel.py from a NEUTRAL cwd (e.g. $RUNNER_TEMP), not the "
        "source repo root, so it verifies the INSTALLED package and not the "
        "source tree."
    )

# 2. Distribution name is the fork's
dist = md.distribution("marqov-quantumflow")
if dist.metadata["Name"] != "marqov-quantumflow":
    fail(f"distribution Name is {dist.metadata['Name']!r}, expected 'marqov-quantumflow'")

# 3. No direct-URL dependencies in the RESOLVED metadata (the exact thing PyPI
#    validates). A PEP 508 direct reference is precisely a requirement whose
#    `.url` is non-None — this is the standard, regex-free way to detect them,
#    and it scans the built artifact's Requires-Dist rather than the source TOML.
bad = []
for r in dist.requires or []:
    try:
        if Requirement(r).url is not None:
            bad.append(r)
    except InvalidRequirement:
        bad.append(f"<unparseable: {r}>")
if bad:
    fail(f"direct-URL deps present: {bad}")

# A downstream SDK's QuantumFlow contract has TWO parts.
# 4a. MODULE-LEVEL `qf.*` symbols (17): the gate classes, Circuit, State,
#     transpile, and the two braket interop functions.
module_syms = ["Circuit", "State", "transpile",
               "braket_to_circuit", "circuit_to_braket",
               "CNot", "CZ", "H", "Rx", "Ry", "Rz", "S", "Swap", "T", "X", "Y", "Z"]
missing = [s for s in module_syms if not hasattr(qf, s)]
if missing:
    fail(f"missing module symbols: {missing}")

# 4b. Circuit-INSTANCE members the SDK accesses on a qf.Circuit() object (NOT
#     module functions): `run()`, `qubit_nb`, and the PRIVATE `_elements`
#     (which it iterates directly). `_elements` is genuine fragility — a
#     leading-underscore attribute a fork/upstream bump can remove without
#     deprecation — so we check it explicitly here, where a break surfaces in
#     the fork's gate rather than at SDK runtime.
c = qf.Circuit([qf.H(0), qf.CNot(0, 1), qf.Rz(0.5, 1)])
inst_members = ["run", "qubit_nb", "_elements"]
missing_inst = [m for m in inst_members if not hasattr(c, m)]
if missing_inst:
    fail(f"missing Circuit-instance members: {missing_inst}")

# 5. Functional smoke: exercise exactly what the SDK exercises. An uncaught
#    exception here exits non-zero, which is the point.
c.run()
list(c._elements)        # the private-attr iteration
_ = c.qubit_nb

n = len(module_syms) + len(inst_members)
print(f"OK: marqov-quantumflow {dist.version}, import quantumflow, "
      f"{len(module_syms)} module symbols + {len(inst_members)} Circuit members ({n} total) present")
sys.exit(0)
