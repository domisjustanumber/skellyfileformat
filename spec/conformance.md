# skellyfileformat conformance tests

Status: **draft, skeleton only.** This file has no tests yet. It goes to the user for review at
gate 1, together with [SPEC.md](SPEC.md).

This list is normative. The license of the text is CC-BY-4.0 ([LICENSE](LICENSE)).

## How to read a test

- A test starts on a new line with its ID in bold, for example `**SFT-001**`, then its title.
- The next line starts with `Checks:` and gives the SFF IDs of the requirements that the test
  checks, for example `Checks: SFF-001, SFF-004`.
- A `Pass:` line gives the pass criteria. A test can also name its inputs, for example a golden file.
- A removed test keeps its line, with `(withdrawn)` after its ID.
- Each requirement of [SPEC.md](SPEC.md) that is not withdrawn has one or more tests.
  `tools/check_spec_traceability.py` checks the IDs and the links.

## Tests
