# 6PNN — The format field is `skellyspecs`; the golden folders are made again

**Status:** accepted, 2026-11-23 (user; questions Q8 and Q13 of the owner session).

## Decision

1. **The field.** The first field of each file of the format is `skellyspecs`, in place of
   `skellyfileformat`. Its values do not change. This applies to these files:
   - the recording manifest, the capture info JSON, the processing info JSON and the header of the
     realtime journal (the member `skellyspecs`, SFF-702);
   - the first line of each timing sidecar, `# skellyspecs=video_timing` or
     `# skellyspecs=audio_timing` (SFF-742), and the header key `skellyspecs` (SFF-766, SFF-869);
   - the recognition of a file of this format by a reader (SFF-864).
2. **No old name.** A reader does not accept `skellyfileformat` in place of `skellyspecs`. No file
   with the old name exists outside the machine of the owner, so no legacy rule is needed.
3. **The name of the format.** The spec calls the format "the skellyspecs recording format".
4. **The test adapter.** The variables are `SKELLYSPECS_ADAPTER` and `SKELLYSPECS_JS_ADAPTER`.
5. **The golden folders.** The writer string of the generator is `skellyspecs-goldgen 1.0.0`.
   `tools/make_golden.py` makes each golden folder again with the new field and writer string, with
   new `SHA256SUMS`. This entry is the decision entry of that change.

## Reason

- The user wants one name for the repository and the format
  ([ADR-YYP7](../../../decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 1).
- The format has no release, so the change breaks no file of a user.

## Alternatives rejected

- Keep `skellyfileformat` in the files: the user rejected it (Q8).
- Accept both names in a reader: no file has the old name.
