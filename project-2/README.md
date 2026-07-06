# Project 2 -- SCS-CN Runoff Model
### Software Development · Hydrological Modeling · 2026

---

`folder: project-2`

This project implements the SCS Curve Number runoff method in Python. The experiment emphasizes three parts: a clear model function, unit tests for physical and boundary behavior, and a sensitivity figure showing how runoff changes with Curve Number.

---

## Model

```text
S  = 25400 / CN - 254
Ia = 0.2 * S

Q = 0,                         if P <= Ia
Q = (P - Ia)^2 / (P - Ia + S), if P > Ia
```

`P` is precipitation depth, `CN` is Curve Number, `S` is potential maximum retention, `Ia` is initial abstraction, and `Q` is direct runoff.

---

## Project Details

| | |
|---|---|
| **Python files** | `scs_cn.py` · `test_scs_cn.py` · `sensitivity_analysis.py` |
| **Output files** | `scs_cn_sensitivity.png` |
| **Documents** | `requirements.txt` · `README.md` · `Experiment2_SCSCN_Runoff.docx` |
| **Screenshots** | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` · `screenshots/5.png` |
| **Dependencies** | `numpy` · `matplotlib` · `pytest` |

---

## Test Coverage

The pytest suite contains 39 checks, including:

```text
zero precipitation                  -> Q = 0
P below initial abstraction          -> Q = 0
P exactly at initial abstraction     -> Q = 0
standard numerical cases             -> formula verification
CN = 100                             -> Q equals P
physical constraint                  -> Q never exceeds P
invalid CN                           -> ValueError
```

---

## Run It

```bash
pip install -r requirements.txt
python -m pytest test_scs_cn.py -v
python sensitivity_analysis.py
```

---

## Review Notes

- `scs_cn.py` is the core model file.
- `test_scs_cn.py` demonstrates that the model handles edge cases.
- `scs_cn_sensitivity.png` visualizes the nonlinear increase of runoff as CN rises.
- The model is intentionally compact so the formula, tests, and results can be inspected quickly.
