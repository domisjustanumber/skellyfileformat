# 94YQ — Review of golden folder G1: file warning `gap`, `DefaultDuration`, G1 conventions, camera matching

**Status:** absorbed into
[`spec/SPEC.md#6-camera-files`](../../SPEC.md#6-camera-files),
[`spec/SPEC.md#8-video-timing-sidecar`](../../SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#20-opening-a-folder`](../../SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`golden/README.md#golden-folders`](../../golden/README.md#golden-folders),
[`golden/G01_CHOICES.md#choices-made-for-g1-that-the-spec-does-not-give`](../../golden/G01_CHOICES.md#choices-made-for-g1-that-the-spec-does-not-give),
[`tools/tests/test_goldgen.py`](../../../tools/tests/test_goldgen.py),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; review of golden folder G1)).

## Decision

Each item has its reason.

1. **The file warning `gap`.** A reader gives a camera file the file warning `gap` when one or more
   usable rows have the flag `gap`, in the same way as the file warning `encode_skip` (SFF-887,
   SFT-717, SFT-768). Camera 1 of each case of G1 has a gap, so its `warnings` are
   `["gap","prerelease"]` in each expected result. This entry is the decision entry that
   `AGENTS.md` section 4 needs for this change of the golden files: the four result files and
   `SHA256SUMS` of G1 change, and no other golden file changes. The generator derives the warning
   from the rows. Reason: `camera_gap` is only a manifest warning that skellycam writes, so the
   reader result showed no sign of a gap.
2. **`DefaultDuration` is rounded down.** In SFF-736, the `DefaultDuration` of a camera file is
   ⌊10^9 × `den` / `num`⌋ ns, where `num/den` is the nominal rate: 33,366,666 for 30000/1001. The
   block timestamps of SFF-736 do not change: they stay rounded half up. Reason: the pinned FFmpeg
   (through PyAV) writes this value, and the writer uses that tool.
3. **`prerelease` and the manifest.** The manifest is never an item of the reader result, so its
   `format_prerelease` shows nowhere in the result. This is accepted as it is (SFF-891). Reason:
   each other file of the take has the warning.
4. **`frames` with no Parquet.** When a take has no Parquet, the row-count part of `frames` alone
   decides the check. For the scope `full`, it is `ok` when the finished camera files have equal
   row counts. For the scope `player`, it is `not_checked` (SFF-872). Reason: the text gave this
   result only by inference.
5. **The conventions of G1.** The other choices of
   [golden/G01_CHOICES.md](../../golden/G01_CHOICES.md) are accepted as the conventions that the
   later golden folders copy: each item except 23 and 30 (items 1 and 2 replace them). Items 3 and
   4 confirm its items 20 and 22. The user named three: the golden files name their writer
   `skellyfileformat-goldgen 1.0.0`; a JSON file of the format in a golden folder has an indent of
   2 spaces and one LF at the end; and the fit of G1 is the exact line that made the rows. These
   are conventions of the golden folders. This entry makes none of them a rule of the format.
   Reason: [ADR-G21H](G21H-gate-2-tests-location-and-interfaces.md) item 5 wants one approved
   example before the other folders copy it.
6. **Camera matching after the calibration check** (a separate decision of the same day). It adds
   to [ADR-70VP](70VP-camera-identity-forms-and-remembered-keys.md) item 2. The user said: "the
   user prompt for matching non-unique cameras must come after there has been a calibration check
   to see where the cameras are and suggest most likely matching candidates." and "For now FMC adds
   the extra step to suggest camera matches from calibration, skellycam does not." So: when
   freemocap runs and a calibration applies, freemocap first checks from the calibration where the
   cameras are. Then it asks the user, with the most likely candidates first. skellycam alone does
   not make this check: it asks with no suggestion (SFF-752). Reason: the camera positions tell
   apart cameras that the OS cannot tell apart, and only freemocap has a calibration.

## Consequences

- Each golden case that copies G1, and each other case with a `gap` row, gets the file warning
  `gap`.
- A writer that does not use FFmpeg must also round `DefaultDuration` down.
- freemocap needs the code change that [open-work.md](../open-work.md) lists.
- Four choices of G01_CHOICES.md (items 13, 14, 15 and 24) could be rules of the format.
  [ADR-W389](W389-format-rules-from-the-golden-conventions.md) decided them (corrected on 2026-11-17).

## Evidence

For item 2, measured on 2026-11-16 on the reference platform with av 19.0.2 (FFmpeg 9.0.2):
`test_mkv_default_duration_rounds_down` of `tools/tests/test_goldgen.py` muxes a camera file with
the rate 30000/1001. Its `DefaultDuration` is 33,366,666, and each block timestamp is the half-up
value of SFF-736. A one-off run with the rates 30/1, 24000/1001, 15/2 and 120/1 gave the same two
results.

For item 1: after `tools/make_golden.py --only G01`, `git diff --stat` shows only the four result
files and `SHA256SUMS`. Each media file, sidecar, manifest, capture info JSON and truth file keeps
its bytes and its sum.

## Alternatives rejected

- Item 1: a take warning from the manifest `camera_gap`. A reader then trusts a value that another
  program wrote, and a take with no manifest shows nothing.
- Item 2: keep "half up" and patch the element after the mux. The writer then has code that its
  tool does not need, for a difference of 1 ns.
- Item 3: a take warning `prerelease`. It repeats what each file item shows.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
