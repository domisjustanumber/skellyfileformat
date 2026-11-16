# 72QQ — Spec draft v2 details, part 8: tests with no Pass text, and the open points of E45D

**Status:** proposed, 2026-11-16 (agent; ambiguous points from the independent review).

## Decision

This part holds items 18 and 19 of the proposals that [ADR-W6HV](W6HV-spec-v2-details-part-3.md)
introduces (items 1 and 2, and the meaning of "Basis" and "CHOICE"). The other parts are
[ADR-Q4BK](Q4BK-spec-v2-details-part-4.md) (3 and 4), [ADR-0XX2](0XX2-spec-v2-details-part-5.md)
(5 to 8), [ADR-ATW0](ATW0-spec-v2-details-part-6.md) (9 to 13) and
[ADR-DM9S](DM9S-spec-v2-details-part-7.md) (14 to 17). Item 19 is not from the independent review.

18. **Tests for requirements with no Pass text.** No new ID is necessary.
    - SFF-720 (`cam<N>`): SFT-705, with a converter run; SFT-763 (the G3 copy with key 0).
    - SFF-734 (no H.264): SFT-712, with a request for H.264 capture that the writer refuses.
    - SFF-736 (rates above 1000): SFT-711, with a nominal rate of 1001/1 that the writer refuses.
    - SFF-751 (direction): SFT-718 with G4. The rotated frame has the upright corner colours of G4.
    - SFF-764 (flush): SFT-720, with a trace of the write calls, and `mfra` at the end.
    - SFF-768 (`overflow`): SFT-722, with a simulated input overflow.
    - SFF-756 (`encode_skip`): SFT-717, with a forced encoder failure; SFT-768, with a new vector in
      G12. `filled` and `repeat`: SFT-717 (the `filled` check is provisional, item 2c).
    - SFF-752 (key): SFT-717, against the `device` values of the capture info JSON.
    - SFF-782: SFT-728, with a new vector in G12 of two rows with equal fitted times.
    - SFF-824 (reader): SFT-706 with G8 as a renamed G3; SFT-763 with a new G9 vector. A wrong
      `recording_id` makes the Parquet item `invalid`, with `take_fact_mismatch`.
    - SFF-830 (`camera_plane`): SFT-749, with freemocap processing of one camera of G1.
    - SFF-869 (`extra_files`): SFT-762, with G3 and a third camera pair of the same take.
    - `empty` and `unreadable`: SFT-768. The test makes an empty folder, and a folder with only one
      timing sidecar of G1. No golden folder is necessary.

19. **Points left open by [ADR-E45D](E45D-spec-draft-v2-corrections-after-review.md).** The current
    spec text is the proposal, unless a point gives a different proposal. Each point is a CHOICE.
    - a. CHOICE. In SFF-885, the journal item gets the members `records` (the number of good
      records) and `rejected_records`, beside `torn_bytes`. Each of the three is null when the
      journal is `not_checked` (SFF-892). A hole of zeros, for example of 4 KiB, is not a rejected
      record. Only a record with a correct `magic` and a wrong `length` or `crc32` is rejected.
    - b. CHOICE. A journal with a torn tail, or with no end record, is `unfinished`. When a record
      is also rejected, the journal is `damaged`. A record that is rejected for a wrong `length`
      also has the reason `crc_mismatch`. This is the text of SFF-843.
    - c. CHOICE. With fewer than two usable rows, or a `period_fs` that is not greater than 0, a
      reader computes no audio fit and maps no sample to take time. This is the text of SFF-784. A
      row with the flag `silence` is a usable row for the fit.
    - d. CHOICE. The annotated videos and the 3D models of a run N other than 0 keep the old
      general pattern, which is the text of SPEC.md section 18: the folder `run-<N>/`, and
      `.run-<N>` before the last suffix. An example is
      `annotated_videos/run-<N>/<rec>.<camera_label>.annotated.run-<N>.mp4`.
    - e. CHOICE. `selected_run_id` is in the processing info JSON and in the Parquet descriptor now.
      A change of the selection then rewrites the Parquet. Proposal: the processing info JSON is
      the only home, and the descriptor loses the member.
    - f. CHOICE. freemocap rewrites the times of a realtime run after a repair (SFF-833). It does
      this when it next opens the take and finds that a sidecar has a `# repair` line and a fit that
      the run did not use.
    - g. CHOICE. No other file of SPEC.md section 18 holds version fields. Only the export inventory
      and the BVH metadata JSON hold them, as
      [ADR-E45D](E45D-spec-draft-v2-corrections-after-review.md) item 3 says.

## Reason

- Item 18: each requirement needs a test with a Pass text that checks it.
- Item 19: [ADR-E45D](E45D-spec-draft-v2-corrections-after-review.md) left these points to the
  user. The spec holds the smallest text for them. A proposal for each lets the user decide them
  together with the other parts.
- 19a: a hole of zeros has no `magic`, so the scan of SFF-843 finds no record in it.
- 19e: a change of the selected run must not replace the Parquet, because the SHA-256 of the
  Parquet is in the processing info JSON and in each export inventory.
- 19f: freemocap owns the Parquet. skellycam, which can do the repair, writes no Parquet file.

## Consequences

- 19e removes `selected_run_id` from the descriptor of parts/parquet-descriptor.md. A reader of the
  Parquet alone then does not know the selected run.
- 19a changes the committed reader result of G13.

## Open work

[open-work.md](../open-work.md)
