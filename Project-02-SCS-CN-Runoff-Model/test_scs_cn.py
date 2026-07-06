import pytest
from scs_cn import calculate_runoff


class TestZeroPrecipitation:
    """P = 0 should always yield Q = 0."""

    def test_zero_precip_typical_cn(self):
        assert calculate_runoff(0.0, 80.0) == 0.0

    def test_zero_precip_low_cn(self):
        assert calculate_runoff(0.0, 40.0) == 0.0

    def test_zero_precip_max_cn(self):
        assert calculate_runoff(0.0, 100.0) == 0.0


class TestPLessThanIa:
    """Q = 0 whenever P < Ia (0.2 * S)."""

    def test_just_below_ia(self):
        # CN=50 → S=254, Ia=50.8 → P=50 < 50.8
        Q = calculate_runoff(50.0, 50.0)
        assert Q == 0.0

    def test_well_below_ia(self):
        # CN=60 → S≈169.33, Ia≈33.87 → P=10 < 33.87
        Q = calculate_runoff(10.0, 60.0)
        assert Q == 0.0

    def test_tiny_precip(self):
        Q = calculate_runoff(1.0, 70.0)
        assert Q == 0.0


class TestPEqualsIa:
    """Q = 0 exactly at the initial abstraction threshold."""

    def test_p_equals_ia_cn_50(self):
        # CN=50 → S=254, Ia=50.8
        Q = calculate_runoff(50.8, 50.0)
        assert Q == 0.0  # (0)² / (0 + S) = 0

    def test_p_equals_ia_cn_80(self):
        # CN=80 → S=63.5, Ia=12.7
        Q = calculate_runoff(12.7, 80.0)
        assert Q == 0.0


class TestNormalCase:
    """Standard SCS-CN runoff calculation."""

    def test_p50_cn80(self):
        # S=63.5, Ia=12.7, Q=(50-12.7)²/(50-12.7+63.5)=1391.29/100.8
        Q = calculate_runoff(50.0, 80.0)
        expected = (50.0 - 12.7) ** 2 / (50.0 - 12.7 + 63.5)
        assert Q == pytest.approx(expected)

    def test_p75_cn70(self):
        # S=108.857..., Ia=21.771..., Q=(75-21.77...)²/(75-21.77...+108.85...)
        S = 25400.0 / 70.0 - 254.0
        Ia = 0.2 * S
        expected = (75.0 - Ia) ** 2 / (75.0 - Ia + S)
        assert calculate_runoff(75.0, 70.0) == pytest.approx(expected)

    def test_p30_cn90(self):
        # S≈28.22, Ia≈5.64, Q=(30-5.64)²/(30-5.64+28.22)
        S = 25400.0 / 90.0 - 254.0
        Ia = 0.2 * S
        expected = (30.0 - Ia) ** 2 / (30.0 - Ia + S)
        assert calculate_runoff(30.0, 90.0) == pytest.approx(expected)


class TestMaximumCN:
    """CN = 100 → S = 0, Ia = 0, so Q = P for all P >= 0."""

    def test_cn100_zero_precip(self):
        assert calculate_runoff(0.0, 100.0) == 0.0

    def test_cn100_small_precip(self):
        assert calculate_runoff(5.0, 100.0) == pytest.approx(5.0)

    def test_cn100_moderate_precip(self):
        assert calculate_runoff(30.0, 100.0) == pytest.approx(30.0)

    def test_cn100_large_precip(self):
        assert calculate_runoff(200.0, 100.0) == pytest.approx(200.0)


class TestQNeverExceedsP:
    """Runoff must never exceed precipitation for any valid input."""

    @pytest.mark.parametrize(
        "P, CN",
        [
            (10.0, 30.0),
            (10.0, 50.0),
            (10.0, 70.0),
            (10.0, 90.0),
            (10.0, 100.0),
            (50.0, 30.0),
            (50.0, 50.0),
            (50.0, 70.0),
            (50.0, 90.0),
            (50.0, 100.0),
            (100.0, 30.0),
            (100.0, 60.0),
            (100.0, 80.0),
            (100.0, 95.0),
            (100.0, 100.0),
            (200.0, 40.0),
            (200.0, 75.0),
            (200.0, 99.0),
            (500.0, 55.0),
            (500.0, 85.0),
        ],
    )
    def test_q_never_exceeds_p(self, P, CN):
        Q = calculate_runoff(P, CN)
        assert Q <= P, f"Q={Q} exceeded P={P} for CN={CN}"


class TestEdgeCases:
    def test_p_just_above_ia(self):
        # CN=80 → S=63.5, Ia=12.7 → P=12.7001
        Q = calculate_runoff(12.7001, 80.0)
        assert Q > 0.0
        assert Q <= 12.7001

    def test_negative_cn_raises(self):
        with pytest.raises(ValueError):
            calculate_runoff(50.0, 0.0)

    def test_zero_cn_raises(self):
        with pytest.raises(ValueError):
            calculate_runoff(50.0, 0.0)

    def test_large_inputs(self):
        # Verify numerical stability with large values
        Q = calculate_runoff(1000.0, 45.0)
        assert Q > 0.0
        assert Q <= 1000.0
