# skellyfileformat specification

Status: **draft, skeleton only.** This file has no requirements yet. The draft goes to the user for
review at gate 1 ([AGENTS.md section 4](../AGENTS.md#4-project-rules)). No format version is
released yet.

This specification is normative. The license of the spec text is CC-BY-4.0 ([LICENSE](LICENSE)).

## 1. Scope and terms

## 2. Conventions

- The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have the meanings of RFC 2119 and
  RFC 8174, when they are in capital letters.
- A requirement starts on a new line with its ID in bold, for example `**SFF-001**`. The ID has
  three digits. A requirement has one ID. An ID is not reused or renumbered.
- A removed requirement keeps its line, with `(withdrawn)` after its ID.
- A provisional requirement has `(provisional)` after its ID and names the open item that it waits
  for. A provisional requirement must be closed before v2.0.0.
- Each requirement has one or more tests in [conformance.md](conformance.md).
  `tools/check_spec_traceability.py` checks this.

## 3. Versioning

## 4. Video: the MKV profile

## 5. Video timing sidecar

## 6. Audio: FLAC in `.mka` (skellycam)

## 7. Audio timing sidecar (`.skau`) and the packet table

## 8. Audio in the camera MKV (skellysync)

## 9. Embedding and finalisation

## 10. Segment UID, live offsets and final offsets

## 11. Unfinalised and crashed files

## 12. File, attachment and MIME names

## 13. Files that are not in this format

## 14. skellysync camera sidecar header (provisional)

## Appendix A. Golden files
