# Project 3 -- Reservoir Dispatch Optimization
### Software Development · Water Resources Optimization · 2026

---

`folder: project-3`

This project solves a seven-day reservoir release scheduling problem. The model chooses daily releases based on inflow and electricity price data, while respecting storage limits, release limits, ecological release requirements, and water balance.

---

## Optimization Problem

| Component | Description |
|---|---|
| **Decision variable** | daily reservoir release for 7 days |
| **Objective** | maximize hydropower revenue |
| **Solver** | SLSQP through `scipy.optimize.minimize` |
| **Physical constraints** | storage bounds, release bounds, ecological flow, mass balance |
| **Main result** | feasible schedule with total revenue reported in `validation_report.txt` |

---

## Project Details

| | |
|---|---|
| **Python files** | `reservoir_optimization.py` |
| **Output files** | `optimal_schedule.csv` · `optimal_schedule_report.txt` · `validation_report.txt` · `tradeoff_analysis.png` |
| **Documents** | `requirements.txt` · `README.md` · `Experiment3_Reservoir_Optimization.docx` |
| **Screenshots** | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` |
| **Dependencies** | `numpy` · `scipy` · `matplotlib` · `pandas` |

---

## Existing Result

The included validation report records:

```text
Release bounds        PASS
Storage bounds        PASS
Mass balance          PASS
Ecological violations 0
Solution feasible     YES
Total revenue         $54,910.69
```

---

## Run It

```bash
pip install -r requirements.txt
python reservoir_optimization.py
```

---

## Review Notes

- `optimal_schedule.csv` is the most direct file for checking the daily operation plan.
- `validation_report.txt` explains whether the result satisfies the constraints.
- `tradeoff_analysis.png` provides a visual result for comparing optimization objectives.
- The project demonstrates use of numerical optimization rather than only manual calculation.
