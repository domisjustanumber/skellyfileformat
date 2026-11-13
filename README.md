# skellyfileformat

skellyfileformat defines the file format of skellycam and skellysync recordings: a profile of
[MCAP](https://mcap.dev/spec) with JPEG video and timing in MCAP messages
([ADR-DK8S](decisions/entries/DK8S-mcap-profile-files-and-names.md)). The [specification](spec/SPEC.md) gives the
channels, the schemas, the field meanings, the clocks and the recovery rules, so that other programs
can implement the format from the spec alone.

**Status: draft.** No format version is released yet. The spec and its conformance tests are written
first and reviewed. Code comes after them ([AGENTS.md section 4](AGENTS.md#4-project-rules)).

The sections marked "normative" are rules. A change to them needs a decision entry
([decisions/](decisions/README.md)).

## Scope (normative)

The format describes one recording (one take): a set of synchronised MCAP files, one for each
device, that share one clock ([ADR-TDB5](decisions/entries/TDB5-whole-recording-no-manifest.md)).
It covers these files:

- each camera file: an MCAP file of profile `freemocap` in which each frame is one JPEG in a
  `foxglove.CompressedImage` message, with the timing of the frame in the MCAP fields and the facts
  in the file metadata ([ADR-DK8S](decisions/entries/DK8S-mcap-profile-files-and-names.md),
  [ADR-752H](decisions/entries/752H-timing-fields.md));
- the audio file of skellycam and skellysync: Opus packets in `foxglove.CompressedAudio` messages,
  with the Opus identification header fields in the channel metadata
  ([ADR-HD8Z](decisions/entries/HD8Z-opus-audio.md)).

There is no recording manifest.

It also covers the recording as a whole: which files make up one recording, the clock that they
share, the facts about the recording in each file's metadata (authoritative), how a writer records
the set, and how a reader opens a recording, also when it is crashed or incomplete.

The format does not cover recordings that older programs wrote, for example H.264 MP4 files and
timestamp CSV files. The programs that read those recordings define how they read them. Section 13
of the spec tells how to find a file that is not in this format.

## Compatibility promise (normative)

- A conforming reader must read every released format version.
- A released format version is one with `prerelease` = 0 in its metadata
  ([Versioning](#versioning-normative)).
- A file with `prerelease` > 0 has no compatibility promise. A later reader can refuse it.
- A writer writes only the latest format version.

## Versioning (normative)

- **Format version.** The format version is the `major.minor` of the skellycam release that last
  changed the format.
  - A change that an older reader cannot read needs a new skellycam major version.
  - An added field needs a new skellycam minor version, or a new major version.
  - A skellycam patch release does not change the format.
- **Version fields.** The metadata of each file holds three values: `major`, `minor` and
  `prerelease`. Each is an unsigned integer that fits in 16 bits, written as a decimal string
  ([ADR-7K3C](decisions/entries/7K3C-format-versioning-in-metadata.md)).
  - `prerelease` is 0 for a released format, and N for the Nth prerelease revision.
  - A reader must refuse a file with a `major` that it does not know.
  - A reader must read a file with a higher `minor` of a `major` that it knows, and skip the fields
    that it does not know.
- **MCAP version.** The MCAP version of a file (its magic) is not the format version.
- **Writer string.** Each file also holds a writer string, for example `skellycam 2.1.0`. It is
  for diagnostics only. A reader must not change its behaviour because of it. skellysync writes the
  format version that skellyfileformat gives, not its own version.
- **Package version.** The skellyfileformat package uses semantic versioning. Its `major.minor` is
  the format version that it implements. Its patch number counts the library fixes that do not
  change the format.

## Conformance (normative)

- A conforming writer writes files that obey each writer requirement of [SPEC.md](spec/SPEC.md),
  and it passes each writer test of [conformance.md](spec/conformance.md).
- A conforming reader obeys each reader requirement of SPEC.md, passes each reader test of
  conformance.md, and reads each golden file in `golden/` to the expected result.
- Each requirement has an ID `SFF-NNN`. Each test has an ID `SFT-NNN` and names the requirements
  that it checks.

## Licenses

- The spec text (`spec/`) and the normative sections of this README: CC-BY-4.0
  ([spec/LICENSE](spec/LICENSE)).
- All other files: Apache-2.0 ([LICENSE](LICENSE)).

## Development

Read [AGENTS.md](AGENTS.md). Run `uv sync`, then `uv run pre-commit install`, then `uv run pytest`.
