#!/usr/bin/env bash
# Verifies fork packaging invariants. Exits non-zero on any violation.
set -euo pipefail
fail=0

# This script checks only OUR OWN invariants — the ones no standard tool covers:
# the distribution name, the import-package name, and the NOTICE. It deliberately
# does NOT try to detect direct-URL (git+) dependencies: those are VALID per
# PEP 508/440, so no standard tool flags them, and a regex of pyproject.toml is
# the wrong instrument. URL-dep enforcement is delegated to (1) tools/verify_wheel.py,
# which scans the BUILT wheel's Requires-Dist with the `packaging` library — the
# exact metadata PyPI sees — and (2) the TestPyPI upload, which is the authoritative
# server-side gate (PyPI rejects URL deps with HTTP 400).

name=$(grep -E '^\s*name\s*=' pyproject.toml | head -1)
echo "$name" | grep -q '"marqov-quantumflow"' || { echo "FAIL: distribution name is not marqov-quantumflow ($name)"; fail=1; }

# Import package must remain 'quantumflow'
grep -qE 'packages\s*=\s*\["quantumflow"\]' pyproject.toml || { echo "FAIL: import package is not quantumflow"; fail=1; }

# NOTICE must exist and name the upstream
test -f NOTICE && grep -q "gecrooks/quantumflow" NOTICE || { echo "FAIL: NOTICE missing or does not reference upstream"; fail=1; }

exit $fail
