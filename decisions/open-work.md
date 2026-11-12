# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Format decisions as entries.** The format decisions of skellycam's plan
  (`research/CAPTURE_AND_RECORDING_PLAN.md` on the `dom/research` branch of the skellycam fork:
  D15 to D19, S1 to S10, and the format parts of D21) must become entries in this log. Each entry
  goes to Historical as absorbed when `spec/SPEC.md` or `README.md` states all of its rules.
- **Spec v0 and its conformance list.** `spec/SPEC.md` and `spec/conformance.md` hold only headings.
  Write them, then stop for the review of the user (gate 1).
- **Provisional parts of spec v0.** Mark these parts provisional in `spec/SPEC.md`. Close each of
  them before v2.0.0: the fields that wait for the audio clock drift test and for the Linux and
  macOS audio timing test, and the skellysync camera sidecar header, which waits for the skellysync
  decisions D-Q, D-FPS, D-HDR and D-DRIFT.
