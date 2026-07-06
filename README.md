# Smart Water Lab Homework Portfolio

This repository contains four specialized software-development experiments for water resources applications. Each project folder includes the task document, implementation code, generated outputs, screenshots, and a short project README.

## Project Index

| Project | Topic | Main Outputs |
| --- | --- | --- |
| [Project 1](project-1/) | Short-term rainfall monitoring and alert dashboard | Streamlit app, alert log, rainfall map, dashboard screenshots |
| [Project 2](project-2/) | SCS-CN runoff calculation and sensitivity analysis | Vectorized runoff function, tests, sensitivity plot |
| [Project 3](project-3/) | Reservoir dispatch optimization | Optimal schedule CSV, validation report, Pareto trade-off figure |
| [Project 4](project-4/) | DEM-based flood inundation analysis | DEM data, flood extent/depth maps, trend curve, validation archive |

## Repository Structure

```text
.
├── project-1/   # Rainfall alert system
├── project-2/   # SCS-CN runoff modeling
├── project-3/   # Reservoir optimization
├── project-4/   # Flood inundation analysis
└── requirements.txt
```

## Quick Start

Install the shared Python dependencies:

```bash
pip install -r requirements.txt
```

Then open an individual project folder and follow its README. Several scripts include fallback plotting logic so the core outputs can still be generated in lightweight Python environments.

## Highlights

- Four complete water-resources experiments are organized consistently.
- Each project contains both source code and generated evidence.
- Validation scripts check physical constraints such as runoff bounds, reservoir mass balance, and monotonic flood-area growth.
- Result figures are committed for direct review on GitHub.
