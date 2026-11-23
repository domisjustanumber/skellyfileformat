"""Fixtures of the conformance tests (decision YBT1, recording-files/conformance.md, "The test adapter").

The tests reach an implementation only through its test adapter. `SKELLYFILEFORMAT_ADAPTER` names
the importable module of the Python adapter, and `SKELLYFILEFORMAT_JS_ADAPTER` the folder of the
JavaScript adapter (decision K4Y1). This module imports no adapter at module level, so
pytest can collect the tests with no adapter. A test that needs an adapter then fails with one line.
"""

from __future__ import annotations

import importlib
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = "SKELLYFILEFORMAT_ADAPTER"
JS_ADAPTER = "SKELLYFILEFORMAT_JS_ADAPTER"
NO_ADAPTER = (
    f"no test adapter is configured: set {ADAPTER} to the importable module of the test adapter of an "
    "implementation (recording-files/conformance.md, 'The test adapter')"
)
NO_JS_ADAPTER = (
    f"no JavaScript test adapter is configured: set {JS_ADAPTER} to the folder that holds "
    "`bin/read-folder.mjs` (recording-files/conformance.md, 'The test adapter')"
)


def adapter_name() -> str:
    """The module name of the Python adapter. A test with no adapter fails with one line."""
    name = os.environ.get(ADAPTER, "")
    if not name:
        pytest.fail(NO_ADAPTER, pytrace=False)
    return name


def js_command(folder: Path, records: bool = False) -> list[str]:
    """The command of the JavaScript adapter for a folder. A test with no adapter or no `node` fails with one line."""
    adapter = os.environ.get(JS_ADAPTER, "")
    if not adapter:
        pytest.fail(NO_JS_ADAPTER, pytrace=False)
    script, node = Path(adapter) / "bin" / "read-folder.mjs", shutil.which("node")
    if node is None or not script.is_file():
        pytest.fail(f"the JavaScript adapter `{script}`, or `node`, does not exist", pytrace=False)
    return [node, str(script), str(folder), *(["--records"] if records else [])]


class _Lazy:
    """The Python adapter, imported at the first use of an attribute.

    So a test with no implementation fails in its body, with one line, and not with a fixture error.
    A test that first asks for a golden folder that is not built is skipped before that.
    """

    def __getattr__(self, name):
        return getattr(importlib.import_module(adapter_name()), name)


@pytest.fixture
def reader():
    """The reader of the Python adapter: `read_folder`, `canonical_json` and the detail functions."""
    return _Lazy()


@pytest.fixture
def writer():
    """The writer of the Python adapter: `TakeWriter`, `repair_take` and `release_check`."""
    return _Lazy()


@pytest.fixture
def js_reader():
    """A function that runs the JavaScript adapter on a folder and returns the bytes of its standard output."""

    def run(folder: Path, records: bool = False) -> bytes:
        return subprocess.run(js_command(folder, records), capture_output=True, check=True).stdout  # noqa: S603

    return run


@pytest.fixture
def golden():
    """A function that returns the folder of a case, for example `golden("G01")` or `golden("G01", "confirmed_key")`.

    The two expected results are beside the folder: `<case>.full.json` and `<case>.player.json`.
    """

    def case_folder(name: str, case: str = "take") -> Path:
        folder = ROOT / "golden" / name / case
        if not folder.is_dir():
            pytest.fail(f"the golden case `recording-files/golden/{name}/{case}` does not exist", pytrace=False)
        return folder

    return case_folder


# --- Marks (conformance.md, "How to read a test"; decision QH61 item 46) ---


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "external(program): the repository of that program runs the test; it is skipped here"
    )
    config.addinivalue_line(
        "markers", "provisional(open_item): the test waits for an open item; it is skipped until then"
    )


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(f"stage{stage_of(item)}")
        mark = item.get_closest_marker("external")
        if mark is not None:
            reason = f"external: {mark.args[0]}; the repository of that program runs it"
            item.add_marker(pytest.mark.skip(reason=reason))
        mark = item.get_closest_marker("provisional")
        if mark is not None:
            item.add_marker(pytest.mark.skip(reason=f"provisional: {mark.args[0]}"))


# --- Stages (conformance.md, "The stage of each test"; decisions CPM2 and YBT1) ---
# A stage is a label for the program and the need that a test serves, not a build stage.
# tools/tests/test_conformance_stages.py checks these three tables against conformance.md.

# The stage of each test: the latest stage of its parts.
STAGES = {
    "700": "2", "701": "1a", "702": "1a", "703": "4", "704": "1a", "705": "2", "706": "2", "707": "2",
    "708": "2", "709": "2", "710": "2", "711": "1a", "712": "1a", "713": "1a", "714": "1a", "715": "1a",
    "716": "1a", "717": "1a", "718": "1a", "719": "1a", "720": "1a", "721": "1a", "722": "1a", "723": "1a",
    "724": "1a", "725": "1a", "726": "1a", "727": "1a", "728": "1a", "729": "1a", "730": "2", "731": "1a",
    "732": "1a", "733": "2", "734": "2", "735": "1a", "736": "2", "737": "3", "738": "2", "739": "2",
    "740": "2", "741": "4", "742": "3", "743": "3", "744": "2", "745": "3", "746": "2", "747": "2",
    "748": "2", "749": "2", "750": "2", "751": "3", "752": "2", "753": "2", "754": "2", "755": "2",
    "756": "2", "757": "2", "758": "2", "759": "2", "760": "1b", "761": "2", "762": "2", "763": "2",
    "764": "1a", "765": "1a", "766": "2", "767": "1a", "768": "2", "769": "2", "770": "2", "771": "1a",
    "772": "1a", "773": "1a",
}  # fmt: skip

# The parts of a test that have an earlier stage. A part is the function name after `test_sft_<NNN>_`,
# with `[<parameter ID>]` for one case. `*` matches any text.
PARTS = {
    "700": {"1a": ["text_integers_json_ids_crcs", "check_on_golden[G01]"]},
    "703": {
        "1a": [
            "version_fields_and_rules[writer_output]", "version_fields_and_rules[pair_version_is_of_its_sidecar]",
            "version_fields_and_rules[unknown_major_*]", "version_fields_and_rules[higher_minor:python_player]",
            "version_fields_and_rules[higher_minor:js]", "version_fields_and_rules[prerelease*]",
            "check_on_golden[G01/*]", "check_on_golden[G10/prerelease_0]", "check_on_golden[results]",
        ],
        "2": [
            "version_fields_and_rules[higher_minor:python_full]", "version_fields_and_rules[higher_minor_journal]",
            "check_on_golden[G03/take]", "descriptor_and_journal_header_on_golden",
        ],
    },
    "705": {"1a": ["names_and_layout"]},
    "706": {"1a": ["renamed_take_folder[player]"]},
    "707": {"1a": ["only_root_and_media_folder[g1]"]},
    "708": {"1a": ["manifest", "check_on_golden"]},
    "709": {"1a": ["summary_is_not_used[g1_*]"]},
    "710": {"1a": ["missing_or_wrong_manifest[audio_only]"]},
    "730": {"1a": ["whole_files_and_live_files", "fsync_provisional", "lock_form"]},
    "733": {"1a": ["repair", "check_on_golden", "camera_file_provisional", "missing_rows_with_no_block"]},
    "736": {"1a": ["camera_configs_by_key[g1]", "confirmed_key", "bad_key_origin[g1_*]", "provisional_key_origin"]},
    "737": {"1a": ["golden_part"], "2": ["golden_part_against_the_parquet"]},
    "744": {"1a": ["hidden_export_files[g1]"]},
    "751": {"2": ["golden_part"]},
    "761": {"1a": ["device_pairs_and_orphan_files[g1_*]"]},
    "762": {"1a": ["refused_pairs_count[g1_*]", "takes_and_counts[g1_*]"]},
    "763": {"1a": ["link_checks_unfinished_files"]},
    "766": {"1a": ["golden_part", "writer_part", "may_contain_private_data[g1_audio_only]"]},
    "768": {
        "1a": [
            "committed_results", "folders_that_the_test_makes[empty-*]", "folders_that_the_test_makes[one_timing_sidecar-*]",
            "folders_that_the_test_makes[only_capture_info-*]", "folders_that_the_test_makes[empty_annotated_video-player]",
            "folders_that_the_test_makes[empty_annotated_video-js]",
        ]
    },
    "769": {
        "1a": [
            "scope_player", "scope_player_against_full[G16]", "scope_player_against_full[G15-v1a]",
            "folder_file_alone[*-player]", "folder_file_alone[*-js]", "committed_results",
        ]
    },
}  # fmt: skip

# In these tests, each other case that reads one golden case with a reader has the stage of that case in
# GOLDEN_STAGES. A case that matches PARTS has the stage of PARTS.
GOLDEN_RULE = {"734", "768", "769"}

# The stage of the `full` result and of the `player` result of each golden case. A key `G<NN>/<case>`
# is for one case, a key `G<NN>` for each other case of the folder.
GOLDEN_STAGES = {
    "G01": ("1a", "1a"), "G02": ("1a", "1a"), "G03": ("2", "1a"), "G04": ("1a", "1a"), "G05": ("1a", "1a"),
    "G06": ("1a", "1a"), "G07": ("2", "1a"), "G08": ("2", "1a"), "G09": ("2", "1a"), "G10/higher_minor": ("2", "1a"),
    "G10/higher_minor_journal": ("2", "1a"), "G10": ("1a", "1a"), "G11": ("1a", "1a"), "G12": ("1a", "1a"),
    "G13": ("2", "1a"), "G14": ("2", "1a"), "G15": ("1a", "1a"), "G16": ("1a", "1a"), "G17": ("1b", "1b"),
    "G18": ("1a", "1a"),
}  # fmt: skip

_SFT = re.compile(r"test_sft_(\d{3})_(\w+)$")

# The only test functions with no SFT ID: they check the fixtures (test_fixtures.py), in stage 1a.
FIXTURE_TESTS = {"test_golden_g01_is_present", "test_reader_has_its_interface"}


def _matches(pattern: str, function: str, name: str) -> bool:
    text = name if "[" in pattern else function
    return re.fullmatch(re.escape(pattern).replace(r"\*", ".*"), text) is not None


def stage_of(item) -> str:
    """The stage of a collected test: `1a`, `1b`, `2`, `3` or `4`. A test with no SFT ID that is not in FIXTURE_TESTS is an error."""
    found = _SFT.match(item.originalname)
    if found is None:
        if item.originalname in FIXTURE_TESTS:
            return "1a"
        raise ValueError(f"{item.nodeid}: a conformance test function must be `test_sft_<NNN>_<part>` (conformance.md, 'The stage of each test')")
    number, function = found.groups()
    name = function + item.name[len(item.originalname) :]
    for stage, patterns in PARTS.get(number, {}).items():
        if any(_matches(pattern, function, name) for pattern in patterns):
            return stage
    params = item.callspec.params if hasattr(item, "callspec") else {}
    if number in GOLDEN_RULE:
        case = f"{params['name']}/{params['case']}" if "name" in params and "case" in params else params.get("case")
        if isinstance(case, str) and "/" in case:
            full, player = GOLDEN_STAGES.get(case) or GOLDEN_STAGES[case.split("/")[0]]
            return player if params.get("kind") in ("player", "js") else full
    return STAGES[number]


def external(program: str):
    """The mark of an external test: `@external("freemocap")` is `@pytest.mark.external("freemocap")`."""
    return pytest.mark.external(program)


def provisional(open_item: str):
    """The mark of a provisional test: `@provisional("DT5")` is `@pytest.mark.provisional("DT5")`."""
    return pytest.mark.provisional(open_item)


# --- Golden folders (SPEC.md Appendix A, "Layout and cases") ---

GOLDEN = ROOT / "golden"


def golden_or_skip(name: str, case: str = "take") -> Path:
    """Return the case folder `recording-files/golden/<name>/<case>`. Skip the test when `recording-files/golden/<name>` is absent."""
    if not (GOLDEN / name).is_dir():
        pytest.skip(f"golden folder {name} is not built yet")
    folder = GOLDEN / name / case
    if not folder.is_dir():
        pytest.fail(f"the golden case `recording-files/golden/{name}/{case}` does not exist", pytrace=False)
    return folder


def expected(name: str, case: str, scope: str) -> bytes:
    """Return the bytes of `recording-files/golden/<name>/<case>.<scope>.json`. `scope` is `full` or `player`."""
    golden_or_skip(name, case)
    return (GOLDEN / name / f"{case}.{scope}.json").read_bytes()


def truth(name: str, case: str):
    """Return the parsed `recording-files/golden/<name>/<case>.truth.json`."""
    import json

    golden_or_skip(name, case)
    return json.loads((GOLDEN / name / f"{case}.truth.json").read_bytes())


@pytest.fixture(name="golden_or_skip")
def _golden_or_skip_fixture():
    """The function `golden_or_skip(name, case="take") -> Path`."""
    return golden_or_skip


@pytest.fixture(name="expected")
def _expected_fixture():
    """The function `expected(name, case, scope) -> bytes`."""
    return expected


@pytest.fixture(name="truth")
def _truth_fixture():
    """The function `truth(name, case) -> dict`."""
    return truth


@pytest.fixture
def variant(tmp_path):
    """A function that copies a golden case to a temporary directory and returns the copy.

    `variant(name, case="take", folder_name=None) -> Path`. The copy keeps the modification times. Its
    folder name is `folder_name`, or the case name. Each call gives a new copy. The test changes the
    copy: a "G3 with X" input is made at test time and is never committed.
    """
    count = 0

    def copy(name: str, case: str = "take", folder_name: str | None = None) -> Path:
        nonlocal count
        source = golden_or_skip(name, case)
        count += 1
        return Path(shutil.copytree(source, tmp_path / f"variant{count}" / (folder_name or case)))

    return copy
