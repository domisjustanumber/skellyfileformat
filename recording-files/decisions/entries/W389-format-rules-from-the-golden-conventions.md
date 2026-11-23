# W389 — Format rules from the golden conventions

**Status:** absorbed into
[`spec/SPEC.md#2-conventions`](../../SPEC.md#2-conventions),
[`spec/SPEC.md#3-versioning`](../../SPEC.md#3-versioning),
[`spec/SPEC.md#13-capture-info-json`](../../SPEC.md#13-capture-info-json),
[`spec/SPEC.md#22-privacy-and-safety`](../../SPEC.md#22-privacy-and-safety),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`golden/README.md#golden-folders`](../../golden/README.md#golden-folders),
[`golden/G01_CHOICES.md#choices-made-for-g1-that-the-spec-does-not-give`](../../golden/G01_CHOICES.md#choices-made-for-g1-that-the-spec-does-not-give),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; review of the golden conventions of G1)).

## Decision

[ADR-94YQ](94YQ-golden-g1-review-decisions.md) item 5 left open which conventions of golden folder
G1 are rules of the format. The user decided each one.

1. **Order of the privacy list.** The array `privacy.fields` of the manifest is sorted by `file` and
   then by `field`, each in the order of its UTF-8 bytes (SPEC.md SFF-881). Reason: SFF-881 said
   "sorted" with no order, so two writers could write different bytes.
2. **End of a reader result.** A reader result has no byte after the canonical JSON: it has no line
   end (SFF-885). Reason: a test compares a result with a file, byte for byte.
3. **Elements and boxes that the spec does not name.** In a camera file and an audio file, a reader
   ignores each Matroska element and each MP4 box that the spec does not name (SFF-709). Reason: the
   pinned FFmpeg writes such elements and boxes, and a reader must not refuse the files of this
   package.
4. **Key order in the capture info JSON.** The words of the user: "Key order must match". A writer
   writes the keys of `camera_configs` in order of `group_position`, and the keys of `controls` in
   the order of the list of SFF-802 (SPEC.md section 13). This is a rule of the format, not only a
   convention of the golden folders. Reason: two writers then write the same bytes for the same
   take.
5. **White space of a JSON file.** The indent of 2 spaces and the one LF at the end are a convention
   of the golden folders only. A reader accepts each JSON white space. Reason: white space has no
   meaning in JSON, and the manifest hash is over the bytes as a writer wrote them.

## Consequences

- Item 4 gives a writer rule only. No reader rule depends on the order of the keys of a JSON object.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
