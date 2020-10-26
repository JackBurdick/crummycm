import pytest

from crummycm.validation.validation import validate
from example_templates.component.mixed.a import (
    A_known_uk,
    A_uk_k,
    A_outter_nested_uk_uk,
)

ex_config = {
    "known_contains_unknown": (
        ({"known_dict": {"kd_num": 3, "uk_dict": {"user_num": 4}}}, A_known_uk),
        {"known_dict": {"kd_num": 3, "uk_dict": {"user_num": 4}}},
    ),
    "unknown_known": (
        ({"my_conf": {"user_kd": {"my_num": 4}}}, A_uk_k),
        {"my_conf": {"user_kd": {"my_num": 4}}},
    ),
    "outter_uk_nested_uk_uk": (
        ({"xxxx": {"yyyy": 4}}, A_outter_nested_uk_uk),
        {"xxxx": {"yyyy": 4}},
    ),
}


def call(config):
    raw_dict = validate(config[0], config[1])
    return raw_dict


@pytest.mark.parametrize(
    "config,expected", ex_config.values(), ids=list(ex_config.keys())
)
def test_basic_parse(config, expected):
    """test whether the user input can be parsed to a dict"""
    if isinstance(expected, dict):
        raw_dict = call(config)
        assert expected == raw_dict
    elif issubclass(expected, ValueError):
        with pytest.raises(ValueError):
            raw_dict = call(config)
    elif issubclass(expected, FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            raw_dict = call(config)
    elif issubclass(expected, TypeError):
        with pytest.raises(TypeError):
            raw_dict = call(config)
    elif issubclass(expected, KeyError):
        with pytest.raises(KeyError):
            raw_dict = call(config)
    else:
        raise ValueError(f"expected {expected} not accounted for")
