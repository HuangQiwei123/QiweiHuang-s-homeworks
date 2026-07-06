"""Physical-sense validation of flood inundation results."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from flood_inundation import calculate_flood, load_dem

OUT_DIR = Path(__file__).resolve().parent


def main() -> None:
    dem = load_dem()
    dem_min = float(dem.min())
    wl_start, wl_end, wl_step = 30.0, 80.0, 0.5
    water_levels = np.arange(wl_start, wl_end + wl_step, wl_step)

    check_names = [
        "pct_in_range",
        "max_depth_correct",
        "depth_non_negative",
        "depth_mask_consistent",
        "depth_value_correct",
    ]
    passed_by_check = {name: 0 for name in check_names}
    failed_by_check = {name: 0 for name in check_names}
    area_pcts = []
    level_passed = 0
    level_failed = 0

    for wl in water_levels:
        mask, depth, area_pct = calculate_flood(dem, float(wl))
        flooded = int(mask.sum())
        max_depth = float(depth.max())
        area_pcts.append(area_pct)

        if flooded > 0:
            expected_max = float(wl - dem_min)
            max_depth_correct = np.isclose(max_depth, expected_max, atol=0.01)
            depth_mask_consistent = bool(((depth > 0) == mask).all())
            depth_value_correct = bool(np.allclose(depth[mask], wl - dem[mask], atol=0.01))
        else:
            max_depth_correct = max_depth == 0.0
            depth_mask_consistent = True
            depth_value_correct = True

        checks = {
            "pct_in_range": 0.0 <= area_pct <= 100.0,
            "max_depth_correct": bool(max_depth_correct),
            "depth_non_negative": bool((depth >= 0).all()),
            "depth_mask_consistent": depth_mask_consistent,
            "depth_value_correct": depth_value_correct,
        }

        if all(checks.values()):
            level_passed += 1
        else:
            level_failed += 1

        for name, ok in checks.items():
            if ok:
                passed_by_check[name] += 1
            else:
                failed_by_check[name] += 1

    areas = np.array(area_pcts, dtype=float)
    deltas = np.diff(areas)
    monotonic = bool((deltas >= 0).all())
    if not monotonic:
        violations = np.where(deltas < 0)[0]
        for vi in violations:
            print(f"  Monotonicity violation at WL={water_levels[vi]:.1f}->{water_levels[vi + 1]:.1f}: "
                  f"{areas[vi]:.4f}% -> {areas[vi + 1]:.4f}%")

    total_checks = len(water_levels) * len(check_names) + 1
    passed_checks = sum(passed_by_check.values()) + (1 if monotonic else 0)
    failed_checks = total_checks - passed_checks

    print("=" * 56)
    print("  PHYSICAL-SENSE VALIDATION REPORT")
    print("=" * 56)
    print(f"  Water levels tested:      {len(water_levels)}")
    print(f"  DEM elevation range:      [{dem_min:.2f}, {dem.max():.2f}] m")
    print()

    print(f"  1. Area monotonic increase: {'PASS' if monotonic else 'FAIL'}")
    print(f"     Area range: [{areas.min():.2f}%, {areas.max():.2f}%] - non-decreasing")
    print()

    print(f"  2. Per-level checks ({len(water_levels)} levels):")
    for name in check_names:
        status = "always true" if failed_by_check[name] == 0 else f"{failed_by_check[name]} failed"
        print(f"     - {name:<22} {status}")
    print(f"     Passed levels: {level_passed}/{len(water_levels)}, Failed levels: {level_failed}")
    print()

    print(f"  OVERALL: {'ALL CHECKS PASSED' if failed_checks == 0 else 'SOME FAILED'}")
    print(f"  Total checks: {total_checks}, Passed: {passed_checks}, Failed: {failed_checks}")
    print("=" * 56)

    np.savez(OUT_DIR / "validation_results.npz",
             water_levels=water_levels, area_pcts=areas, monotonic=monotonic)
    print("\nSaved: validation_results.npz")


if __name__ == "__main__":
    main()
