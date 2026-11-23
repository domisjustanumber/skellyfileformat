# G9ER — Consolidation of the pushed entries whose rules changed

**Status:** absorbed into
[`README.md#scope-normative`](../../README.md#scope-normative),
[`README.md#compatibility-promise-normative`](../../README.md#compatibility-promise-normative),
[`README.md#versioning-normative`](../../README.md#versioning-normative),
[`README.md#implementations`](../../README.md#implementations),
[`recording-files/AGENTS.md#1-purpose`](../../AGENTS.md#1-purpose),
[`spec/SPEC.md#skellyspecs-recording-format-specification`](../../SPEC.md#skellyspecs-recording-format-specification),
[`spec/parts/parquet-descriptor.md#sensorgroup-closed`](../../parts/parquet-descriptor.md#sensorgroup-closed),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q129 and Q155: one
consolidation entry supersedes the changed entries and changes no rule; an agent wrote the
restatements; commit to main)).

## Decision

This entry supersedes in full the pushed entries 3D33, 5XNA, 92TM, 9DV4, G1YG, KW3G, N6HS, P76Y,
Q9X2 and VPD9 ([ADR-H2HQ](H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 6,
[ADR-HH7B](../../../decisions/entries/HH7B-absorb-documents-and-clean-up-timing.md) item 2). A later entry changed a rule of
each of them. It changes no decision. An agent wrote the restatements. A citation of one of their
items means its rule here.

**Kept rules.** Each heading states the rules of the items that its line names. For an item that
"Changed rules" also names, the heading states the rule as changed.

- README [Scope](../../README.md#scope-normative): 92TM 1.
  [Compatibility](../../README.md#compatibility-promise-normative): 9DV4 5; 92TM 1.
  [Versioning](../../README.md#versioning-normative): 9DV4 1, 2, 4, 6, 7, 8, 9.
  [Implementations](../../README.md#implementations): 92TM 2.
- [AGENTS.md 1](../../AGENTS.md#1-purpose): VPD9 1.
- [§1](../../SPEC.md#1-scope-and-terms): 5XNA 2; 3D33 and VPD9 (preambles).
- [§2](../../SPEC.md#2-conventions): N6HS 2; VPD9 1, 5.
- [§3](../../SPEC.md#3-versioning): 9DV4 1, 3, 4, 6, 8; VPD9 2.
- [§4](../../SPEC.md#4-the-take-folder-layout-and-names): 5XNA 1 to 4, 9, 10; 92TM 1; VPD9 3, 4
  and the file names (preamble).
- [§5](../../SPEC.md#5-the-recording-manifest): 3D33 1, 10; 5XNA 2, 6, 7, 8; N6HS 2.
- [§6](../../SPEC.md#6-camera-files): VPD9 10.
- [§7](../../SPEC.md#7-csv-timing-sidecars-common-rules): 5XNA 5; G1YG 6; VPD9 5.
- [§8](../../SPEC.md#8-video-timing-sidecar): N6HS 2; VPD9 4, 5, 6 (the flag `encode_skip`
  replaces the log message as guidance for programs, ADR-Z641 item 1) and the two keys (preamble).
- [§9](../../SPEC.md#9-audio-file): 92TM 1, 2, 3, 4, 6, 10; VPD9 11.
- [§10](../../SPEC.md#10-audio-timing-sidecar): 92TM 5, 6, 11; N6HS 2; VPD9 7.
- [§11](../../SPEC.md#11-clocks-the-fit-and-reader-timing): 92TM 5, 7, 8; N6HS 2; VPD9 8, 9.
- [§12](../../SPEC.md#12-writing-crashed-files-and-repair): 92TM 1, 8, 9; G1YG 1 to 9; KW3G
  16; Q9X2 2 (its file rules), 5; VPD9 12.
- [§13](../../SPEC.md#13-capture-info-json): 3D33 2; 92TM 5; N6HS 1, 2; VPD9 `user_name`
  and the link by `camera_key` (preamble).
- [§14](../../SPEC.md#14-processing-info-json): 3D33 3; N6HS 1.
- [§15](../../SPEC.md#15-calibration-toml): 3D33 4; N6HS 2 to 7.
- [§16](../../SPEC.md#16-tracking-parquet): 3D33 5; N6HS 9; P76Y 1 to 8; VPD9 1.
- [Descriptor `SensorGroup`](../../parts/parquet-descriptor.md#sensorgroup-closed): 3D33 5.
- [§17](../../SPEC.md#17-realtime-journal): G1YG 6; Q9X2 1 to 8 (items 2 and 7 as guidance
  for programs, [ADR-Z641](Z641-program-guidance-gate-2-scope-and-no-push.md) item 1); VPD9 13.
- [§18.1](../../SPEC.md#181-blender): 3D33 6. [§18.2](../../SPEC.md#182-annotated-videos):
  3D33 7. [§18.3](../../SPEC.md#183-exports): 3D33 8; P76Y 9.
  [§18.4](../../SPEC.md#184-logs): 3D33 9.
- [§19](../../SPEC.md#19-skellysync-folders): KW3G 15; VPD9 14.
- [§20](../../SPEC.md#20-opening-a-folder): 3D33 10; 5XNA 11; KW3G 5, 8.
- [§21](../../SPEC.md#21-legacy-folders): 3D33 11; 5XNA 11; N6HS 8.
- [§22](../../SPEC.md#22-privacy-and-safety): 3D33 12; KW3G 6.
- [§23](../../SPEC.md#23-the-reader-result): 3D33 13; KW3G 1 to 14.
- [Appendix A](../../SPEC.md#appendix-a-golden-folders): 3D33 14.
- [Appendix B](../../SPEC.md#appendix-b-player-guidance-informative): 92TM 1, 10, 12.

**Changed rules.** The spec cites the entry that changed each rule, next to the rule.

- 3D33 item 4: in a manifest rebuild, a reader uses `<rec>_camera_calibration.toml`. Item 5: the
  ChArUco source is `charuco_detector:<squares_x>x<squares_y>`.
- 5XNA item 8: a rebuild tests exact names, not a suffix. Item 11: a take exists for each
  `take_uuid` of a device pair. A folder with a file of this format and no take is `unreadable`.
- 92TM item 10: a program that decodes the audio drops the pre-skip and applies no output gain. The
  Python reader does not decode.
- 9DV4 items 3 and 6, VPD9 item 2: the files of SFF-707 hold the version fields and `writer`. A
  media file holds none. `format_prerelease` is 1, and from the external review each revised draft
  adds 1.
- G1YG item 7: skellycam asks about a take that it recorded on its own. freemocap asks one time for
  the whole take. A manifest in the state `recording` also gives the question. A program also asks
  at start-up. Nothing changes before the user agrees. Item 8: an interrupted repair leaves the
  manifest in the state `recording`. Some sidecars can be `repaired`. A new repair finishes the
  rest.
- KW3G item 4: the file warnings also have `gap`. Item 7: a folder file is in `folder_files`.
  Item 8: a timing sidecar alone is not a camera file or an audio file. A refused pair counts as a present file.
- N6HS item 3: a change of the geometry also gives a new `calibration_uuid`.
- P76Y item 8: the result holds only the code `realtime_run`. The text and the badge are guidance.
- Q9X2 item 5: no program folds a journal at start-up before the user agrees.
- VPD9 item 4: four forms of the identity string. Item 6: bit 3 `repeat`, and bit 1 `filled` is
  provisional. Item 12: the repair line has `media_cut_bytes`. The lock covers only whole-file
  writes, and skellycam also holds it.

## Reason

A pushed entry changes only by the allowed edits, so a new entry restates its rules.

## Open work

G1YG item 10, the desk test of a replace on Windows ([open-work.md](../open-work.md)).

_Edited 2026-11-17 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
