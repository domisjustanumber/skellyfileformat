"""A placeholder that shows that the collection and the fixtures work. The tests of conformance.md replace it."""


def test_golden_g01_is_present(golden):
    case = golden("G01")
    assert case.with_name("take.full.json").is_file() and case.with_name("take.player.json").is_file()


def test_reader_has_its_interface(reader):
    assert callable(reader.read_folder) and callable(reader.canonical_json)
