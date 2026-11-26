# NB40 — LF line ends for each text file

**Status:** accepted, 2026-11-26 (user; answer Q862 of the owner session of 2026-11-26, "agree to all").

## Decision

1. **Q862.** `.gitattributes` starts with `* text=auto eol=lf`. Git stores each text file with LF
   in the index, and it writes LF in the working tree, also when `core.autocrlf` is `true`.
2. The line `recording-files/golden/** -text` stays. It comes after the general rule, so it wins
   for the golden files. Git changes no byte of a golden file
   ([ADR-G21H](../../recording-files/decisions/entries/G21H-gate-2-tests-location-and-interfaces.md)
   item 9).
3. Do not write a CRLF line end in a text file of this repository.

## Reason

- The owner wants LF line ends in all his repositories.
- A system Git config on Windows sets `core.autocrlf` to `true`. Without the rule, Git wrote CRLF in
  the working tree of this repository.

## Evidence

- Git 2.43.0.windows.1. `git add --renormalize .` changed no file except
  `.gitattributes`. `git ls-files --eol` showed no file with CRLF in the index outside the golden
  folders.
- `git checkout-index -a` with the new attributes wrote each golden file byte for byte as in the
  working tree. `uv run --group golden python tools/make_golden.py --check` gave "the same" for
  each folder, and each `SHA256SUMS` passed.
