# KJ91 — `NV12` is a value of `capture_format`

**Status:** absorbed into [`SPEC.md#13-capture-info-json`](../../SPEC.md#13-capture-info-json), [`conformance.md#camera-files-section-6`](../../conformance.md#camera-files-section-6), [`conformance.md#capture-info-processing-info-and-calibration-sections-13-to-15`](../../conformance.md#capture-info-processing-info-and-calibration-sections-13-to-15), 2026-11-25 (commit on dom/nv12-capture-format; was accepted, 2026-11-25 (user; answer Q808 of the owner session of 2026-11-25)).

## Decision

1. The member `requested.capture_format` of a camera config of the capture info JSON (section 13,
   SFF-800) has the values `MJPG`, `YUYV` and `NV12`.
2. A take from a camera that sends raw frames records the format of those frames: `YUYV` for a
   YUY2 mode, `NV12` for an NV12 mode. The capture writer encodes each raw frame to JPEG (SFF-734).
3. SFT-712 also runs a raw source in `NV12` and checks the recorded `capture_format` of each raw
   source. SFT-735 checks that each `capture_format` is one of the three values.

## Reason

- skellycam opens a raw mode when a camera has no MJPG mode at 30 fps or more at the requested size
  (skellycam answer Q807 of 2026-11-25). Some cameras give NV12 and no YUY2 at that size.

## Consequences

- No golden folder changes: each golden capture info JSON has `MJPG`.
- A writer that wrote another value now fails SFT-735.
