from typing import Type
import pytest

from crummycm.validation.validation import validate
from example_templates.element.multi.a import (
    SINGLE,
    SINGLE_default,
    SINGLE_req_false,
    SINGLE_inner_str,
    SINGLE_homogeneous,
    SINGLE_homogeneous_float,
    SINGLE_default_tup,
    SINGLE_is_list,
    SINGLE_multi_inner_types,
)

ex_config = {
    # as list
    "single_value_provided": (
        ({"my_multi": ["c", "d"]}, SINGLE),
        {"my_multi": ["c", "d"]},
    ),
    "single_value_provided": (({"my_multi": None}, SINGLE), ValueError),
    "single_value_not_provided": (
        ({"my_multi": None}, SINGLE_default),
        {"my_multi": ["a", "b"]},
    ),
    "SINGLE_req_false_a": (
        ({"my_multi": ["c", "d"]}, SINGLE_req_false),
        {"my_multi": ["c", "d"]},
    ),
    "SINGLE_req_false_b": (({"my_multi": None}, SINGLE_req_false), {"my_multi": None}),
    # base inner type
    "SINGLE_inner_str_v": (
        ({"my_multi": ["a", "b"]}, SINGLE_inner_str),
        {"my_multi": ["a", "b"]},
    ),
    "SINGLE_inner_str_i": (({"my_multi": ["a", 1]}, SINGLE_inner_str), TypeError),
    "SINGLE_homogeneous_v_str": (
        ({"my_multi": ["a", "b"]}, SINGLE_homogeneous),
        {"my_multi": ["a", "b"]},
    ),
    "SINGLE_homogeneous_v_int": (
        ({"my_multi": [2, 3]}, SINGLE_homogeneous),
        {"my_multi": [2, 3]},
    ),
    "SINGLE_homogeneous_v_int": (
        ({"my_multi": [2, 3.1]}, SINGLE_homogeneous),
        ValueError,
    ),
    # NOTE: in the strict sense, this is not valid and so a TypeError is thrown
    "SINGLE_homogeneous_v_int_float_i": (
        ({"my_multi": [2, 3.1]}, SINGLE_homogeneous_float),
        TypeError,
    ),
    "SINGLE_homogeneous_v_int_float_v": (
        ({"my_multi": [2.0, 3.1]}, SINGLE_homogeneous_float),
        {"my_multi": [2.0, 3.1]},
    ),
    # as tuple
    "tup_single_value_provided": (
        ({"my_multi": ("c", "d")}, SINGLE),
        {"my_multi": ("c", "d")},
    ),
    "tup_single_value_provided": (({"my_multi": None}, SINGLE), ValueError),
    "tup_single_value_not_provided": (
        ({"my_multi": None}, SINGLE_default_tup),
        {"my_multi": ("a", "b")},
    ),
    "tup_SINGLE_req_false_a": (
        ({"my_multi": ("c", "d")}, SINGLE_req_false),
        {"my_multi": ("c", "d")},
    ),
    "tup_SINGLE_req_false_b": (
        ({"my_multi": None}, SINGLE_req_false),
        {"my_multi": None},
    ),
    # base inner type
    "tup_SINGLE_inner_str_v": (
        ({"my_multi": ("a", "b")}, SINGLE_inner_str),
        {"my_multi": ("a", "b")},
    ),
    "tup_SINGLE_inner_str_i": (({"my_multi": ("a", 1)}, SINGLE_inner_str), TypeError),
    "tup_SINGLE_homogeneous_v_str": (
        ({"my_multi": ("a", "b")}, SINGLE_homogeneous),
        {"my_multi": ("a", "b")},
    ),
    "tup_SINGLE_homogeneous_v_int": (
        ({"my_multi": (2, 3)}, SINGLE_homogeneous),
        {"my_multi": (2, 3)},
    ),
    "tup_SINGLE_homogeneous_v_int": (
        ({"my_multi": (2, 3.1)}, SINGLE_homogeneous),
        ValueError,
    ),
    # NOTE: in the strict sense, this is not valid and so a TypeError is thrown
    "tup_SINGLE_homogeneous_v_int_float_i": (
        ({"my_multi": (2, 3.1)}, SINGLE_homogeneous_float),
        TypeError,
    ),
    "tup_SINGLE_homogeneous_v_int_float_v": (
        ({"my_multi": (2.0, 3.1)}, SINGLE_homogeneous_float),
        {"my_multi": (2.0, 3.1)},
    ),
    "SINGLE_is_list_v": (
        ({"my_multi": ["c", "d"]}, SINGLE_is_list),
        {"my_multi": ["c", "d"]},
    ),
    "SINGLE_is_list_i": (({"my_multi": ("c", "d")}, SINGLE_is_list), TypeError),
    "SINGLE_multi_inner_types_v": (
        ({"my_multi": [1, "d"]}, SINGLE_multi_inner_types),
        {"my_multi": [1, "d"]},
    ),
    "SINGLE_multi_inner_types_i": (
        ({"my_multi": [1, "d", (2,)]}, SINGLE_multi_inner_types),
        TypeError,
    ),
    # compose
    "SINGLE_multi_inner_types_i": (
        ({"my_multi": [1, "d", (2,)]}, SINGLE_multi_inner_types),
        TypeError,
    ),
    # numeric inner
    # # TODO: complex
    # # -- functions
    # "apply_fn_wo_kwargs": (({"my_num": 1}, A_fn_EX_TEMP), {"my_num": 2}),
    # "apply_fn_kwargs": (({"my_num": 1}, A_fn_kwargs_EX_TEMP), {"my_num": 11}),
    # "apply_bad_kwargs": (({"my_num": 0}, A_fn_bad_kwargs_EX_TEMP), ValueError),
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
