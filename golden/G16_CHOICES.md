# Choices made for G16 that the spec does not give

**Accepted by the user on 2026-11-16 as conventions of the golden folders**
([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 7). An item is a
rule of the format only where the spec states it. A decision of the same day settled item 1 of
"Texts that must change" (ADR-2MQE item 1). The committed pickle stays harmless.

G16 holds the files that could run code, of
[SPEC.md Appendix A](../spec/SPEC.md#appendix-a-golden-folders) and SFF-884.
`tools/goldgen/g16.py` makes it. The conventions of [G01_CHOICES.md](G01_CHOICES.md) apply and are
not repeated here.

## What the case `take` holds

- The take of G1 (case `take`), with `<rec>` `g16_synthetic_take` and its own `take_uuid`: two
  cameras, the audio, the capture info JSON and the manifest.
- `harmless_plain_dict.pkl` in the root: 23 bytes. The manifest does not list it.
- `exports/npy/g16_synthetic_take.frames.npy`: 134 bytes. Its NPY header has `descr` `|O`. The
  manifest lists it in `files`, with the role `export`.

**The two files are harmless.** The pickle is the pickle of the value `{"harmless": True}`. The
body of the NPY is the pickle of an empty list. Each stream has only opcodes that push a plain
value: no stream names a module, a class or a function, so a load runs no code.
`tools/tests/test_g_legacy_safety.py` reads the opcodes with `pickletools` and fails on `GLOBAL`,
`STACK_GLOBAL`, `REDUCE`, `INST`, `OBJ`, `NEWOBJ`, `NEWOBJ_EX`, `BUILD`, an extension opcode or a
persistent ID. The test does not load a pickle.

## The expected result

Each member that this table does not name has the value and the requirement of G1
([README.md](README.md)).

| Member | Value | Requirement |
|---|---|---|
| `other_files` | one item: `harmless_plain_dict.pkl`, `invalid`, `code_in_file`. The same in the two scopes: the reader finds the pickle by its name | SFF-884, SFF-885 |
| `folder_files` | two items, in order of the bytes of the path: the NPY, then the capture info JSON | SFF-885, SFF-890 |
| The NPY item, scope `full` | `role` `export`, `state` `invalid`, `reason` `code_in_file`, `warnings` `[]` | SFF-884 |
| The NPY item, scope `player` | `state` `not_checked`, `reason` null, `warnings` `[]` | SFF-892 |
| `takes[].state`, `takes[].warnings` | `complete`, `[]`: an `invalid` folder file does not change the take | SFF-869, SFF-887 |
| `links`: `files` | `ok`: each path of the manifest exists, also the NPY | SFF-872 |
| `folder_state`, `folder_warnings` | `ok`, `[]`: a pickle is not a file of this format, so it gives no `orphan_file` | SFF-875, SFF-888, SFF-889 |

The `player` result differs from the `full` result only in the NPY item and in the check `frames`.

## Choices

1. **The take.** Appendix A says only "the take folder". Choice: the input of G1 (case `take`)
   with no change, through `common.write_take`, with `<rec>` `g16_synthetic_take` and `take_uuid`
   `00000000000040008000000000000016`. The folder has about 270 kB, nearly all from the media
   files of G1. Alternative: a take with fewer frames, which needs a second take input.
2. **No truth file.** G16 has no `take.truth.json`: no test of the clicks and the flashes names
   G16.
3. **A harmless pickle.** Appendix A says "a pickle (`.pkl`)". SFT-767 says "a canary file is not
   created", which suggests a pickle whose load creates a file. Choice: the repository holds no
   file whose load runs code. The pickle holds a plain dictionary. SFF-884 finds a pickle by its
   name suffix, so the content does not change the result. See "Texts that must change".
4. **The name and the place of the pickle.** Choice: `harmless_plain_dict.pkl`, in the root. The
   name tells a person that the file is safe. Alternative: a name of an old release, for example
   `<rec>_calibration.pickle`; a second pickle in `synchronized_videos/` with the suffix
   `.PICKLE`, to test "in any case" and the media folder. G16 has only the one file that
   Appendix A names.
5. **The bytes of the pickle.** Choice: `pickle.dumps({"harmless": True}, protocol=2)`. A fixed
   protocol gives fixed bytes, and protocol 2 writes no frame. `SHA256SUMS` holds the sum.
   Alternative: protocol 4 or 5.
6. **The path and the role of the NPY.** SFF-884 says "that the manifest lists", with no path and
   no role. Only section 18.3 puts an NPY file in a take. Choice:
   `exports/npy/<rec>.frames.npy`, the fixed export name of SFF-857 for run 0. The manifest item
   has `role` `export`, `owner` `freemocap` and `sha256` null (SFF-723). Alternative: an array of
   a table, `exports/npy/<rec>.<table>.npy`, which needs a table name.
7. **No other export file.** The take has no export inventory, no processing info JSON and no
   Parquet. A writer of this format does not make such a take. A reader has no rule that needs
   these files for an item with the role `export`, so the result does not change. Alternative: G3
   as the base, which is much larger.
8. **The bytes of the NPY.** Written by hand, without NumPy: the magic, the version 1.0, a header
   of 118 bytes with `{'descr': '|O', 'fortran_order': False, 'shape': (0,), }`, padded with
   spaces to 128 bytes in all, as NumPy pads it. The body is `pickle.dumps([], protocol=2)`
   (6 bytes): NumPy stores an object array as one pickle. Alternative: `numpy.save` with
   `allow_pickle`, whose body is a pickle that names NumPy functions (`REDUCE`). Then the
   repository would hold a pickle that calls code. A test with NumPy 2.4.6 confirms that NumPy
   reads the header as an object type and refuses the file with `allow_pickle=False`.
9. **The warnings of the NPY item.** SFF-891 gives `prerelease` to a file with
   `format_prerelease` > 0. An NPY file has no such member. Choice: `[]`.
10. **The manifest is written two times.** `common.write_take` has no input for one more `files`
    item. The generator reads the manifest that `write_take` wrote, adds the item in order of
    `path` and writes the file again with the same white space. `privacy` and `summary` do not
    change: the table of SFF-881 has no field of an export.

## Texts that must change

1. **SFT-767, last sentence:** "No code from the files runs (a canary file is not created)." The
   committed pickle is harmless, so a canary check on G16 proves nothing. Proposed text: "The
   reader does not unpickle a file: the test replaces the unpickle functions with functions that
   fail." Alternative: the test makes a pickle with a canary at test time, in a temporary copy of
   G16. A file whose load runs code must not be in the repository. Decision (ADR-2MQE item 1): the
   alternative. The test makes, at run time in a temporary folder, a pickle that creates a marker
   file if a program loads it, and it passes when no marker file is created.
   `tests/conformance/test_s22_privacy.py` does this.
2. **Appendix A, row G16:** add "The pickle and the object array hold plain values: a load of
   them runs no code."
3. **SFF-884:** it does not say which role and which path an NPY file "that the manifest lists"
   has (choice 6), or what a reader does with an NPY file in the root or the media folder that
   the manifest does not list. By SFF-885, that file is `not_in_format` in `other_files`, and the
   reader does not read its header.
