# Project 03 - Reservoir Dispatch Optimization

## Overview

This project studies a 7-day reservoir dispatch problem. The model decides daily water releases based on inflow and electricity price data. It uses constrained optimization to improve hydropower revenue while maintaining storage and environmental requirements.

## Objectives

- Build a reservoir storage balance model.
- Define hydropower revenue as an optimization objective.
- Add physical constraints for storage and release.
- Verify the final schedule with a validation report.
- Explore trade-offs between revenue and ecological release goals.

## Optimization Components

| Component | Description |
|---|---|
| Decision variable | Daily release flow for 7 days |
| Objective | Increase total hydropower revenue |
| Solver | `scipy.optimize.minimize` with SLSQP |
| Main constraints | Storage bounds, release bounds, ecological release, mass balance |
| Outputs | Schedule table, validation report, trade-off figure |

## File Description

| File or Folder | Purpose |
|---|---|
| `reservoir_optimization.py` | Main optimization and analysis script. |
| `optimal_schedule.csv` | Optimized release, storage, and revenue schedule. |
| `optimal_schedule_report.txt` | Text summary of the optimized schedule. |
| `validation_report.txt` | Feasibility and constraint-check report. |
| `tradeoff_analysis.png` | Visualization of revenue and ecological trade-off. |
| `screenshots/` | Running and interaction screenshots. |
| `Experiment3_Reservoir_Optimization.docx` | Experiment report. |
| `requirements.txt` | Dependencies for this project. |

## How to Run

```bash
cd Project-03-Reservoir-Dispatch-Optimization
pip install -r requirements.txt
python reservoir_optimization.py
```

## Review Points

When reviewing this project, check:

- whether storage remains within the allowed reservoir capacity;
- whether daily release satisfies lower and upper limits;
- whether the ecological release condition is respected;
- whether the mass balance is consistent;
- whether the final revenue is calculated from the optimized release schedule.

## Existing Outputs

The repository already includes generated result files. The most useful files for quick review are:

- `optimal_schedule.csv`;
- `optimal_schedule_report.txt`;
- `validation_report.txt`;
- `tradeoff_analysis.png`.

These files allow the result to be inspected without rerunning the whole optimization.
