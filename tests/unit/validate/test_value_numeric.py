import pytest

from crummycm.validation.validation import validate
from example_templates.element.numeric.a import (
    A_EX_TEMP,
    A_float_EX_TEMP,
    A_fn_bad_kwargs_EX_TEMP,
    A_fn_EX_TEMP,
    A_fn_kwargs_EX_TEMP,
    A_int_EX_TEMP,
    A_required_EX_TEMP,
    numeric_bounds_inf,
    numeric_bounds_1_1,
    numeric_bounds_1_1_inc,
)

ex_config = {
    "single_value_provided": (({"my_num": 1}, A_EX_TEMP), {"my_num": 1}),
    "no_val_default_provided": (({}, A_EX_TEMP), {"my_num": 0}),
    "required_provided": (({"my_num": 3.3}, A_required_EX_TEMP), {"my_num": 3.3}),
    "required_not_provided": (({"my_num": None}, A_required_EX_TEMP), ValueError),
    # -- types
    # int
    "int_correct_type_provided": (({"my_num": 2}, A_int_EX_TEMP), {"my_num": 2}),
    "int_incorrect_str_type_provided": (({"my_num": "jack"}, A_int_EX_TEMP), TypeError),
    "int_incorrect_cmplx_type_provided": (({"my_num": 3j}, A_int_EX_TEMP), TypeError),
    # float
    "float_correct_type_int_provided": (
        ({"my_num": 2}, A_float_EX_TEMP),
        {"my_num": 2},
    ),
    "float_correct_type_float_provided": (
        ({"my_num": 2.3}, A_float_EX_TEMP),
        {"my_num": 2.3},
    ),
    "float_incorrect_type_provided": (({"my_num": "Jack"}, A_float_EX_TEMP), TypeError),
    # TODO: complex
    # -- functions
    "apply_fn_wo_kwargs": (({"my_num": 1}, A_fn_EX_TEMP), {"my_num": 2}),
    "apply_fn_kwargs": (({"my_num": 1}, A_fn_kwargs_EX_TEMP), {"my_num": 11}),
    "apply_bad_kwargs": (({"my_num": 0}, A_fn_bad_kwargs_EX_TEMP), ValueError),
    "bounds_inf_positive_v": (({"my_num": 0}, numeric_bounds_inf), {"my_num": 0}),
    "bounds_inf_positive_i": (({"my_num": -1}, numeric_bounds_inf), ValueError),
    "bounds_inclusive_t": (({"my_num": 0}, numeric_bounds_1_1), {"my_num": 0}),
    "bounds_inclusive_pos_f": (({"my_num": 1}, numeric_bounds_1_1), ValueError),
    "bounds_inclusive_neg_f": (({"my_num": -1}, numeric_bounds_1_1), ValueError),
    "bounds_inclusive_inc_t_pos": (
        ({"my_num": 1}, numeric_bounds_1_1_inc),
        {"my_num": 1},
    ),
    "bounds_inclusive_inc_t_neg": (
        ({"my_num": -1}, numeric_bounds_1_1_inc),
        {"my_num": -1},
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
