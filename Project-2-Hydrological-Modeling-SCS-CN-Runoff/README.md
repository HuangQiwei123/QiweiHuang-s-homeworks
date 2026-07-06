# SCS-CN Runoff Model

**Specialized Experiment 2 · Xi'an Jiaotong University · Software Development 2026**

Hydrological runoff calculation using the USDA Soil Conservation Service Curve Number method. The implementation translates the mathematical formula into tested Python code, handles boundary conditions, and visualizes runoff sensitivity to rainfall depth and curve number.

---

## Model Logic

| Quantity | Formula / Rule |
| --- | --- |
| Potential retention | `S = 25400 / CN - 254` |
| Initial abstraction | `Ia = 0.2 * S` |
| No-runoff condition | `P <= Ia` gives `Q = 0` |
| Runoff equation | `Q = (P - Ia)^2 / (P - Ia + S)` |
| Physical cap | `Q <= P` |

---

## What's Inside

| File | Role |
| --- | --- |
| `scs_cn.py` | Core `calculate_runoff(P, CN)` implementation with scalar and NumPy-array support |
| `test_scs_cn.py` | Boundary-condition and vectorization tests |
| `sensitivity_analysis.py` | Generates CN sensitivity and rainfall-runoff comparison plots |
| `scs_cn_sensitivity.png` | Output figure for runoff sensitivity |
| `Experiment2_SCSCN_Runoff.docx` | Original experiment task document |
| `report.tex` | Overleaf-ready experiment write-up |
| `requirements.txt` | Python dependencies |

---

## Run It

```bash
# clone and open this project
git clone https://github.com/HuangQiwei123/QiweiHuang-s-homeworks.git
cd QiweiHuang-s-homeworks
git checkout project-2
cd Project-2-Hydrological-Modeling-SCS-CN-Runoff

# install
pip install -r requirements.txt

# run analysis
python sensitivity_analysis.py
pytest test_scs_cn.py
```

---

## Development Notes

Built through iterative AI-assisted refinement:

- Round 1 -- Formula translation and baseline runoff calculation.
- Round 2 -- Boundary tests for `P = 0`, `P <= Ia`, `CN = 0`, and `CN = 100`.
- Round 3 -- Vectorized NumPy support and sensitivity-plot generation.

The plotting script includes a Pillow fallback so the result figure can still be generated in lightweight Python environments.

---

## Result Preview

The generated figure compares fixed-rainfall CN sensitivity and rainfall-runoff curves for multiple curve numbers.

![SCS-CN sensitivity result](scs_cn_sensitivity.png)

---

*Huang Qiwei · 3125301141 · Software Development · Xi'an Jiaotong University · 2026*
