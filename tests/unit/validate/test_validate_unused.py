import pytest

from crummycm.validation.validation import validate
from example_templates.component.unused.a import (
    no_catchall,
    inner_multi_catchall,
    inner_single_catchall,
)

ex_config = {
    "disallow_true_valid": (
        (
            {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3}},
            no_catchall,
            True,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3}},
    ),
    "disallow_true_extra_outer": (
        (
            {
                "my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3},
                "no_template": 3,
            },
            no_catchall,
            True,
        ),
        ValueError,
    ),
    "disallow_true_extra_inner": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            no_catchall,
            True,
        ),
        ValueError,
    ),
    "disallow_false_valid": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            no_catchall,
            False,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3}},
    ),
    "disallow_false_extra_outer": (
        (
            {
                "my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3},
                "no_template": 3,
            },
            no_catchall,
            False,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3}},
    ),
    "inner_multi_catchall": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "wild_card": 2.3,
                    "another": 9,
                }
            },
            inner_multi_catchall,
            True,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3, "another": 9}},
    ),
    "inner_multi_catchall_a": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "wild_card": 2.3,
                    "another_a": 9,
                }
            },
            inner_multi_catchall,
            True,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3, "another_a": 9}},
    ),
    "inner_multi_catchall_b": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "wild_card": 2.3,
                    "another_a": 9,
                    "another_b": 9,
                }
            },
            inner_multi_catchall,
            True,
        ),
        {
            "my_mixed": {
                "kd_num": 0,
                "my_str": "Jack",
                "wild_card": 2.3,
                "another_a": 9,
                "another_b": 9,
            }
        },
    ),
    "inner_single_catchall_a": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "wild_card": 2.3,
                    "another_a": 9,
                }
            },
            inner_single_catchall,
            True,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "wild_card": 2.3, "another_a": 9}},
    ),
    "inner_single_catchall_b": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "wild_card": 2.3,
                    "another_a": 9,
                    "another_b": 9,
                }
            },
            inner_single_catchall,
            True,
        ),
        ValueError,
    ),
}


def call(config):
    raw_dict = validate(config[0], config[1], config[2])
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

