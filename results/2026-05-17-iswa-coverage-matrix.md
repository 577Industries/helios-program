# ISWA SEP Scoreboards — exhaustive pre-2018 coverage matrix

**Probe date**: 2026-05-17 (Sprint C-Training-v2)
**Probe script**: `/tmp/iswa_probe.py` (committed snapshot below)
**Base URL**: `https://iswa.ccmc.gsfc.nasa.gov/iswa_data_tree/model/heliosphere/sep_scoreboard/`

## Headline finding

**ISWA's earliest deposit anywhere is calendar-year 2017.** No model directory contains any data older than 2017. Of the 7 Table 3-1 training events, only **September 2017** has real ISWA coverage; the other 6 events (Bastille 2000, Halloween 2003, Mid-cycle 23 2005, Late-cycle 23 2006, Cycle 24 onset 2012, Cycle 24 mid 2012) are confirmed empty.

This finding **directly upgrades** v1's "ISWA cutover ~2018" hypothesis to: ISWA cutover is **exactly Jan 2017 for SEPSTER, UMASEP v2_0, SAWS_ASPECS Nowcasts/Profile, NCAR_MLSO_KCOR, and mag4_2019**; everything else starts later. v1's blanket synthetic-proxy fallback for Sept 2017 was unnecessarily conservative.

## Models discovered (post-REleASE-filter)

11 top-level model directories visible (excluded REleASE family `RELEASE`, `RELEASE_PLUS`, `STEREO_RELEASE`, `STEREO_RELEASE_PLUS` per licensing constraint):

| Model | Top-level subdirs | Year coverage (across all variants) |
|---|---|---|
| `GSU_All_Clear` | `v0_1` | 2023–2026 |
| `MagPy` | `2.X`, `3.X` (`LOS`, `VEC`) | 2023–2026 (2.X: 2023–2025; 3.X/VEC + 3.X/LOS: 2025–2026) |
| `NCAR_MLSO_KCOR` | (no variant — year dirs at top) | 2017, 2022, 2024, 2025, 2026 |
| `SAWS_ASPECS` | `1.X/{Forecasts,Nowcasts}/{Intensity,Probability,Profile}` | Nowcasts/Profile: 2017+; others: 2022+ |
| `SEPForecast` | `2X` | 2025–2026 |
| `SEPSTER` | `Parker`, `WSA-ENLIL` | Parker: 2017, 2019–2026; WSA-ENLIL: 2017, 2020–2026 |
| `SEPSTER2D` | `1.X` | 2020–2026 |
| `SPRINTS-SEP` | `1.X/Post_Eruptive` | 2022–2026 |
| `UMASEP` | `v2_0`, `v2_1`, `v3_X`, `v20190101` | v2_0: 2017, 2021; v3_X: 2022–2026 |
| `iPATH` | `2.X` | **No year subdirectories at all** (empty model dir) |
| `mag4_2019` | `{HMI-NRT,V-HMI-NRT,VPLUS-HMI-NRT,VWF-HMI-NRT,WF-HMI-NRT}-JSON` | 2017, 2019–2026 |

## Per-event coverage matrix

Columns: 6 of 7 events probed for the calendar months containing the onset (Bastille 2000 → 2000-07; Halloween 2003 → 2003-10 + 2003-11; etc.). Sept 2017 → 2017-09. Cell value = count of JSON files returned by the ISWA Apache index for that (model, variant, energy, year/month).

| Tuple | Bastille 2000 (07) | Halloween 2003 (10/11) | Mid-23 2005 (01) | Late-23 2006 (12) | Cycle24-onset 2012 (03) | Cycle24-mid 2012 (05) | **Sept 2017 (09)** |
|---|---|---|---|---|---|---|---|
| `UMASEP/v2_0/10MeV` | 0 | 0 | 0 | 0 | 0 | 0 | **8,640** |
| `UMASEP/v2_0/30MeV` | 0 | 0 | 0 | 0 | 0 | 0 | **8,640** |
| `UMASEP/v2_0/50MeV` | 0 | 0 | 0 | 0 | 0 | 0 | **8,640** |
| `UMASEP/v2_0/100MeV` | 0 | 0 | 0 | 0 | 0 | 0 | **8,640** |
| `UMASEP/v2_0/500MeV` | 0 | 0 | 0 | 0 | 0 | 0 | **43,199** |
| `UMASEP/v3_X/10MeV` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (v3_X starts 2022) |
| `SEPSTER/Parker` | 0 | 0 | 0 | 0 | 0 | 0 | **28** |
| `SEPSTER/WSA-ENLIL` | 0 | 0 | 0 | 0 | 0 | 0 | **28** |
| `SEPSTER2D/1.X` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (starts 2020) |
| `SAWS_ASPECS/1.X/Nowcasts/Profile` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (year dir exists, but probe found no JSONs) |
| `SAWS_ASPECS/*` (others) | 0 | 0 | 0 | 0 | 0 | 0 | 0 (others start 2022) |
| `MagPy/2.X`, `MagPy/3.X/{LOS,VEC}` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (starts 2023+) |
| `SPRINTS-SEP/1.X/Post_Eruptive` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (starts 2022) |
| `iPATH/2.X` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (no year dirs at all) |
| `GSU_All_Clear/v0_1` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (starts 2023) |
| `SEPForecast/2X` | 0 | 0 | 0 | 0 | 0 | 0 | 0 (starts 2025) |
| `NCAR_MLSO_KCOR` | 0 | 0 | 0 | 0 | 0 | 0 | **57** |
| `mag4_2019/HMI-NRT-JSON` | 0 | 0 | 0 | 0 | 0 | 0 | **708** |
| `mag4_2019/V-HMI-NRT-JSON` | 0 | 0 | 0 | 0 | 0 | 0 | **658** |
| `mag4_2019/VPLUS-HMI-NRT-JSON` | 0 | 0 | 0 | 0 | 0 | 0 | **658** |
| `mag4_2019/VWF-HMI-NRT-JSON` | 0 | 0 | 0 | 0 | 0 | 0 | **658** |
| `mag4_2019/WF-HMI-NRT-JSON` | 0 | 0 | 0 | 0 | 0 | 0 | **708** |

**Total real-data tuples for Sept 2017**: **13** (5 UMASEP-v2_0 energies + 2 SEPSTER variants + 5 mag4_2019 variants + NCAR_MLSO_KCOR).

**Total real-data tuples for the other 6 events**: **0**.

## Path decision rationale

- **Path A (use real ISWA data where available)**: applies to Sept 2017 only. Refit BMA priors for `sep_2017` using real UMASEP v2_0 + SEPSTER (Parker, WSA-ENLIL) component-model predictions.
- **Path B (pivot to SWPC SEP-event archive for ground-truth labels)**: applies to all 7 events. The umbra.nascom.nasa.gov/SEP/seps.html archive (NOAA Space Environment Services Center "Solar Proton Events Affecting the Earth Environment, 1976–present") provides observed SEP onset times + peak proton flux + associated CME/flare. This is a methodologically stronger ground-truth signal than v1's synthetic Kp-derived truth.
- **Per-component-per-event fallback** (Sprint C-Training-v1 open question #2): only the (model, variant, energy) tuples without real ISWA data fall back to synthetic-proxy streams. For Sept 2017 this means UMASEP v2_0 + SEPSTER use real data; the other 9 nominal components use synthetic proxies anchored on the SWPC ground-truth label.

We choose **Hybrid: Path A + Path B**. Sprint C-Training-v2 refits with real UMASEP-v2_0 + SEPSTER for Sept 2017, SWPC archive ground-truth for all 7 events, and per-component-per-event synthetic proxies elsewhere.

## REleASE-family exclusion (verified)

The top-level discovery confirmed these four model directories exist but are **never probed, never listed in any registry, never appear in any URL emitted by the adapter**:

- `RELEASE/`
- `RELEASE_PLUS/`
- `STEREO_RELEASE/`
- `STEREO_RELEASE_PLUS/`

The adapter's `_assert_no_hesperia_release()` guard, the `FORBIDDEN_PATH_TOKENS = {"release", "hesperia"}` allowlist, and the URL-sweep regression test continue to enforce this.

## Registry expansion recommendation for `SepScoreboardsAdapter` v0.2.1

Add the following entries to `SCOREBOARD_MODELS` default registry (v0.2.0 → v0.2.1):

| Entry | Reason |
|---|---|
| `UMASEP` variants `v2_0`, `v2_1`, `v20190101` (in addition to existing `v3_X`) | v2_0 covers 2017 (Table 3-1 Sept 2017 event); v2_1 covers 2021–2022; v20190101 covers 2020–2021 |
| `SEPSTER` variant `WSA-ENLIL` (in addition to existing `Parker`) | Independent component prediction; covers 2017+ for Sept 2017 event |
| `SAWS_ASPECS` extended variants chain to `1.X/Nowcasts/{Probability,Profile,Intensity}` and `1.X/Forecasts/{...}` | The existing `("1.X",)` chain doesn't reach JSON files; the real layout has `Forecasts/Nowcasts × Intensity/Probability/Profile` between `1.X` and the year |
| `MagPy` chain `("2.X",)` (in addition to existing `("3.X", "VEC")`) | 2.X covers 2023–2025; 3.X starts 2025; needed for kill-gate hold-out events 2022/2023/2024 |
| `MagPy` chain `("3.X", "LOS")` (in addition to existing `("3.X", "VEC")`) | LOS is a second 3.X channel; both should be ingested |
| `SPRINTS-SEP` chain `("1.X", "Post_Eruptive")` (in addition to existing `()`) | The existing empty-variants registry hits no files; the real layout requires this chain |
| `GSU_All_Clear` chain `("v0_1",)` — NEW | Newly discovered model; covers 2023–2026 |
| `SEPForecast` chain `("2X",)` — NEW | Newly discovered model; covers 2025–2026 |
| `mag4_2019` chain `("HMI-NRT-JSON",)` and four other variants — NEW | Newly discovered model with broadest pre-2018 coverage (2017+); five independent NRT variant streams |

**NOT added to registry**: `iPATH/2.X` — model directory exists but has **zero year subdirectories**. The model is registered on the ISWA side but has not deposited any data anywhere. Will continue to appear as a nominal component (synthetic-proxy stream) in the training loader.

**NOT added**: `NCAR_MLSO_KCOR` is a coronagraph/EUV product, not a SEP probability/intensity forecast. It belongs to the upstream-cause trigger stream (CME observation), not the per-model SEP prediction registry. Documented but not registered as a SEP component.

## Probe methodology notes

- **Filter applied at every level**: `FORBIDDEN_TOKENS = {"release", "hesperia"}` checked case-insensitively against every URL before fetch.
- **Polite rate**: 0.3s sleep between top-level model layout walks; 0.15s sleep between event-window probes. No 429s observed during the probe.
- **Apache index parsing**: identical regex to the adapter's `_HREF_RE` (`r'href="([^"?/][^"]*?)"'`).
- **Year subdirectory detection**: 4-digit numeric match (`re.fullmatch(r"\d{4}", subdir)`).
- **What "JSON files found" means**: count of href values ending in `.json` inside the `<year>/<MM>/` index. A single `sep_forecast_submission` envelope per JSON.

## Files

- Probe results (JSON): `/tmp/iswa_probe_results.json` — full raw layout walk + per-tuple probe counts
- Probe log: `/tmp/iswa_probe_log.txt` — stdout from the probe run

## Implications for Sprint C-Training-v2

1. **Connectors v0.2.1**: registry expansion is substantive (10+ new tuples). Bump version per C.3.
2. **Fusion-engine v2 loader**: implement per-component-per-event fallback (C.5); use UMASEP-v2_0 + SEPSTER real-data path for Sept 2017 (C.4 Path A), use SWPC archive labels for all 7 events (C.4 Path B).
3. **Methodology note for OSF deviations**: v2's hybrid ground-truth signal (SWPC archive labels) is methodologically stronger than v1's synthetic-truth signal. Document in the v2 review pack.
