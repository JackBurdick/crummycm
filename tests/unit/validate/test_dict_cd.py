import pytest

from crummycm.validation.validation import validate
from example_templates.component.config_dict.a import (
    cd_outer,
    no_cd_single,
    no_cd_single_nested,
)

ex_config = {
    "cd_outer": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            cd_outer,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3}},
    ),
    "no_cd_single": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            no_cd_single,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3}},
    ),
    "no_cd_single_nested": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                    "nested_md": {
                        "kd_num": 0,
                        "my_str": "Jack",
                        "my_num": 11,
                        "wild_card": 2.3,
                    },
                }
            },
            no_cd_single_nested,
        ),
        {
            "my_mixed": {
                "kd_num": 0,
                "my_str": "Jack",
                "my_num": 11,
                "wild_card": 2.3,
                "nested_md": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
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

