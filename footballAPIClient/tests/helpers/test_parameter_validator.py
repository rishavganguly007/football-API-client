

from footballAPIClient.helpers.ParameterValidator import ParameterValidator
import pytest


def test_validate_account_header_type():
    with pytest.raises(ValueError):
        ParameterValidator.validate_account_header_type("invalid-header")

def test_check_missing_params():
    assert ParameterValidator.check_missing_params(None, None, None) is True
    assert ParameterValidator.check_missing_params(None, "param2", None) is False

def test_validate_type_str():
    assert ParameterValidator.validate_type_str("test_string", "field_name") is None
    with pytest.raises(TypeError):
        ParameterValidator.validate_type_str(123, "field_name")

def test_validate_type_int():
    with pytest.raises(TypeError):
        ParameterValidator.validate_type_int("not-an-int", "field_name")

def test_validate_player_fields():
    with pytest.raises(ValueError):
        ParameterValidator.validate_player_fields(search="search_value")

def test_validate_search_field():
    with pytest.raises(ValueError):
        ParameterValidator.validate_search_field("ab")

def test_validate_player_search_field():
    with pytest.raises(ValueError):
        ParameterValidator.validate_player_search_field("abc")

def test_validate_code_field():
    with pytest.raises(LookupError):
        ParameterValidator.validate_code_field("invalid-code")

def test_validate_season_field():
    assert ParameterValidator.validate_season_field("2023") is None
    assert ParameterValidator.validate_season_field("9999") is None
    assert ParameterValidator.validate_season_field("0000") is None
    with pytest.raises(ValueError):
        ParameterValidator.validate_season_field("not-an-int")
        ParameterValidator.validate_season_field("111")
        ParameterValidator.validate_season_field("00000")