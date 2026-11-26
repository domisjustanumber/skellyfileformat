# A8Y2 — skellysync is the only converter of old recordings

**Status:** absorbed into [`recording-files/README.md#implementations`](../../recording-files/README.md#implementations), [`recording-files/SPEC.md#1-scope-and-terms`](../../recording-files/SPEC.md#1-scope-and-terms), [`recording-files/conformance.md#how-to-read-a-test`](../../recording-files/conformance.md#how-to-read-a-test), [`recording-files/conformance.md#the-stage-of-each-test`](../../recording-files/conformance.md#the-stage-of-each-test), [`recording-files/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap`](../../recording-files/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap), 2026-11-26 (commit on dom/v1-player-rules; was accepted, 2026-11-26 (user; answer Q848 of the owner session of 2026-11-26)).

## Decision

1. **Q848.** The owner wrote: "the skellyspecs texts that mention converting old recordings name
   only skellysync as the converter."
2. Each text of this repository that names a converter of old recordings names only skellysync.
   skellycam plays old recordings as they are and converts no recording
   ([ADR-46NQ](46NQ-old-recordings-play-as-they-are-no-upgrade-converter.md)).
3. The conversion writer of SPEC.md section 1 is skellysync. "The converter" of `conformance.md` is
   `TakeWriter` of the test adapter in a conversion, and it stands for the converter of skellysync.
4. This entry changes no requirement, no test, no mark and no golden file. The mark of the
   converter cases is a separate choice of the agent
   ([ADR-VS9Z](../../recording-files/decisions/entries/VS9Z-converter-cases-keep-the-mark-stage1a.md),
   proposed).

This entry adds to 46NQ. It supersedes no entry. A decided entry that names "the skellycam
converter" is historical, and it stays as it is.

## Reason

- 46NQ removed the converter of skellycam, but SPEC.md section 1 and the stage text of
  `conformance.md` still named "the skellycam converter" and "its converter".
- One converter of old recordings keeps one place for the conversion rules.

## Alternatives rejected

- Name no converter: the term "conversion writer" then has no program, and SFF rules that say "a
  conversion writer MAY" have no subject.
