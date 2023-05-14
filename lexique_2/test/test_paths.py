from pathlib import Path


def test_data_test_grammar():
    from lexique_2.paths import get_data_test_grammar
    assert get_data_test_grammar().is_dir()
    assert get_data_test_grammar().exists()
    assert get_data_test_grammar().name == "grammar"
    assert get_data_test_grammar() == Path(__file__).parent / "data_for_test/grammar"
