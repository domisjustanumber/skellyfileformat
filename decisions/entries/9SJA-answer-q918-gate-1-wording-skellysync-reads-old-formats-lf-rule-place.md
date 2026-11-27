# 9SJA — Answer Q918: gate 1 wording, skellysync reads old formats, the place of the LF rule

**Status:** accepted, 2026-11-27 (user; answer Q918 of the owner session of 2026-11-27, "agree to all").

## Decision

The owner accepted the recommendation of each part of Q918.

1. The Scope section of `recording-files/README.md` agrees with `SPEC.md`: SFF-896 to SFF-903 have
   gate 1 approved on 2026-11-25, and they keep the draft form until gate 2
   ([ADR-X7QP](../../recording-files/decisions/entries/X7QP-gate-1-approval-of-the-v1-camera-file-rules.md)).
   This is a correction of a stale text. It changes no rule.
2. New skellycam, skellysync and freemocap keep reading each recording format that freemocap
   v1.0.25 to v1.8.2 and the current code write. Legacy annex section 8 names skellysync. skellysync
   is the only converter of old recordings, so it must read them
   ([ADR-A8Y2](A8Y2-skellysync-is-the-only-converter-of-old-recordings.md),
   [ADR-SY2H](../../recording-files/decisions/entries/SY2H-answers-q858-to-q861-converter-cases-and-legacy-readers.md)).
3. The LF rule of [ADR-NB40](NB40-lf-line-ends-for-each-text-file.md) is not copied into
   `AGENTS.md`. `.gitattributes` enforces it. NB40 stays `accepted`.

## Reason

- Item 1: the README still said "a draft for gate 1" after gate 1 closed.
- Item 2: the annex bullet named only skellycam and freemocap.
- Item 3: a copy in `AGENTS.md` adds text and no check. The tool setting is enough.
