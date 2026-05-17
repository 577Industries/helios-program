# HELIOS Fusion Engine — Pre-Registration

**File this on the Open Science Framework BEFORE running hold-out evaluation on Table 3-1.**
**The OSF URL must be present in `orchestration/osf_preregistration.url` for the kill-gate runner to proceed.**

---

## 1. Title

Pre-registered validation of the HELIOS fusion engine: Bayesian Model Averaging with isotonic-regression reliability calibration and conformal prediction across SEP Scoreboards A/B/C for NASA mission-operations all-clear revocation forecasting.

## 2. Investigators

- Thomas Waweru, Principal Investigator, 577 Industries Inc.
- [Senior ML Engineer name]
- [Space-Weather / Ionospheric Physics SME name]

## 3. Pre-registration date and version

- Date filed (UTC ISO 8601): **TO_BE_FILLED_AT_FILING_TIME**
- OSF DOI: **TO_BE_FILLED_AT_FILING_TIME**
- This template version: 1.0

## 4. Hypotheses

We pre-register the following directional hypotheses:

**H1**: Fused all-clear-revocation HSS on the held-out events exceeds the HSS of the best single component model on the same hold-out events by at least 15% (relative).

**H2**: Reliability-diagram slope (linear regression of observed vs. predicted probability) is within 0.15 of 1.0 across all three Kp severity strata (quiet: Kp 0-3; moderate: Kp 4-6; extreme: Kp 7-9).

**H3** (secondary, not gate-determining): Fused Brier score and CRPS on the held-out events improve over the best single component model on the same hold-out events.

## 5. Data

**Training events** (locked, no augmentation, no resampling outside SMOTE within training):

1. Bastille Day — 2000-07-14
2. Halloween storms — 2003-10-28 through 2003-11-04
3. Mid-cycle 23 — 2005-01-20
4. Late cycle 23 — 2006-12-13
5. Cycle 24 onset — 2012-03-07
6. Cycle 24 mid — 2012-05-17
7. September 2017 storm — 2017-09-06 and 2017-09-10

**Hold-out events** (locked, sealed until after model freeze and OSF filing confirmation):

1. Cycle 25 onset — 2022-01-20 (M5.5)
2. Mid-cycle 25 — 2023-02-17 (X2.2)
3. Gannon — 2024-05-11 (G5)

**Component models** (the BMA averages across these; "best component" baseline is whichever individual model scores highest on the hold-out by HSS, computed identically):

- UMASEP
- HESPERIA REleASE
- SEPMOD
- MagPy
- SEP Scoreboard A (consensus onset probability)
- SEP Scoreboard B (consensus peak flux prediction)
- SEP Scoreboard C (event time profile)

All component-model outputs are pulled from public sources via [`helios-spaceweather-connectors`](https://github.com/577-Industries/helios-spaceweather-connectors). No reprocessing; if a component model's output is unavailable for a given event, that component is excluded from BMA *for that event only*, with the exclusion recorded.

## 6. Metrics

Computed per CCMC's standard validation conventions [11, 13]:

- **HSS** (Heidke Skill Score) — primary metric for H1
- **Reliability-diagram slope** — primary metric for H2
- **Brier score** — secondary
- **CRPS** (continuous ranked probability score) — secondary
- **TSS** (True Skill Statistic) — reported
- **POD** (Probability of Detection) — reported
- **FAR** (False Alarm Ratio) — reported

All metrics report point estimates and **bootstrapped 95% confidence intervals** (1000 resamples with replacement over hold-out event-windows).

## 7. Severity strata

Kp-binned at the time of the prediction window:

- **Quiet**: Kp 0-3
- **Moderate**: Kp 4-6
- **Extreme**: Kp 7-9

All metrics are reported per-stratum AND aggregated.

## 8. Pre-registration discipline

- Model freeze date (date after which no hyperparameter changes, feature additions, or architecture revisions are permitted before hold-out evaluation): **TO_BE_FILLED**
- Hold-out evaluation date: **TO_BE_FILLED** (must be after OSF filing date)
- All code at evaluation time is tagged with git commit SHA `TO_BE_FILLED` in the `helios-fusion-engine` repo.
- The `orchestration/kill_gate.py` script's output is committed to `helios-program/results/<date>-killgate.json` and is the **single source of truth** for whether the kill-gate passed.

## 9. Decision rules

Computed AFTER hold-out evaluation; no post-hoc re-baselining.

- **PASS both H1 and H2** → file full arXiv preprint to astro-ph.SR with cs.LG cross-list. Companion footnote in `companion.md` populated with arXiv URL within 7 days of submission.
- **PASS one, FAIL one** → file an "honest ablation" preprint reporting the failing dimension, with explicit pre-registration reference. Useful for the community even though it isn't the headline result.
- **FAIL both** → do not publish. Ship `helios-fusion-engine` v0.1.0 with the negative result documented in a notebook and a clearly-labeled section of the README.

Deviations from the pre-registration (e.g., a component model becomes unavailable, a hold-out event is rescoped due to data-availability issues) are documented as deviations in the final report; they are not retroactive corrections to the pre-registration.

## 10. References

[11] Whitman, K. et al., *Tools Used in Space Radiation Operations*, NASA Technical Reports (2023).
[13] Whitman, K. et al., *NASA's Ongoing SEP Model Validation Effort Driving an Effective R2O2R Process*, COSPAR (2024).
[31] Vovk, V., Gammerman, A., Shafer, G., *Algorithmic Learning in a Random World (Conformal Prediction)*, 2nd ed., Springer (2022).

---

**This template is the starting point. Before filing on OSF**:
1. Fill in TO_BE_FILLED fields
2. Confirm component-model list against actual data availability per `helios-spaceweather-connectors` adapters at the time
3. Have the SME consultant review the metric definitions
4. File. Save the OSF DOI/URL to `orchestration/osf_preregistration.url`.
5. Tag the helios-fusion-engine repo with `prereg-v1.0` at the locked commit.

Only then does the kill-gate runner permit invocation.
