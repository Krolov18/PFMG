def test_data_test_grammar():
    from utils.paths import get_data_test_grammar
    assert get_data_test_grammar().exists()
    assert get_data_test_grammar().is_dir()
    assert get_data_test_grammar().name == "data_for_test"
