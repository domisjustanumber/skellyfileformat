# Decision log

This log records the technical decisions of skellyfileformat, with their reasons and evidence. Read this
file and [open-work.md](open-work.md) before you change the spec, the README, the golden files, the tools or the agent instructions. The
[Rules](#rules) tell you which entries to read
([ADR-0001](entries/0001-decision-log-agents-md-and-private-data.md)).

Each entry gives the decision, its reason, the evidence (when there is evidence), the alternatives
rejected and a "Not repeated" section for pitfalls already found. When a decision changes, add a new
entry that supersedes the old entry in full. The body of a decided entry changes only by the edits
that the [Rules](#rules) allow. To write an entry, use [template.md](template.md).

## Index

### Active

These entries are `accepted` or `evidence`.

| # | Decision | Status |
|---|----------|--------|
| [0001](entries/0001-decision-log-agents-md-and-private-data.md) | Decision log and its rules; `AGENTS.md` files hold the instructions; `plans/` is local; no private data | accepted |
| [2C9V](entries/2C9V-whole-take-folder-scope-and-package.md) | The format is the whole take folder; every file fully specified, incl. other formats by content mapping; one package; JS reader for player needs | accepted |
| [5XNA](entries/5XNA-folder-layout-names-and-manifest.md) | Folder layout and fixed names; folder renamable, files not; `<rec>` prefix; `recording_manifest.json` with links, warnings, privacy, summary | accepted |
| [6RSB](entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) | Camera files: MJPEG MKV with index timestamps; one CSV timing sidecar per file; `camera_key` link key; fit in the sidecar; player time | accepted |
| [92TM](entries/92TM-opus-audio-in-fragmented-mp4.md) | Audio: Opus (libopus) in fragmented MP4 with 1 s fragments, one CSV sidecar; silence for gaps; fit for timing; crash read and clean-up rules | accepted |
| [9DV4](entries/9DV4-format-version-from-freemocap.md) | Format version = major.minor of the freemocap release that last changed the folder; package and skellycam in step; version in each file | accepted |
| [CZQ9](entries/CZQ9-read-old-write-new-and-legacy-recognition.md) | Old recordings stay readable; new programs write only this format; the spec recognises v1 folders by era; pre-v1 unsupported; legacy annex | accepted |
| [G1YG](entries/G1YG-writing-crash-reading-and-repair.md) | Whole files via `.tmp` and replace; live files append and flush; crashed files read in place; repair only after the user agrees | accepted |
| [KW3G](entries/KW3G-reader-result-for-the-folder.md) | One canonical reader result for the folder: file states, codes, folder files, link checks, private-data flag; the reader never writes | accepted |
| [N6HS](entries/N6HS-info-jsons-and-calibration.md) | Two info JSONs, one writer each, no copied fields; one fact one home; calibration as a setup file with `calibration_uuid` and a copy per take | accepted |
| [P76Y](entries/P76Y-tracking-parquet.md) | Tracking Parquet: 2D and 3D in one file; value f32 + value_f64; BYTE_STREAM_SPLIT, ZSTD 3; descriptor v2 links; realtime runs marked | accepted |
| [Q9X2](entries/Q9X2-realtime-tracking-journal.md) | Realtime tracking: CRC-framed binary journal by its own freemocap node, folded into a Parquet run; deleted only after a verified fold | accepted |
| [T8PK](entries/T8PK-privacy-notice-and-no-code-in-files.md) | Private data allowed in any field and declared in the manifest `privacy` list; no strip option yet; no file format that runs code | accepted |
| [VPD9](entries/VPD9-spec-draft-v2-details.md) | Spec draft v2 details, part 1: structure, IDs, names, CSV dialect, columns, fit lines, clocks, media boxes, repair line, journal layout | accepted |
| [3D33](entries/3D33-spec-draft-v2-details-folder-files.md) | Spec draft v2 details, part 2: manifest, info JSONs, TOML, Parquet v2 fields, Blender, exports, opening, legacy, privacy, result codes | accepted |
| [G21H](entries/G21H-gate-2-tests-location-and-interfaces.md) | Gate 2: tests in `tests/conformance/`; reader, writer and detail function names; writer scope; golden file rules | accepted |
| [Q4BK](entries/Q4BK-spec-v2-details-part-4.md) | Spec draft v2 details, part 4 (items 3, 4): reader result members; "a file of this format"; orphan files, `missing_media` | accepted |
| [0XX2](entries/0XX2-spec-v2-details-part-5.md) | Spec draft v2 details, part 5 (items 5 to 8): legacy result, manifest rebuild, link check parts, summary, manifest lock | accepted |
| [DM9S](entries/DM9S-spec-v2-details-part-7.md) | Spec draft v2 details, part 7 (items 14 to 17): JavaScript scope, privacy list, pickles, identity string, ranges, exports | accepted |
| [70VP](entries/70VP-camera-identity-forms-and-remembered-keys.md) | Camera identity: serial, port, OS device or assigned form; remembered key after the user confirms; `key_origin`; `user_name` is metadata only | accepted |
| [94YQ](entries/94YQ-golden-g1-review-decisions.md) | G1 review: file warning `gap`; `DefaultDuration` rounded down; G1 choices are the golden conventions; freemocap suggests camera matches from calibration | accepted |
| [W389](entries/W389-format-rules-from-the-golden-conventions.md) | Format rules from G1: privacy list in byte order; no line end after a result; unknown elements and boxes ignored; key order in the capture info JSON | accepted |
| [B6WH](entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) | Repair: rows = blocks in a camera pair; cut at the first bad row; no normal end of a media file; `camera_gap` source; `rows` of an unfinished file | accepted |
| [XR63](entries/XR63-reader-rules-of-the-golden-review.md) | Reader rules: legacy keys at any depth; refused sidecars out of take checks; role `calibration`; `dimensions`; unknown major; open descriptor members | accepted |
| [2MQE](entries/2MQE-tests-prerelease-serial-and-exports.md) | Test wording; golden conventions; `format_prerelease` after external review; usable serial frozen; assigned key for a new camera; exports provisional | accepted |
| [E68K](entries/E68K-camera-match-repair-order-and-g5-g6-files.md) | Camera match by vendor and product ID, else `model`; repair each step for the whole take; SFT-717 forms; sidecar with no `take_uuid`; G5 and G6 files | accepted |
| [H2HQ](entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) | Optional `filtering`, `camera_assignment`; absent and null model members; points wait for `sfn26` and 18.3; old audio not corrected; consolidation after gate 2 | accepted |
| [1P4N](entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md) | Realtime `timing` stays `realtime`; hit = a frame with a good record of its group; lowest latency per frame; event stages; latency fixed at the fold | accepted |
| [158N](entries/158N-details-for-the-decisions-of-round-3.md) | Camera match null test, prompt; repair step 3; interrupted repair stays `recording`; no-`take_uuid` sidecar; "has a default"; `timing` coverage; orphan file | accepted |
| [FB8P](entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) | Refused pair counts; `rotation` member; `invalid` file; interrupted audio `records`; legacy subfolders | accepted |
| [783H](entries/783H-text-corrections-of-the-second-golden-review.md) | Golden review 2 text fixes: SFT-703, SFT-748, SFT-763, `frames_processed`, choice files; refused audio pair; `records` null; whole audio blocks; legacy dirs | accepted |
| [7JJJ](entries/7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md) | Supersedes W5AK: repair keeps min(rows, blocks) frames; audio repair cut to whole blocks; refused header values need the correct form; W5AK rules | accepted |
| [64ER](entries/64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) | 2.0 form for an unknown major; reader audio fit from all usable rows; refused pair counts only, not take checks | accepted |

### Proposed

These entries wait for a decision of the user. Section is the section or area of the change, or
`none`.

| # | Decision | Section | Status |
|---|----------|---------|--------|
| [SM53](entries/SM53-choices-for-the-decisions-of-round-7.md) | Round 7 choice: `held_samples` and `complete_blocks` in the G5 truth | `golden` | proposed |
| [0HS2](entries/0HS2-wording-of-the-audio-repair-and-the-audio-records.md) | Wording: samples of the kept rows; usable rows; every sample in a complete fragment; audio repair steps; incomplete `mdat` | `spec` | proposed |

The entries that are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX` or `done` are in [historical.md](historical.md).

## Open work

The open work is in [open-work.md](open-work.md).

## Rules

- Read the Active entries that apply to your task. Then you do not repeat a settled question or a
  completed measurement. Read a Proposed entry only for work in its section, or when a skill
  tells you to. Read an entry of [historical.md](historical.md) only to find the reason for a
  decision.
- The body of an entry that is not `proposed` changes only by four edits: a link or anchor repair, a
  typo that does not change the meaning, the redaction of private data, and a change of ID with the
  repair of its citations. Each edit adds `_Edited YYYY-MM-DD (#PR): <kind>._` at the end of the
  entry, for example `re-ID from XXXX`. For a
  change of ID, the renamed entry gets `re-ID from XXXX`, and each repaired entry gets
  `citation repair`. Add these two lines only to an entry that is on `main`. A plain-text
  old path in a decided entry or a script stays, and means the same file at
  its new path.
- A decision that a document or code refers to must be in an entry. "This log" in an older entry or
  in the Rules means all logs.
- An absorb document is one of these: the root or a nested `AGENTS.md`, the skills, `README.md`, `spec/SPEC.md`, `spec/conformance.md`, the Rules of this file with [template.md](template.md), and the docstring of a
  tool in `tools/` for the rules that it checks. A test in `tools/tests/` is a tool here. An accepted entry is absorbed when the absorb
  documents together state all of its rules. Open work of the entry does not stop the absorb when
  `open-work.md` states that work in full. A link to the entry is not
  enough.
- The status `absorbed into` has one link for each heading that states a rule of the entry. Link a
  heading one time, also when it states two or more rules. Link a file with no anchor only when the
  rule is not under a heading, for example in a tool docstring or a YAML file. When the status
  paragraph is longer than `STATUS_EXEMPTION_LIMIT`, replace the headings of one file with the title
  heading of that file. Start with the file that has the most links. If the paragraph is still too
  long, replace the files of one document with the title heading of its
  main file. A commit that renames a heading repairs each status link to that heading. A change from
  a file link to heading links is a link repair.
- The entry that supersedes an old entry restates each rule of the old entry that stays. A link can
  restate a rule. The link must go to a heading of an absorb document, and that heading must state
  the rule. The commit that changes the text under such a heading cites its own entry next to the
  changed rule. That change does not supersede the entry that links the heading.
- Only these status changes are allowed: `proposed` to `accepted` or `rejected`; `accepted` to
  `superseded by XXXX`, `absorbed into <path>#<anchor>` or `done`; `absorbed into <path>#<anchor>`
  to `superseded by XXXX`; and `evidence` to
  `evidence; used by XXXX`, when an accepted entry cites the `evidence` entry for its decision.
  `done` is for an accepted entry that records a one-off action, with no rule that stays, when the
  action is complete. Each status change adds its date and the PR that made it. In the same PR,
  change the status in the index and move the row to the table for the new status.
- `tools/check_decision_log.py` checks the tables, the status forms, the Section cell, the ID
  alphabet and the size limits. Its docstring states them. `tools/check_links.py` checks the links
  and the full-SHA permalinks. A tool is the source of a rule that it checks.
- A consolidation entry states the rules that stay from a group of entries, and it supersedes each
  entry of the group. It changes no decision.
- When the read path is at 90% of its limit or more, first absorb each accepted entry whose rules
  the absorb documents state. Then
  write each rule that no absorb document states in the absorb document where it belongs, and
  absorb its entry.
- A commit that only makes a workflow, skill, template or tool copy agree with a landed entry
  cites that entry. It needs no entry of its own. A new rule is not a copy.
- Delete an open-work item when the work is done. Put a dated fact in `open-work.md` or in an
  entry, not in `AGENTS.md`.
- Put long evidence in a tracked file in `evidence/` of the log folder, and link to it. A PR that raises a limit
  of `tools/check_decision_log.py` must add an entry.
- An ID changes only on a `re-ID:` line of `tools/check_decision_log.py`, to the ID of a new `--new`
  run.
- Until a commit is on `main`, cite its PR number and the file path, not its SHA.
  The `ADR-` prefix is for citations only: a file name, a
  heading, an index row and a status line hold the bare ID. Cite a provisional entry of another repo
  by the repo name, the PR number and the slug. Do not edit a decided entry only to add or move the
  prefix or the link.
