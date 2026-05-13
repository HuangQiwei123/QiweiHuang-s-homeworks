def calculate_runoff(P: float, CN: float) -> float:
    """Calculate SCS Curve Number runoff (Q) from precipitation (P) and curve number (CN).

    Args:
        P: Total precipitation depth (inches or mm).
        CN: SCS Curve Number (dimensionless, typically 30–100).

    Returns:
        Direct runoff depth Q in the same units as P.
    """
    if CN <= 0:
        raise ValueError(f"CN must be positive, got {CN}")

    S = (25400.0 / CN) - 254.0
    Ia = 0.2 * S

    if P <= Ia:
        return 0.0

    Q = (P - Ia) ** 2 / (P - Ia + S)
    return min(Q, P)
