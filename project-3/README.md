# Project 3 - Reservoir Dispatch Optimization

This experiment solves a 7-day reservoir release scheduling problem under storage, release, mass-balance, hydropower, and ecological-flow constraints.

## Key Features

- Maximizes hydropower revenue while evaluating ecological-flow trade-offs.
- Supports SciPy SLSQP optimization when SciPy is installed.
- Includes a linear fallback solver for environments without SciPy.
- Exports an optimal 7-day schedule to CSV.
- Generates a Pareto-style trade-off figure.
- Writes a validation report for storage bounds, release bounds, and mass balance.

## Files

- `reservoir_optimization.py` - Optimization, validation, and plotting workflow.
- `optimal_schedule.csv` - 7-day release schedule.
- `validation_report.txt` - Constraint verification report.
- `tradeoff_analysis.png` - Revenue/ecology trade-off figure.
- `optimal_schedule_report.txt` - Text summary of the optimal schedule.

## Run

```bash
pip install -r requirements.txt
python reservoir_optimization.py
```

## Result Figure

![Reservoir trade-off](tradeoff_analysis.png)
