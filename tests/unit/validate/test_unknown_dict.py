import pytest

from crummycm.validation.validation import validate
from example_templates.component.unknown.a import A_inner_unknown, A_outer_unknown

ex_config = {
    "some_config": (
        ({"some_config": {"my_val": 4}}, A_inner_unknown),
        {"some_config": {"my_val": 4}},
    ),
    "nested_unknown": (
        ({"some_config": {"kd_num": 3, "uk_dict": {"user_num": 4}}}, A_inner_unknown),
        {"some_config": {"kd_num": 3, "uk_dict": {"user_num": 4}}},
    ),
    "outter_config": (({"anything": 3}, A_outer_unknown), {"anything": 3}),
    "anything_config": (
        ({"anything": {"doesnt_matter": {"ok": 3}}}, A_outer_unknown),
        {"anything": {"doesnt_matter": {"ok": 3}}},
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
