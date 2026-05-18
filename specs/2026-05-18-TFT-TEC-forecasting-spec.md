# §2 Objective 2 — TFT for TEC Forecasting Dispatch Spec

**Type**: forward-looking dispatch spec.
**Status**: ready to dispatch when prerequisites met.
**Estimated agent runtime**: 8-16 hours (substantial ML work — multi-step model build + 20+ years of training data + tuning).

---

## TL;DR

Implements the Temporal Fusion Transformer (TFT) for vertical-TEC multi-horizon forecasting per the proposal §2 Objective 4 GNSS slice. TFT consumes 20+ years of CDDIS GIM data + DSCOVR upstream solar wind + SWPC Dst as exogenous variables, predicts TEC at 0-24 hour horizons.

**Why this matters**: this is the second of the proposal's two main ML objectives (§2 Obj 2 BMA-on-SEP is the first; Sprint D evaluates that). When this ships, both proposal objectives have shipped artifacts. Bonus: `gannon-storm-rtk-analysis` v2 swaps its v1 climatological model for real SPP using the TFT-predicted TEC — the headline "1,302 station-hours" claim upgrades from "climatological-v1" to "real-data v2."

## Prerequisites

| Prereq | How to verify | Operator-action? |
|---|---|---|
| `NASA_EARTHDATA_USER` set | `echo $NASA_EARTHDATA_USER` non-empty | Yes ([OPERATOR_TODO §2](../OPERATOR_TODO.md)) |
| `NASA_EARTHDATA_PASS` set | `echo $NASA_EARTHDATA_PASS` non-empty | Yes |
| CDDIS authorized on Earthdata profile | <https://urs.earthdata.nasa.gov/> → Applications → "NASA GESDISC DATA ARCHIVE" approved | Yes |
| ~20 GB disk for the CDDIS cache | `df -h ~/.cache/helios-connectors/cddis/` shows ≥20 GB free | Auto |
| GPU available (recommended) | `nvidia-smi` works; or use AWS GPU instance per proposal §5.2 budget | Operator decides (CPU works but ~10× slower) |
| `helios-spaceweather-connectors` v0.2.1+ has `CddisGimAdapter` exposed | `python3 -c "from helios_connectors import CddisGimAdapter"` works | Auto (already true) |

## Architecture: Temporal Fusion Transformer

Per Lim, Arik, Loeff, Pfister (2021), *International Journal of Forecasting* 37(4):1748-1764 (proposal ref [32]).

| Hyperparameter | Value | Rationale |
|---|---|---|
| Lookback window | 168 hours (1 week) | Captures solar rotation effects + multi-day storm recovery |
| Forecast horizon | 0-24 hours | Spans operator-relevant decision windows |
| Quantile heads | 0.1, 0.5, 0.9 | Conformal-prediction-compatible; matches the BMA fusion engine's interval shape |
| Embedding dim | 128 | Standard for time-series TFT |
| Attention heads | 4 | Same |
| Dropout | 0.1 | Same |
| Optimizer | Adam, LR 1e-3 with cosine schedule | Robust default |
| Batch size | 64 (GPU) / 32 (CPU) | Adjust per hardware |
| Early stopping | Val MAE plateau over 10 epochs | Prevents over-fitting on quiet periods |

## Static + time-varying variables

**Static (per spatial gridpoint)**:
- Geomagnetic latitude (computed from geographic lat at each timestamp via IGRF coefficients)
- Geographic latitude + longitude
- Solar zenith angle bin (proxy for ionospheric responsiveness)

**Time-varying past + future known**:
- Hour of day, day of year (cyclic encodings)
- Solar wind speed, density, IMF Bz from `DscovrAdapter` (past); SWPC 3-day forecast where available (future-known)
- Kp index from `SwpcAdapter` with GFZ Potsdam fallback for pre-2010 (past); SWPC 3-day Kp forecast (future-known)

**Time-varying past only (target)**:
- Vertical TEC at the (lat, lon) grid point from `CddisGimAdapter.fetch_tec_at_point`

## Training data window

- **Training**: 2003-01-01 to 2018-12-31 (16 years; covers Cycle 23 peak through Cycle 24 mid)
- **Validation**: 2019-01-01 to 2020-12-31 (2 years; solar minimum window for low-activity baseline)
- **Hold-out**: 2021-01-01 to 2025-12-31 (5 years; Cycle 25 ramp including Gannon)

**Total training samples**: ~16 years × 365 days × 12 maps/day × selected grid points (e.g., 100 stations + 50 random gridpoints) ≈ 10M samples. Plenty for TFT.

**Cache footprint**: ~24 years × ~50-100 KB per IONEX file (compressed) ≈ 5-10 GB.

## Validation event set

For consistency with the proposal Table 3-1 split AND the proposal §1.3 Gannon anchor:

| Event | Date | Use |
|---|---|---|
| Halloween storms | 2003-10-28 to 2003-11-04 | TRAIN — Cycle 23 peak |
| Sept 2017 storm | 2017-09-06 + 2017-09-10 | TRAIN — bridge cycle |
| Cycle 25 onset | 2022-01-20 | HOLD-OUT (matches Sprint D set) |
| Mid-cycle 25 | 2023-02-17 | HOLD-OUT |
| Gannon | 2024-05-10 to 2024-05-12 | HOLD-OUT (proposal §1.3 anchor) |
| March 2024 (G4) | (date) | HOLD-OUT |
| October 2024 (G3) | (date) | HOLD-OUT |
| February 2024 (G2) | (date) | HOLD-OUT |

The GNSS slice's 4-event hold-out (Gannon + March G4 + October G3 + February G2 per proposal §3.1) maps onto the Cycle-25 hold-out window naturally.

## Quality bar (per proposal §2 Obj. 4 success criterion)

- **TEC MAE ≤ 3 TECU on quiet-period hold-out** (Kp < 4 windows)
- **TEC MAE ≤ 10 TECU during G2+ events** (the hard-mode regime)
- **Heidke Skill Score improvement ≥ 20% over climatological persistence at the 6-hour forecast horizon**
- Coverage of conformal-wrapped 80% prediction intervals ≥ 78% on hold-out
- All metrics with bootstrapped 95% CIs

## Agent brief sketch

1. **Setup**: worktree at `~/577i-Projects/.worktrees/helios-fusion-engine-tft/` on branch `feat/v0.2-tft-tec-forecasting`.
2. **Data pipeline**:
   - `src/helios_fusion/tft/data.py` — windowed dataset assembly: pull CDDIS GIMs via `CddisGimAdapter`; align with DSCOVR + SWPC via the connectors' common time grid; produce a `pytorch-forecasting`-compatible `TimeSeriesDataSet`.
   - Cache-aware: warm the cache once over the full training window; subsequent epochs read from disk.
3. **Model**: `src/helios_fusion/tft/model.py` — either pin `pytorch-forecasting>=1.0` (recommended; well-maintained TFT impl) or write a thin from-scratch implementation per the Lim 2021 architecture diagrams. Choose pytorch-forecasting unless its license terms or breaking API changes preclude.
4. **Train**: `src/helios_fusion/tft/train.py` — entry point. Logs to `helios-fusion-internal/tft-runs/<UTC timestamp>/`. Each run produces (a) model checkpoint, (b) training-curve plots, (c) hold-out metric JSON.
5. **Eval**: `src/helios_fusion/tft/eval.py` — load the best checkpoint, compute MAE / HSS / conformal coverage on the hold-out events.
6. **Persist trained model**: weights land in `helios-fusion-internal/tft-runs/<UTC>/model.pt` (consistent with the existing weights/ pattern; IP-gated).
7. **Provenance**: emit a `HeliosTransformationRecord` per spec for the trained-model entry. Append to `helios-fusion-internal/weights/manifest.json` (the array preserves all run histories).

## Downstream payoff for `gannon-storm-rtk-analysis` v2

After this lands:

1. `gannon-storm-rtk-analysis/src/gannon_analysis/positioning.py` swaps the v1 climatological model for real SPP:
   - TEC at each station's (lat, lon) at each timestamp ← `TFTModel.predict(...)` (or directly from CDDIS GIM for the exact past; TFT predicts for the future-horizon flavor)
   - Klobuchar correction applied via the GNSS observable equations
   - Real pseudo-range residuals → 2D horizontal error per station
2. The "**1,302 station-hours over 2.5 cm**" headline gets recomputed against real SPP — likely shifts to a different (and more credible) number.
3. The methodology disclosure in `gannon-storm-rtk-analysis/docs/methodology.md` evolves from "v1 climatological; v2 real SPP" to "v2 real SPP shipped" — closes the v1→v2 boundary.

## Files to be created / modified

| Path | Action |
|---|---|
| `~/577i-Projects/.worktrees/helios-fusion-engine-tft/` | NEW worktree |
| `helios-fusion-engine/src/helios_fusion/tft/{__init__,data,model,train,eval}.py` | NEW |
| `helios-fusion-engine/tests/tft/test_*.py` | NEW (synthetic-data tests + integration test with recorded CDDIS fixture) |
| `helios-fusion-engine/pyproject.toml` | Edit (add `pytorch-forecasting` + `torch` to `[ml]` optional extra) |
| `helios-fusion-engine/notebooks/04-tft-tec-forecasting.ipynb` | NEW (reproducibility demo) |
| `helios-fusion-engine/docs/tft.md` | NEW (architecture + reproducibility walkthrough) |
| `helios-fusion-internal/tft-runs/<UTC>/...` | NEW (trained model artifacts; IP-gated) |
| `helios-fusion-internal/weights/manifest.json` | Edit (append `tft_runs[]` array entry) |
| `gannon-storm-rtk-analysis/src/gannon_analysis/positioning.py` | Edit (v2 swap to real SPP using TFT TEC) |
| `gannon-storm-rtk-analysis/docs/methodology.md` | Edit (close v1→v2 boundary) |

## Verification gates

1. Hold-out TEC MAE meets proposal §2 Obj. 4 thresholds.
2. Reproducibility notebook runs end-to-end on a fresh checkout with Earthdata creds in env.
3. `helios-fusion-internal/weights/manifest.json` has the new `tft_runs` array entry with full provenance.
4. `gannon-storm-rtk-analysis` v2 builds + tests pass with the new real-SPP positioning.
5. Refreshed "1,302 station-hours" number reported in the gannon-storm-rtk-analysis README + companion document.

## Cross-references

- Proposal §2 Obj. 4 (GNSS slice success criteria)
- Proposal §1.3 (Gannon case study + the v1→v2 boundary the gannon-storm-rtk-analysis methodology doc preserves)
- `helios-spaceweather-connectors/docs/adapters/cddis.md` (Earthdata setup walkthrough)
- `OPERATOR_TODO.md §2` (Earthdata credentials)
- Lim et al. (2021) — proposal ref [32]

## What this sprint does NOT do

- Does NOT integrate TFT-TEC outputs into the BMA fusion engine — that's a Phase II item. This sprint produces a standalone forecaster; integration with `helios-fusion-engine.bma` happens later.
- Does NOT publish a separate TFT paper — that's also a Phase II item.
- Does NOT replace the SEP all-clear kill-gate path — Sprint D's evaluation is unaffected.
