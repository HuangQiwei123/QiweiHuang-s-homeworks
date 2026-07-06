# Project 02 - SCS-CN Runoff Model

## Overview

This project implements the SCS Curve Number runoff equation and verifies the implementation with unit tests. It also produces a sensitivity analysis figure to show how runoff changes with Curve Number values.

## Objectives

- Implement the SCS-CN runoff formula in Python.
- Validate boundary cases and physical constraints.
- Plot the relationship between rainfall, Curve Number, and runoff.
- Provide a small testable model that can be reused in hydrological calculations.

## Formula

```text
S  = 25400 / CN - 254
Ia = 0.2 * S

if P <= Ia:
    Q = 0
else:
    Q = (P - Ia)^2 / (P - Ia + S)
```

Where:

- `P` is precipitation depth;
- `CN` is the Curve Number;
- `S` is potential maximum retention;
- `Ia` is initial abstraction;
- `Q` is direct runoff depth.

## File Description

| File or Folder | Purpose |
|---|---|
| `scs_cn.py` | Core function `calculate_runoff(P, CN)`. |
| `test_scs_cn.py` | Pytest test suite with 39 cases. |
| `sensitivity_analysis.py` | Generates runoff sensitivity plots. |
| `scs_cn_sensitivity.png` | Output figure from sensitivity analysis. |
| `screenshots/` | Running and interaction screenshots. |
| `Experiment2_SCSCN_Runoff.docx` | Experiment report. |
| `requirements.txt` | Dependencies for this project. |

## How to Run

```bash
cd Project-02-SCS-CN-Runoff-Model
pip install -r requirements.txt
python -m pytest test_scs_cn.py -v
python sensitivity_analysis.py
```

## Validation Coverage

The test file checks:

- zero precipitation;
- precipitation below initial abstraction;
- precipitation exactly equal to initial abstraction;
- normal calculation cases;
- `CN = 100` impervious-surface behavior;
- runoff not exceeding precipitation;
- invalid CN input.

## Result Interpretation

The sensitivity plot demonstrates that the CN-runoff relationship is nonlinear. When CN is high, a small increase in CN can lead to a larger increase in runoff. This matches the hydrological meaning of CN: impervious or low-infiltration surfaces produce more direct runoff.
