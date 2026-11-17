# 3GWN — Jitter in the G5 audio rows after the cut

**Status:** absorbed into
[`golden/CAPTURE_VECTORS_CHOICES.md#5-g05`](../../golden/CAPTURE_VECTORS_CHOICES.md#5-g05),
[`tools/tests/test_g_capture.py`](../../tools/tests/test_g_capture.py),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; question Q153 of the review of the golden folders; commit
to main)).

## Decision

The `adc_ns` values of the G5 audio sidecar get a small timing jitter in the rows after the cut:
the rows whose block is not in `records` (SFF-792). So the reader fit from all usable rows
([ADR-64ER](64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) item 2) and a fit
from only the rows in `records` give different `fitted_ns`. G05 and G06 are made again. This is a
change of the golden files of the same kind as the slow record of G13
([ADR-158N](158N-details-for-the-decisions-of-round-3.md) item 11).

The size, the pattern and the rows of the jitter are a proposed choice
([ADR-SM53](SM53-choices-for-the-decisions-of-round-7.md) item 4).

## Reason

Before this entry, the G5 `adc_ns` values were exactly linear. So the two fits gave the same
`fitted_ns`, and a reader that applied ADR-64ER item 2 incorrectly passed. The user answered "yes"
to the jitter on 2026-11-17.

## Consequences

- In G05, the audio sidecar, the expected results and the truth files change in both cases.
- No byte of G06 changes. The repair removes the rows with the jitter, and the fit of each case of
  G06 uses only the 9 kept rows. Each changed value keeps its number of digits, so `cut_bytes` of
  the audio repair does not change.
- `tools/tests/test_g_capture.py` checks that a fit from only the rows in `records` gives other
  `fitted_ns` than the expected results.

## Open work

See [open-work.md](../open-work.md).
