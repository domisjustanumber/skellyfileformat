# 5G42 — Four names of spec draft v1 confirmed at gate 1: the repair record, the audio label, the audio latency key and RFC 8785

**Status:** superseded by [G1YG](G1YG-writing-crash-reading-and-repair.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. A repaired file has a `freemocap.repair` Metadata record, with the keys `cut_bytes` (the number
   of bytes that the repair removed) and `repair_writer` (the writer string of the program that
   repaired the file). A reader reports the state `repaired` when a file has this record.
2. The audio Channel `metadata` has the key `label`, with the rules of `camera_label`. The same
   label is in the topic.
3. The optional, provisional key `audio_latency_ns` is in the audio Channel `metadata`, not in
   `freemocap.recording`.
4. The reader result is serialised with the JSON Canonicalization Scheme (RFC 8785).

## Reason

- Without the repair record, a reader cannot tell a repaired file from a file that finished
  normally. A repair changes the file of the user, so a reader must be able to show it.
- The latency belongs to one microphone, and the audio Channel describes one microphone.
- The golden files compare the results of the Python and the JavaScript readers byte for byte. A
  canonical form makes the bytes equal.

## Evidence

- skellycam `dom/research` (local commit, not pushed):
  `research/skellycam_recording/docs/spec_v1_review_20261113.md` (the answers of the user).

## Alternatives rejected

- No repair record: a repaired file looks the same as a finished file.
- `audio_latency_ns` in `freemocap.recording`: the record is the same in each file of a take.
- Compare the results as parsed JSON: the golden files are not byte-stable.
