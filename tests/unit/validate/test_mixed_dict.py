import pytest

from crummycm.validation.validation import validate
from example_templates.component.mixed_keys.a import (
    A_mixed_all_single,
    A_mixed_outter,
    A_mixed_all_single_nested,
    A_mixed_outter_nested,
    mixed_all_single_key_unnamed_req_false,
    mixed_all_single_key_unnamed_req_false_v_req_false,
    mixed_all_single_key_unnamed_req_false_v_req_false_default,
)

ex_config = {
    "mixed_inner": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            A_mixed_all_single,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3}},
    ),
    "mixed_all_single_key_known_req_false_a": (
        (
            {"my_mixed": {"kd_num": 0, "my_num": 11, "wild_card": 2.3}},
            mixed_all_single_key_unnamed_req_false,
        ),
        {"my_mixed": {"kd_num": 0, "my_num": 11, "wild_card": 2.3}},
    ),
    "mixed_all_single_key_known_req_false_b": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            mixed_all_single_key_unnamed_req_false,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3}},
    ),
    "mixed_all_single_key_known_req_false_i": (
        (
            {"my_mixed": {"kd_num": 0, "my_num": 11, "my_str": None, "wild_card": 2.3}},
            mixed_all_single_key_unnamed_req_false,
        ),
        ValueError,
    ),
    "mixed_all_single_key_unnamed_req_false_v_req_false_a": (
        (
            {"my_mixed": {"kd_num": 0, "my_num": 11, "wild_card": 2.3}},
            mixed_all_single_key_unnamed_req_false_v_req_false,
        ),
        {"my_mixed": {"kd_num": 0, "my_num": 11, "wild_card": 2.3}},
    ),
    "mixed_all_single_key_unnamed_req_false_v_req_false_b": (
        (
            {"my_mixed": {"kd_num": 0, "my_str": None, "my_num": 11, "wild_card": 2.3}},
            mixed_all_single_key_unnamed_req_false_v_req_false,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": None, "my_num": 11, "wild_card": 2.3}},
    ),
    "mixed_all_single_key_unnamed_req_false_v_req_false_def_a": (
        (
            {"my_mixed": {"kd_num": 0, "my_num": 11, "wild_card": 2.3}},
            mixed_all_single_key_unnamed_req_false_v_req_false_default,
        ),
        {"my_mixed": {"kd_num": 0, "my_num": 11, "wild_card": 2.3}},
    ),
    "mixed_all_single_key_unnamed_req_false_v_req_false_def_b": (
        (
            {"my_mixed": {"kd_num": 0, "my_num": 11, "my_str": None, "wild_card": 2.3}},
            mixed_all_single_key_unnamed_req_false_v_req_false_default,
        ),
        {"my_mixed": {"kd_num": 0, "my_num": 11, "my_str": "DIESEL", "wild_card": 2.3}},
    ),
    "mixed_outter": (
        (
            {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3},
            A_mixed_outter,
        ),
        {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3},
    ),
    "mixed_inner_nested": (
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
            A_mixed_all_single_nested,
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
    "mixed_outter_nested": (
        (
            {
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
            },
            A_mixed_outter_nested,
        ),
        {
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

