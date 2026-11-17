"""Time windows are data selection, not drawing.

One pure function, one table of kinds: adding "今年以来" later is a row here, not
an ``if`` in every caller. Rendering never sees a window.
"""
from __future__ import annotations

from typing import Any, Callable

__all__ = ["WINDOW_GAP_TEXT", "apply_window", "window_kind"]

#: Below this a chart has nothing to show.
MIN_POINTS = 2

WINDOW_GAP_TEXT = {
    "bad_window": "无法识别的时间窗口",
    "too_few_points": "可作图的数据点不足",
}

_DATE_KEYS = ("date", "trade_date", "as_of")


def _date_of(row: dict[str, Any]) -> str:
    for key in _DATE_KEYS:
        value = str(row.get(key) or "")
        if value:
            return value[:10]
    return ""


def _last_n(rows: list[dict[str, Any]], window: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        count = int(window.get("value") or 60)
    except (TypeError, ValueError):
        count = 60
    count = max(2, min(500, count))
    return rows[-count:]


def _range(rows: list[dict[str, Any]], window: dict[str, Any]) -> list[dict[str, Any]]:
    start = str(window.get("start") or "")[:10]
    end = str(window.get("end") or "")[:10]
    if not start and not end:
        return []
    kept = []
    for row in rows:
        day = _date_of(row)
        if not day:
            continue
        if start and day < start:
            continue
        if end and day > end:
            continue
        kept.append(row)
    return kept


def _ytd(rows: list[dict[str, Any]], window: dict[str, Any]) -> list[dict[str, Any]]:
    if not rows:
        return []
    year = str(window.get("year") or _date_of(rows[-1])[:4] or "")
    if not year:
        return []
    return [row for row in rows if _date_of(row).startswith(year)]


_KINDS: dict[str, Callable[[list[dict[str, Any]], dict[str, Any]],
                           list[dict[str, Any]]]] = {
    "last_n_days": _last_n,
    "range": _range,
    "ytd": _ytd,
}


def window_kind(window: Any) -> str:
    return str((window or {}).get("kind") or "") if isinstance(window, dict) else ""


def apply_window(rows: list[dict[str, Any]] | None,
                 window: dict[str, Any] | None) -> tuple[list[dict[str, Any]], str]:
    """Return ``(rows, gap)``; empty ``gap`` means "use these rows"."""
    rows = [row for row in (rows or []) if isinstance(row, dict)]
    if not rows:
        return [], "too_few_points"
    kind = window_kind(window)
    if not kind:
        return rows, ""
    handler = _KINDS.get(kind)
    if handler is None:
        return [], "bad_window"
    kept = handler(rows, window if isinstance(window, dict) else {})
    if len(kept) < MIN_POINTS:
        return [], "too_few_points"
    return kept, ""
