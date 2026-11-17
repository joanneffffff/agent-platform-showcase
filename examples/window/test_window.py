"""Time windows are data selection, not drawing.

Run: ``python -m pytest examples/window/test_window.py -q`` (needs pytest only).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from window import MIN_POINTS, apply_window  # noqa: E402


def rows(days: int) -> list[dict]:
    return [{"date": f"2026-11-{day:02d}", "close": float(day)} for day in range(1, days + 1)]


def test_last_n_days_keeps_the_tail() -> None:
    kept, gap = apply_window(rows(30), {"kind": "last_n_days", "value": 20})
    assert gap == ""
    assert len(kept) == 20
    assert kept[-1]["date"] == "2026-11-30"


def test_range_is_inclusive_on_both_ends() -> None:
    kept, gap = apply_window(rows(30), {"kind": "range", "start": "2026-11-05",
                                        "end": "2026-11-10"})
    assert gap == ""
    assert [row["date"] for row in kept] == [
        "2026-11-05", "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09", "2026-11-10"]


def test_ytd_defaults_to_the_last_row_year() -> None:
    kept, gap = apply_window(rows(30), {"kind": "ytd"})
    assert gap == ""
    assert len(kept) == 30


def test_too_few_points_is_a_gap_not_an_exception() -> None:
    # a single row is below MIN_POINTS; two rows are allowed
    kept, gap = apply_window(rows(30), {"kind": "range", "start": "2026-11-30",
                                        "end": "2026-11-30"})
    assert kept == []
    assert gap == "too_few_points"
    assert MIN_POINTS == 2
    two, gap_two = apply_window(rows(30), {"kind": "range", "start": "2026-11-29"})
    assert gap_two == "" and len(two) == 2


def test_unknown_kind_and_empty_input_return_gaps() -> None:
    assert apply_window(rows(5), {"kind": "last_week"}) == ([], "bad_window")
    assert apply_window([], {"kind": "last_n_days"}) == ([], "too_few_points")
    # no window means "use the rows as they are"
    kept, gap = apply_window(rows(3), None)
    assert gap == "" and len(kept) == 3
