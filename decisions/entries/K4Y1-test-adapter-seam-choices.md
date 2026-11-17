# K4Y1 — The choices of the test adapter seam

**Status:** absorbed into
[`spec/conformance.md#the-test-adapter`](../../spec/conformance.md#the-test-adapter),
[`AGENTS.md#4-project-rules`](../../AGENTS.md#4-project-rules),
[`README.md#implementations`](../../README.md#implementations),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; the user accepted each item as it
stands); was proposed, 2026-11-17 (an agent chose these items to apply
[ADR-YBT1](YBT1-spec-only-test-adapter-and-labels.md))).

## Decision

[ADR-YBT1](YBT1-spec-only-test-adapter-and-labels.md) item 2 asks for one configurable seam. The
user did not choose its form. An agent chose these items. The code of `tests/conformance/` applies
them now, so that the tests can run.

1. **The Python adapter.** The environment variable `SKELLYFILEFORMAT_ADAPTER` names an importable
   Python module: the test adapter. The fixtures `reader` and `writer` give that module. It is
   imported at the first use of a name, so a test with no adapter fails in its body, with one line:
   "no test adapter is configured: set SKELLYFILEFORMAT_ADAPTER to the importable module of the
   test adapter of an implementation (spec/conformance.md, 'The test adapter')".
2. **The JavaScript adapter.** The environment variable `SKELLYFILEFORMAT_JS_ADAPTER` names a
   folder. The JavaScript command is `node <folder>/bin/read-folder.mjs <take folder> [--records]`,
   the old layout of `js/`. With no variable, a test that runs the command fails with one line.
3. **hyparquet.** The hyparquet part of SFT-747 finds `hyparquet` and `hyparquet-compressors` in
   `<folder>/node_modules` of the JavaScript adapter. With no JavaScript adapter, that part is
   skipped, as before.
4. **The child process of SFT-730.** It imports the module that `SKELLYFILEFORMAT_ADAPTER` names,
   with the `sys.path` of the test process.
5. **No pytest option.** The two variables are the only configuration.
6. **Names.** The marks keep the names `stage1a` to `stage4`. The `README.md` section "Package"
   becomes "Implementations".

## Reason

- An environment variable reaches the test process and the child process of SFT-730 with no new
  code. A pytest option does not reach the child.
- A folder for the JavaScript adapter keeps the old command and gives hyparquet a place to resolve
  from, with one variable.
- The old mark names keep the commands of `AGENTS.md` and the tables of `spec/conformance.md`.

## Alternatives rejected

- A command line in place of a folder for the JavaScript adapter: hyparquet then needs a second
  variable.

## Open work

See [open-work.md](../open-work.md).
