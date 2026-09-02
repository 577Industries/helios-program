# Sprint D — Kill-Gate Execution Dispatch Spec

**Type**: forward-looking dispatch spec (not a review pack of completed work).
**Status**: ready to dispatch when prerequisites met.
**Estimated agent runtime**: 2-4 hours (mostly real-data fetch + bootstrap CI computation).

---

## TL;DR

Sprint D executes the pre-registered kill-gate evaluation on the 3-event hold-out (Cycle 25 onset 2022-01-20 M5.5; Mid-cycle 25 2023-02-17 X2.2; Gannon 2024-05-11 G5). Outcome determines paper-vs-ablation-vs-no-paper per master plan §"Per-Artifact Briefs → C — `helios-fusion-engine`".

**This sprint produces the headline Phase II result.** Every hold-out event post-dates ISWA's January 2017 cutover (per the Sprint C-Training-v2 coverage matrix) — so the evaluation runs against fully native real-data Scoreboard streams. No synthetic proxies in the final go/no-go.

## Prerequisites — verify ALL before dispatching the agent

| Prereq | How to verify | Status check |
|---|---|---|
| OSF pre-registration filed | `cat ~/577i-Projects/GitHub/577Industries/helios-program/orchestration/osf_preregistration.url` should print a real `https://osf.io/...` URL | Operator action (see [OPERATOR_TODO §3](../OPERATOR_TODO.md)) |
| Methodology note in OSF "Deviations" | The Sprint C-Training-v2 review pack's drafted note (real NOAA SESC truth labels; per-(component, event) source labeling) included before filing | Operator action |
| `helios-fusion-engine` tagged `prereg-v1.0` | `gh release view prereg-v1.0 --repo 577Industries/helios-fusion-engine` returns a release | Operator action |
| `helios-fusion-internal/weights/` v2 artifacts loadable | `python3 -c "from helios_fusion_internal import load_weights; load_weights()"` works | Auto (already true post-Sprint-C-Training-v2) |
| `helios-spaceweather-connectors` v0.2.1+ installable | `pip install 'helios-spaceweather-connectors @ git+https://github.com/577Industries/helios-spaceweather-connectors.git@v0.2.1'` | Auto |
| All 3 hold-out events have real ISWA coverage | Probe via `SepScoreboardsAdapter.fetch` for one timestamp per event window | Pre-flight test in the agent brief |

**Do NOT dispatch the agent until all six rows show ✅.** The kill-gate runner at `orchestration/kill_gate.py` enforces row 1 programmatically (refuses to run without an OSF URL).

## 3 hold-out events (locked per Table 3-1)

| Event | Date | Solar context |
|---|---|---|
| Cycle 25 onset | 2022-01-20 | M5.5 flare; tests cycle-25 distribution shift |
| Mid-cycle 25 | 2023-02-17 | X2.2 flare; mid-cycle hold-out anchor |
| Gannon (G5) | 2024-05-11 | Largest storm in >20 yr; dual-use anchor event |

All three post-date ISWA's Jan 2017 cutover — full native real-data Scoreboard streams expected.

## Pre-registered metrics (do NOT retune)

From `orchestration/osf_preregistration.template.md` (frozen):

| Hypothesis | Metric | Threshold |
|---|---|---|
| H1 (primary) | HSS Donaldson 1975 of fused all-clear-revocation vs. best individual component model | Fused beats best-component by ≥15% relative on hold-out |
| H2 (primary) | Reliability-diagram slope (OLS of observed-freq vs. predicted-prob) per Kp severity stratum | Slope within 0.15 of 1.0 in all 3 strata (quiet/moderate/extreme) |
| H3 (secondary) | Brier score; CRPS | Fused improves over best-component (no threshold; informational) |

All metrics report point estimates AND **bootstrapped 95% confidence intervals** (1000 resamples with replacement over hold-out event-windows). The HSS implementation in `helios_fusion.eval.metrics.hss` already does this.

## Agent brief sketch

The dispatch agent should:

1. **Set up isolated worktree** on `helios-fusion-engine`:
   ```bash
   cd ~/577i-Projects/helios-fusion-engine
   git worktree add -b feat/sprint-d-kill-gate \
     ~/577i-Projects/.worktrees/helios-fusion-engine-killgate origin/main
   ```
2. **Install pinned deps** (commit-SHA-locked per pre-reg):
   ```bash
   pip install -e '.[dev]'
   pip install 'helios-spaceweather-connectors @ git+https://github.com/577Industries/helios-spaceweather-connectors.git@v0.2.1'
   pip install 'helios-provenance-spec @ git+https://github.com/577Industries/helios-provenance-spec.git@v0.1.0'
   ```
3. **Pre-flight verification**:
   - Confirm `orchestration/osf_preregistration.url` is non-empty (the runner's existing check)
   - Probe `SepScoreboardsAdapter.fetch_scoreboard_a` for one timestamp per hold-out event; assert at least one real-data record returned per event
   - Confirm `helios-fusion-internal/weights/manifest.json` `training_runs[-1].fusion_engine_version` matches the locked commit
4. **Execute** `python -m orchestration.kill_gate` (the existing stub gets implementation; pulls weights + connector data + computes metrics + emits JSON)
5. **Persist outputs**:
   - `helios-program/results/<YYYY-MM-DD>-killgate.json` — primary
   - `helios-program/results/<YYYY-MM-DD>-killgate-reliability-diagrams.png` — per-Kp-stratum reliability diagrams (3 panels)
   - `helios-program/results/<YYYY-MM-DD>-killgate-bootstrap-distributions.png` — HSS/Brier/CRPS bootstrap distributions
6. **Decision routing** based on H1, H2 outcomes (see master plan §C):
   - **PASS H1 ∧ PASS H2** → write `results/<date>-decision.md` declaring "full arXiv preprint"; trigger `specs/2026-05-18-arXiv-preprint-draft-spec.md` results fill-in (one commit on the paper branch)
   - **PASS one ∧ FAIL one** → declare "honest ablation paper"; trigger arXiv draft's ablation variant
   - **FAIL both** → declare "no paper"; ship `helios-fusion-engine` v0.2.0 with negative-result notebook and a clearly labeled README section
7. **Update**:
   - `companion/footnotes.yaml` (fusion_engine.preprint URL OR negative-result notebook URL; osf_preregistration URL)
   - `companion/companion.md` artifact-registry status (fusion-engine → "stable" if PASS or "honest-ablation" or "negative-result-shipped")
   - `plan/master-plan.md` execution log
8. **Branch policy**: commits land on `feat/sprint-d-kill-gate` in fusion-engine worktree; the runner's output files land directly on `helios-program/main`. Operator reviews + merges + tags `helios-fusion-engine` accordingly.

## What the agent must NOT do

- Do **not** retune any pre-registered hyperparameter (BMA weight-update formula; isotonic-on-Platt-rejection; Mondrian per Kp stratum; HSS Donaldson 1975 formula).
- Do **not** modify the hold-out event list (3-event set is frozen).
- Do **not** drop a component model from BMA without recording the exclusion in `results/<date>-killgate.json` `deviations[]`.
- Do **not** publish the arXiv preprint — that's a separate Sprint after operator review of the kill-gate result.
- Do **not** push the `feat/sprint-d-kill-gate` branch — operator merges.

## Decision-tree post-conditions

Each branch has explicit downstream actions:

### PASS H1 ∧ PASS H2 → full arXiv paper
1. `feat/sprint-d-kill-gate` branch tagged `prereg-v1.0-passed` after operator merge.
2. Dispatch arXiv preprint agent per `specs/2026-05-18-arXiv-preprint-draft-spec.md` — fill in §4 results from `results/<date>-killgate.json`.
3. Submit to arXiv `astro-ph.SR` with `cs.LG` cross-list within 7 days.
4. Companion footnote `fusion_engine.preprint` populated within 7 days.

### PASS one ∧ FAIL one → honest-ablation paper
1. `feat/sprint-d-kill-gate` branch tagged `prereg-v1.0-partial` after operator merge.
2. Dispatch arXiv preprint agent (ablation variant) — §4 results document the failing dimension; §5 discussion analyzes the failure mode honestly.
3. This is **still valuable** for the community — demonstrates pre-registration discipline.

### FAIL H1 ∧ FAIL H2 → no paper
1. `feat/sprint-d-kill-gate` branch tagged `prereg-v1.0-negative` after operator merge.
2. Ship `helios-fusion-engine` v0.2.0 with:
   - A clearly labeled README section titled "Pre-registered hold-out evaluation: negative result"
   - `notebooks/03-killgate-negative-result.ipynb` reproducing the metrics
   - Companion footnote `fusion_engine.preprint = null` with a `negative_result_notebook` URL
3. **No paper submission.** Honest disclosure protects credibility for Phase II.

## Files to be created / modified

| Path | Action |
|---|---|
| `orchestration/kill_gate.py` | Implementation (currently stub raises NotImplementedError) |
| `~/577i-Projects/.worktrees/helios-fusion-engine-killgate/` | NEW worktree for the dispatch |
| `~/577i-Projects/GitHub/577Industries/helios-program/results/<date>-killgate.json` | NEW (primary output) |
| `~/577i-Projects/GitHub/577Industries/helios-program/results/<date>-killgate-{reliability-diagrams,bootstrap-distributions}.png` | NEW |
| `~/577i-Projects/GitHub/577Industries/helios-program/results/<date>-decision.md` | NEW (branch-routing rationale) |
| `~/577i-Projects/GitHub/577Industries/helios-program/companion/footnotes.yaml` | Edit (fusion_engine.preprint URL or negative-result URL) |
| `~/577i-Projects/GitHub/577Industries/helios-program/companion/companion.md` | Edit (status table; potentially refresh innovation #1 wording) |
| `~/577i-Projects/GitHub/577Industries/helios-program/plan/master-plan.md` | Append execution-log entry |

## Verification gates (pre-merge)

1. `results/<date>-killgate.json` validates against a JSON Schema describing the OSF-pre-registered shape (HSS, reliability slope, Brier, CRPS per stratum + aggregate + 95% CIs).
2. Reliability diagrams render correctly per Kp stratum.
3. Bootstrap distributions have n=1000 resamples.
4. `helios-program/orchestration/companion_sync.py --check` exits 0.
5. The decision-routing rationale at `results/<date>-decision.md` is internally consistent with the JSON metrics.

## Cross-references

- Master plan §C (Per-Artifact Briefs → C, kill-gate decision tree)
- `orchestration/osf_preregistration.template.md` (frozen pre-reg metrics)
- `specs/2026-05-17-Sprint-C-Training-v2-review-pack.md` (training-time methodology + Deviations note)
- `specs/2026-05-18-arXiv-preprint-draft-spec.md` (downstream paper sprint)
- `OPERATOR_TODO.md §3` (OSF filing — the gating prerequisite)
