# `window.py` — time windows as data selection

One pure function, one table of kinds. Adding a new window ("last week", "this
year") is a row in `_KINDS`, not an `if` in every chart caller, and the renderer
never sees a window.

```python
kept, gap = apply_window(rows, {"kind": "last_n_days", "value": 20})
if gap:                     # "bad_window" | "too_few_points"
    write_gap_into_answer(gap)
```

- `last_n_days` keeps the tail, clamped to 2…500;
- `range` is inclusive on both ends and skips rows without a date;
- `ytd` defaults to the year of the last row;
- fewer than `MIN_POINTS` rows is a **gap**, never an exception — the caller turns
  it into a visible shortfall instead of an empty chart.

This is the smallest piece of the chart package that can be lifted out and read in
one sitting; the rest (spec, resolve, renderers) lives in the private repository.

```bash
python -m pytest examples/window/test_window.py -q
```
