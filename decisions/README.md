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
| [VJ14](entries/VJ14-shared-package-and-spec.md) | skellyfileformat is the one shared package for the format, with a descriptive spec; the spec fixes the names | accepted |
| [5K7G](entries/5K7G-no-recorded-overlays.md) | No recorded overlays: no burned-in stamp, no overlay file or attachment; the player draws the frame label | accepted |
| [WD9A](entries/WD9A-lichtblick-reference-viewer.md) | Lichtblick is the external test viewer, not Foxglove; VLC compatibility dropped; audio tests use a pinned Lichtblick build with an Audio panel | accepted |
| [X1G6](entries/X1G6-read-old-write-mcap.md) | Old recordings stay readable; new skellycam and skellysync write only MCAP with JPEG and Opus; no file of this format means legacy | accepted |
| [7K3C](entries/7K3C-format-versioning-in-metadata.md) | Format version = major.minor of the skellycam release that last changed the format; major/minor/prerelease in each file's metadata | accepted |
| [68Z6](entries/68Z6-rotation-in-metadata-only.md) | Frames stored unrotated; `display_rotation` in the camera file's metadata only; no other rotation; readers apply it | accepted |
| [752H](entries/752H-timing-fields.md) | Arrival in `log_time`, sample time in `timestamp`, `sequence` = frame or packet number; no legacy time; encoder skips as `foxglove.Log` | accepted |
| [DK8S](entries/DK8S-mcap-profile-files-and-names.md) | One MCAP file per device; profile `freemocap`; protobuf; topics carry the label; `freemocap.*` metadata records; writer in Header `library` | accepted |
| [TDB5](entries/TDB5-whole-recording-no-manifest.md) | Whole recording of per-device MCAP files; no manifest; takes grouped by `take_uuid`; canonical reader-result JSON; repo rules | accepted |
| [10JC](entries/10JC-lichtblick-audio-checks.md) | Lichtblick audio checks: mrkbac/lichtblick at 70f5900, built offline, Opus picked by hand at 48 kHz, 1x only; sync judged in skellycam | accepted |
| [MG7C](entries/MG7C-fit-segments-by-position.md) | Fit segments keyed by position (`pos_first`, `pos_last`), in position order with no gap; fitter named; breakpoints give `sequence` | accepted |
| [PV6S](entries/PV6S-writing-crash-reading-and-repair.md) | Fixed-count chunks, no compression, data CRC, fsync ~1 s; crashed files read in place; user-approved repair cuts after the last good chunk | accepted |
| [D9N1](entries/D9N1-opus-audio-settings-and-timing.md) | Opus in `foxglove.CompressedAudio`; OpusHead fields in channel metadata, `sample_rate` = decode rate, gain 0; 48 kHz 20 ms VBR; log_time = arrival | accepted |
| [5G42](entries/5G42-gate1-names.md) | Gate 1 names: `freemocap.repair` record, audio `label`, `audio_latency_ns` in the audio channel metadata, RFC 8785 reader result | accepted |

### Proposed

These entries wait for a decision of the user. Section is the section or area of the change, or
`none`.

| # | Decision | Section | Status |
|---|----------|---------|--------|
| [T24G](entries/T24G-spec-v1-review-fixes-crash-fit-audio.md) | Spec v1 review fixes, 15 items: records before first chunk, CRC checks, crash-read end, repair details, fit maths and cover, Opus and camera details | `spec` | proposed |
| [WG08](entries/WG08-reader-result-states-and-codes.md) | Reader result: `invalid` state, folder states, reason and warning codes, `audio_count`, take counting, null members, integer types, sort orders | `spec.reader_result` | proposed |
| [W4PF](entries/W4PF-shared-package-and-no-overlays.md) | Consolidate VJ14 and 5K7G: one shared package, spec fixes its own names only, no recorded overlays; no change of decision | none | proposed |

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
