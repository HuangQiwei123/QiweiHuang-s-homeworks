from __future__ import annotations

import numpy as np


def calculate_runoff(P: float | np.ndarray, CN: float | np.ndarray) -> float | np.ndarray:
    """Calculate SCS Curve Number runoff depth.

    Args:
        P: Total precipitation depth in mm. Scalars and NumPy arrays are supported.
        CN: Curve Number in [0, 100]. Scalars and NumPy arrays are supported.

    Returns:
        Direct runoff depth Q in mm, with the same broadcast shape as P and CN.
    """
    p = np.asarray(P, dtype=float)
    cn = np.asarray(CN, dtype=float)
    p, cn = np.broadcast_arrays(p, cn)

    if np.any(p < 0):
        raise ValueError("Precipitation P must be non-negative")
    if np.any((cn < 0) | (cn > 100)):
        raise ValueError("Curve Number CN must be in the range [0, 100]")

    q = np.zeros_like(p, dtype=float)

    impervious = cn == 100
    q[impervious] = p[impervious]

    valid = (cn > 0) & (cn < 100)
    if np.any(valid):
        s = (25400.0 / cn[valid]) - 254.0
        ia = 0.2 * s
        active = p[valid] > ia
        runoff = np.zeros_like(s)
        runoff[active] = (p[valid][active] - ia[active]) ** 2 / (
            p[valid][active] - ia[active] + s[active]
        )
        q[valid] = np.minimum(runoff, p[valid])

    if q.ndim == 0:
        return float(q)
    return q
