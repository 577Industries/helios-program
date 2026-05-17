---
network: Twitter / X
status: draft (operator review before publishing)
character_limit: 280 per tweet
length: ~10 tweet thread
---

**Tweet 1/9** — Hook + headline plot

May 10, 2024. Peak planting season in the U.S. Midwest. RTK GPS positioning went sideways for 12-48 hours across the corn belt.

We just quantified what farmers actually saw.

🧵 a thread on the Gannon G5 storm + how our retrospective works (with code).

[ATTACH: results/figures/fig-01-regional-error-vs-time.png]

---

**Tweet 2/9**

The headline: across 25 NGS CORS stations in IA / IL / IN / OH, 2D horizontal RTK error exceeded the 2.5 cm planting threshold for **1,302 station-hours** during May 10-12.

95th-percentile peak: ~3.0 m. ~150× the quiet-period baseline.

---

**Tweet 3/9**

Why does the 2.5 cm threshold matter? Because that's what John Deere StarFire, Trimble RTX/RTK, and AgLeader receivers need to deliver for row-crop planting accuracy. Lose it during peak planting season and you're either parking the tractor or planting blind.

---

**Tweet 4/9**

The data is all public:
• NGS CORS RINEX (175 real files; ITRF2014 truth from each station's day-131 header)
• Kp from GFZ Potsdam (CC-BY-4.0)
• Dst from Kyoto WDC

⚠️ Gotcha: NOAA SWPC's public archive only serves the last ~30 days. For retrospective work, you need GFZ + Kyoto.

---

**Tweet 5/9**

Honest disclosure: v1 of our analysis is a *climatological* model, not full pseudo-range SPP. Real RINEX manifest, real Kp/Dst, but the per-station error series is derived from a documented empirical model calibrated against OEM quiet-time specs + Gannon peak observations.

---

**Tweet 6/9**

v2 will swap in full SPP/PPP via the HELIOS connectors layer (helios-spaceweather-connectors), which adds a CDDIS GIMs adapter for IGS ephemerides. The methodology doc spells out the v1→v2 boundary precisely.

---

**Tweet 7/9**

`make all` reproduces the entire analysis from cold cache in ~10 min. 40 tests at 80% coverage. mypy --strict, ruff clean. The reproducibility scaffold is the point: anyone can clone, re-run, audit.

---

**Tweet 8/9**

This is one of four artifacts in HELIOS — our NASA SBIR Phase I program (SPWX.1.S26A) on calibrated, provenance-tracked space-weather decision intelligence. The other three: a provenance RFC, a connector library, a Bayesian Model Averaging fusion engine.

---

**Tweet 9/9** — CTA

If your operation was affected by the May 2024 storm (or any G2+ event in 2025-2026), we'd value the conversation. We're building the translation layer that converts Kp=9 into "your StarFire 6000 will not hold sub-3 cm RTK for 4 hours."

📦 https://github.com/577Industries/gannon-storm-rtk-analysis
🌐 https://577industries.github.io/helios-program/
