# B6WH — Repair: equal rows and blocks, the cut at the first bad row, no normal end of a media file

**Status:** accepted, 2026-11-16 (user; questions Q83 to Q86 and Q109 of the review of the golden
capture vectors).

## Decision

The user accepted these rules. Each item gives its question number.

1. **A repair makes a camera pair equal (Q83).** A repair cuts the sidecar and the camera file back
   to the frames that have a complete row and a complete block. After a repair, the number of rows
   is the number of blocks (SFF-759, SFF-795, SFF-797). Before, the rules cut each file on its own:
   in G06 `repaired`, a camera had 22 rows and 17 blocks, and this does not agree with SFF-759. G06
   is made again.
2. **An interrupted file that is not repaired (Q84).** `rows` of the reader result stays the number
   of complete rows (SFF-746). The multi-camera frames (SFF-754) use only the rows that have a
   complete block (SFF-740).
3. **No normal end of a repaired media file (Q85).** A repaired camera file gets no normal end: the
   repair writes no Cues and does not write the SeekHead again. A repaired audio file gets no `mfra`
   box. Reason: these writes change bytes before the cut. A reader accepts both files (SFF-794,
   SFF-796, SFF-797).
4. **The cut of a sidecar (Q86).** A repair cuts a sidecar at the first bad row: a row that is not
   complete or that has a wrong CRC. It does not keep the good rows after a bad row. This text
   replaces "the last complete row with a correct CRC" of SFF-795.
5. **`source` of the warning `camera_gap` of a repair (Q109).** `source` of the manifest warning
   `camera_gap` that a repair adds is the program that ran the repair: `skellycam` or `freemocap`
   (SFF-727, SFF-793).

## Reason

The user answered "otherwise agree" to the recommendations of the review on 2026-11-16. Item 3
has the reason of the user. Item 1 has the conflict with SFF-759 that the user named. The other
items have no recorded reason.

The decision of Q108 (the order of the steps of a repair) is not in this entry. Its text does not
agree with the case `interrupted_repair` of G06 (see [open-work.md](../open-work.md)).
[ADR-W5AK](W5AK-details-for-the-decisions-q83-to-q111.md) proposes the details that the spec text
of these items needed.

## Consequences

- The golden generator makes G06 again (item 1). This entry is the decision entry that
  `AGENTS.md` section 4 needs for that change of the golden files.

## Alternatives rejected

- A repair that cuts each file on its own (the text before item 1): a repaired pair then has
  different numbers of rows and blocks.
- A normal end of a repaired media file: it changes bytes before the cut.

## Open work

See [open-work.md](../open-work.md).
