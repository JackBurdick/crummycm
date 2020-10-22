import pytest

from crummycm.validate import validate
from example_templates.component.known.a import (
    A_ex,
    A_named_ex,
    A_named_out,
    A_nested_known_ex,
    A_extra_nested_known_ex,
)

ex_config = {
    "two_elements_both_provided": (
        ({"my_str": "Jack", "my_num": 1}, A_ex),
        {"my_str": "Jack", "my_num": 1},
    ),
    "two_elements_neither_provided_default": (
        ({}, A_ex),
        {"my_str": "Jack", "my_num": 0},
    ),
    "two_elements_neither_provided_default": (
        ({"my_num": 3}, A_named_out),
        {"my_num": 3},
    ),
    "named_dict": (
        ({"config": {"my_str": "Jack", "my_num": 1}}, A_named_ex),
        {"config": {"my_str": "Jack", "my_num": 1}},
    ),
    "nested_named_dict": (
        (
            {"config": {"my_dict": {"my_str": "Jack", "my_num": 1}, "my_num": 0}},
            A_nested_known_ex,
        ),
        {"config": {"my_num": 0, "my_dict": {"my_num": 1, "my_str": "Jack"}}},
    ),
    "extra_nested_named_dict": (
        (
            {
                "config": {
                    "my_num": 0,
                    "my_dict": {
                        "my_inner_dict": {
                            "my_val": 2,
                            "my_extra_inner_dict": {"my_num": 3.3, "my_str": "Jack"},
                        },
                        "my_str": "Diesel",
                    },
                }
            },
            A_extra_nested_known_ex,
        ),
        {
            "config": {
                "my_num": 0,
                "my_dict": {
                    "my_inner_dict": {
                        "my_val": 2,
                        "my_extra_inner_dict": {"my_num": 3.3, "my_str": "Jack"},
                    },
                    "my_str": "Diesel",
                },
            }
        },
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
