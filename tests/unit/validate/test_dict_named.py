import pytest

from crummycm.validation.validation import validate
from example_templates.component.named.a import (
    A_named_single,
    A_named_double,
    A_named_outer_single,
    A_named_outer_double,
)


ex_config = {
    "basic_known_single": (
        ({"known_dict": {"some_thing": 1234}}, A_named_single),
        {"known_dict": {"some_thing": 1234}},
    ),
    "basic_known_double": (
        ({"known_dict": {"a": 12, "b": "Jack"}}, A_named_double),
        {"known_dict": {"a": 12, "b": "Jack"}},
    ),
    "basic_known_outer_single": (
        ({"some_thing": 1234}, A_named_outer_single),
        {"some_thing": 1234},
    ),
    "basic_known_outer_double": (
        ({"a": 12, "b": "Jack"}, A_named_outer_double),
        {"a": 12, "b": "Jack"},
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
