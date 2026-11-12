# CD4G — Spec first, and the rules of this repository

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. **Spec first.** For each part of the format: write the spec text and the conformance test list;
   the user reviews them (gate 1); write the runnable tests and the golden files; the user reviews
   them (gate 2); then write the implementation.
2. **Normative documents.** `README.md`, `spec/SPEC.md` and `spec/conformance.md`.
3. **IDs.** A requirement has an ID `SFF-NNN`, and a test has an ID `SFT-NNN` that cites the
   requirements that it checks. An ID is not reused or renumbered. A removed item stays, marked
   withdrawn. `tools/check_spec_traceability.py` checks the links.
4. **Golden files.** They are committed with their SHA-256 sums and the script that made them. A
   change to a golden file needs an entry.
5. **Repository.** Public, on the account of the owner for now. Apache-2.0 for code and CC-BY-4.0
   for the spec text. Commits go to `main` directly until v2.0.0 is released.
6. **Spec v0.** It covers only the new format: the MKV profile, the video timing sidecar, the
   `.skau` and its packet table, the skellysync FLAC track, embedding and finalisation, the Segment
   UID and the live and final offsets, unfinalised and crashed files, the names, and how to find a
   file that is not in this format. Some parts are provisional
   ([open-work.md](../open-work.md)). Each provisional part must be closed before v2.0.0.
7. **Versions of dependencies.** Each one is pinned exactly, to a release that is at least 14 days
   old.

## Reason

- The user wants an agreed contract before code. An early prototype of a skellycam part was written
  before any spec, and it had to be put aside.
- A golden file that a script can change is not a fixed reference for other implementations.

## Evidence

- Plan rows D22 and D23 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.
