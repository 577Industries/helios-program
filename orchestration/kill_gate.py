"""Execute the pre-registered HELIOS fusion-engine kill-gate.

Per the master plan §C (Decisions Locked), the kill-gate is:

  1. Fused all-clear-revocation HSS on the 3-event hold-out beats the
     best-component-model HSS by >= 15%.
     Hold-out events (frozen):
       - 2022-01-20  Cycle 25 onset (M5.5)
       - 2023-02-17  Mid-cycle 25 (X2.2)
       - 2024-05-11  Gannon (G5)
  2. Reliability-diagram slope is within 0.15 of 1.0 across all three
     Kp severity strata (quiet / moderate / extreme).

Outcomes:
  - PASS both          -> full arXiv paper
  - PASS one, FAIL one -> ablation paper (honest negative result)
  - FAIL both          -> no paper; framework ships with a notebook
                          documenting the negative result

The OSF pre-registration MUST be timestamped before this script runs on
the hold-out events. The CI workflow that ships this file verifies the
OSF registration URL is present in `helios-program/orchestration/osf_preregistration.txt`
and refuses to run otherwise.

Implementation deferred to the helios-fusion-engine build phase. This file
is a placeholder so consumers can `from orchestration.kill_gate import run`.
"""
from __future__ import annotations

from pathlib import Path

HOLDOUT_EVENTS = [
    "2022-01-20",  # Cycle 25 onset (M5.5)
    "2023-02-17",  # Mid-cycle 25 (X2.2)
    "2024-05-11",  # Gannon (G5)
]

SEVERITY_STRATA = ["quiet", "moderate", "extreme"]

HSS_RELATIVE_IMPROVEMENT_THRESHOLD = 0.15  # 15% relative improvement required
RELIABILITY_SLOPE_TOLERANCE = 0.15         # |slope - 1| <= 0.15 in every stratum


def run() -> dict[str, object]:
    """Execute the kill-gate evaluation and return a structured result.

    Implementation in Sprint C-K1 (kill-gate execution day). For now, raises
    to make accidental early invocation loud.
    """
    raise NotImplementedError(
        "Kill-gate execution is deferred to helios-fusion-engine Sprint C-K1. "
        "Filing OSF pre-registration must happen first; see master plan §C."
    )


if __name__ == "__main__":
    result = run()
    print(result)
