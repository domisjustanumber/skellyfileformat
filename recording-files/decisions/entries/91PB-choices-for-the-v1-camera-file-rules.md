# 91PB — Choices of the agent for the v1 camera-file rules

**Status:** proposed, 2026-11-25 (agent; the spec work of [ADR-3XYN](3XYN-v1-camera-file-rules-move-to-recording-files.md)).

## Decision

The owner did not decide these points. The agent chose them to write SFF-896 to SFF-903, SFT-774 to
SFT-778 and section 9 of the legacy annex.

1. **Place.** The requirements are under the heading "Section 21, continued" at the end of section
   23, and each says "This requirement belongs to section 21", as SFF-894 and SFF-895 do. Section 21
   links to them.
2. **Draft form.** Until gate 2, each new requirement and each new test starts with the word
   "Draft" before its ID, and the new tests have no row in the stage table. The doc checks then do
   not count them. At gate 2, the word goes, and the runnable tests and the stage rows come in the
   same commit.
3. **Folders.** A legacy folder of the family `unknown` with `.mp4` files in `synchronized_videos/`
   is read as v1, for the sample data and the import folders. The family of a folder does not
   change. A v2 alpha name is `*.id-<n>.idx-<n>.mp4`, and it wins over the other rules. The texts of
   the refusals are examples. A refusal changes no member of the reader result.
4. **Codes.** `time_file_unusable`, `extra_tracks`, `edit_list_not_supported`, `index_mismatch`
   and `frame_count_differs` are codes of the report of a program, not warnings of the reader
   result.
5. **The time file.** The causes of each reason are those of the table of SFF-897. A file with
   fewer than n values gives `length`. Each value is rounded to the nearest integer, and a half
   rounds up.
6. **The frame table.** The end of the edit is compared exactly in integers. E is rounded to the
   nearest track unit, and a half rounds up. The frame count stops at the first frame whose bytes are
   not all inside the file.
7. **The comparison of indexes.** Each index is shifted so that frame 0 has the time stamp 0,
   because FFmpeg shifts its time stamps.
8. **The time map.** The base B is taken at the first row with a finite value. Earlier rows have
   T_k = 0. U_k is rounded to the nearest nanosecond, and a half rounds up. When no time file has a
   finite value, the header map applies.
9. **The header rate.** A camera with fewer than 2 frames, or with equal first and last time stamps,
   has no header rate. With no header rate, a reader moves only frame by frame. r is the recorded
   frame rate also when the folder has time files.
10. **The tests.** SFT-774 to SFT-778 get the mark `stage1a` at gate 2. They make their inputs at test time
   with PyAV 19.0.2 and commit no media. They reach a reader through the detail functions
   `legacy_media` and `legacy_frame_at`, and through the command `bin/legacy-media.mjs` of a
   JavaScript adapter. Their shapes are decided at gate 2.

## Reason

- Item 1: the IDs are in file order (SPEC.md section 2), and `tools/check_spec_traceability.py`
  refuses an ID before a lower ID. The new IDs must come after SFF-895.
- Item 2: `tools/tests/test_conformance_coverage.py` needs a runnable test for each test of
  conformance.md, and `tools/check_spec_traceability.py` needs a test for each requirement. A gate-1
  draft has no runnable test yet. No code is written before gate 2.
- Item 3: the player spec of skellycam reads such folders (its section 2.2, rule 3), and the reader
  result stays as the golden folders have it.
- Items 5 to 9: two programs must give the same frames and the same times. Each rounding and each
  edge case needs one rule.
- Item 10: playback is stage 1a. Inputs made at test time follow the rule of no committed media.

## Alternatives rejected

- A new section 24: the owner named section 21 (Q798).
- A new normative part in `parts/`: the traceability tool reads only SPEC.md.
- Bold IDs now: the doc checks of `tools/tests` would fail until gate 2.
- Stub runnable tests now: that is code before gate 2.
- Golden folders with MP4 files: they would commit media.
