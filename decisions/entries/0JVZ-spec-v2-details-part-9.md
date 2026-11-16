# 0JVZ — Spec draft v2 details, part 9: prerelease number, result scopes, golden layout

**Status:** absorbed into [`spec/SPEC.md#3-versioning`](../../spec/SPEC.md#3-versioning),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/SPEC.md#appendix-a-golden-folders`](../../spec/SPEC.md#appendix-a-golden-folders),
[`spec/SPEC.md#layout-and-cases`](../../spec/SPEC.md#layout-and-cases),
[`spec/conformance.md#how-to-read-a-test`](../../spec/conformance.md#how-to-read-a-test),
[`spec/conformance.md#clocks-the-fit-and-reader-timing-section-11`](../../spec/conformance.md#clocks-the-fit-and-reader-timing-section-11),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

A second independent review found points that stop a golden folder with a byte-for-byte expected
result. Parts 9 to 15 proposed one resolution for each. "Basis" and "CHOICE" have the meaning of
[ADR-W6HV](W6HV-spec-v2-details-part-3.md). The user accepted items 20 to 22 on 2026-11-16. Items
20 and 21 are the own choice of the user, not the first proposal.

20. **Prerelease number** (SFF-710; SFT-703; each golden folder). The user: "start at 1 until I say
    it's going for external review". `format_prerelease` is 1 for this draft and through the
    internal drafts: a draft change does not change it. Only SFF-710 states the value. The
    value after the user sends the draft to external review is not decided. Each file of each
    golden folder has the warning `prerelease`. G10 gets the case `prerelease_0`: a copy of G1 in
    which each file has `format_prerelease` 0, with no such warning. First proposal (not used): 3, plus
    1 for each changed draft. Its alternative: 1.

21. **Result scopes** (SFF-885, SFF-892; SFT-727, SFT-729, SFT-768, SFT-769). The user: "the goal
    is the same result regardless of js or python".
    - a. A reader gives its result for a scope. `full` is the whole result, as the Python reader
      gives it. `player` is the result for the files that a player needs: the media files, the
      timing sidecars and the JSON files. A reader that is asked for `player` gives exactly the
      `player` result, whichever reader it is. The Python reader has the two scopes:
      `read_folder(path, records=False, scope="full")`. The JavaScript reader has only `player`.
      The result gets no `scope` member.
    - b. The JavaScript command is `node js/bin/read-folder.mjs <folder> [--records]`. It writes
      the canonical JSON to standard output, and no other byte. The `scope` argument and the
      switch are new in [ADR-G21H](G21H-gate-2-tests-location-and-interfaces.md) item 2.
    - c. The `player` result is the `full` result with only these changes. `folder_files`: an
      item of a TOML, a Parquet, a journal, an NPY file or an NPZ file that exists is
      `not_checked`, with `reason` null and `warnings` `[]`. The three integers of the journal
      item are null. A `missing` item stays `missing`. No NPY header is read. `links`: `frames`
      (also its row-count part), `dimensions`, `hashes` and `calibration` are `not_checked`. The
      other checks have only the parts of item 31 that need no TOML, Parquet or journal. No take
      has `stale_processing_info`, `calibration_mismatch` or `realtime_run`. The mark of SFF-875
      is found only in a timing sidecar, a JSON file and a media file of a device pair. A TOML,
      a Parquet or a journal in no `folder_files` list is `not_in_format` in `other_files`, with
      no `orphan_file`. `legacy`: `family` and `calibration` do not change. For `v1`, no era
      signal is read: `release_range` is `["v1.0.25","v1.8.2"]`, `ambiguous` is true, `eras` is
      `[]`, and the four warnings of SFF-879 apply.
    - d. Each case (item 22) has two committed results, with `records`: one for each scope. The
      Python reader gives the bytes of each. The JavaScript reader gives the bytes of `player`.
    - e. SFT-729 takes the fit values from `audio_details` of the Python reader. A `player`
      result shows the fit through `fitted_ns` (item 35).

    First proposal (not used): one result for each reader, and no test compares the two. Its
    alternative: one result, and the test removes the members that differ.

22. **Layout of the golden folders** (Appendix A). A case is one folder `golden/G<NN>/<case>/`,
    with two digits in `<NN>`: a take folder or a legacy folder. A case name has only `a` to `z`,
    `0` to `9` and `_`. It is not the `<rec>` of the take. The results are beside the case folder:
    `<case>.full.json` and `<case>.player.json`. `golden/G<NN>/SHA256SUMS` lists each file. The cases:
    - G1 to G4, G12, G13, G16: `take`. G4 has four cameras. G12 has four cameras and audio with a
      fit: camera 0 has two segments and a source frame gap, camera 1 a `period_ps` with a
      remainder, camera 2 no fit, and camera 3 two equal fitted times and an `encode_skip` row.
    - G5: `audio_clean_kill` and `audio_torn_fragment`. Each has three cameras (0: a clean cut; 1:
      a torn row of 37 bytes; 2: a row with a wrong CRC), the `.tmp` manifest and the old manifest.
    - G6: `repaired` and `interrupted_repair`, from `audio_torn_fragment`.
    - G7: `no_manifest`, `other_take_manifest`. G8: `renamed`.
    - G9: `take_uuid`, `camera_key`, `frame_range`, `row_counts`, `dimensions`,
      `rotation_in_configs`, `unresolved_file`, `stale_parquet_sha256`, `calibration_hash`,
      `calibration_uuid`, `recording_id`.
    - G10: `higher_minor` (G3 with `2.1` in each version field; `x_future` as the last header key
      and as a column before `crc32` in each sidecar, and as a member of the manifest and of the
      info JSONs), `unknown_major_sidecar` and `unknown_major_folder_file` (G1 with `3.0` in one
      video sidecar; in the capture info JSON), `higher_minor_journal` (item 47) and
      `prerelease_0`.
    - G11, each a copy of G1 with one changed video sidecar: `leading_zero`, `plus_sign`,
      `row_integer_2_53`, `rate_0_1`, `rate_2_20_plus_1`, `rotation_45`, `bad_label`,
      `missing_key`, `unknown_clock`.
    - G14: `calibration_take`, `mocap_take`, and the folder `library/`, which is not a case.
    - G15: `v1a`, `v1b_v1d`, `v1b_v1c`, `v1e_v1h`, `v1f_v1h`, `v1g_v1h`, `v1h`, `v1h_prime`,
      `v1i`, `two_chains`, `no_signal`, `v0_0_x`, `v0_1_0`, `mp4_only`.

    Basis (3).

## Reason

- Without these items, two generators give different golden bytes.

## Evidence

skellyfileformat at fe7deba: the examples of `spec/SPEC.md` had `format_prerelease` 3.

## Open work

[open-work.md](../open-work.md)
