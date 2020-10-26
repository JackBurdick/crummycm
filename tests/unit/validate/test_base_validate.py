import pytest

from crummycm.validation.validation import validate
from example_templates.base.a import (
    A_EX_TEMP,
    A_bool_EX_TEMP,
    A_float_EX_TEMP,
    A_fn_bad_kwargs_EX_TEMP,
    A_fn_EX_TEMP,
    A_fn_kwargs_EX_TEMP,
    A_int_EX_TEMP,
    A_required_EX_TEMP,
    A_str_EX_TEMP,
)

ex_config = {
    "single_value_provided": (({"name": "Jack"}, A_EX_TEMP), {"name": "Jack"}),
    "no_default_provided": (({}, A_EX_TEMP), {"name": "Sam"}),
    "required_provided": (({"name": "Jack"}, A_required_EX_TEMP), {"name": "Jack"}),
    "required_not_provided": (({"name": None}, A_required_EX_TEMP), ValueError),
    "str_correct_type_provided": (({"name": "Jack"}, A_str_EX_TEMP), {"name": "Jack"}),
    "str_incorrect_type_provided": (({"name": 3}, A_str_EX_TEMP), TypeError),
    "int_correct_type_provided": (({"name": 3}, A_int_EX_TEMP), {"name": 3}),
    "int_incorrect_type_provided": (
        ({"name": "some_string"}, A_int_EX_TEMP),
        TypeError,
    ),
    "int_disallow_float_provided": (({"name": 3.3}, A_int_EX_TEMP), TypeError),
    "bool_correct_type_provided": (({"name": True}, A_bool_EX_TEMP), {"name": True}),
    "bool_incorrect_type_provided": (
        ({"name": "some_string"}, A_bool_EX_TEMP),
        TypeError,
    ),
    "float_correct_type_provided": (({"name": 3.3}, A_float_EX_TEMP), {"name": 3.3}),
    "float_incorrect_type_provided": (
        ({"name": "some_string"}, A_float_EX_TEMP),
        TypeError,
    ),
    "float_allow_int_type_provided": (({"name": 3}, A_float_EX_TEMP), {"name": 3.0}),
    "apply_fn_wo_kwargs": (({"name": "Jack"}, A_fn_EX_TEMP), {"name": "Jackaaa"}),
    "apply_fn_kwargs": (({"name": "Jack"}, A_fn_kwargs_EX_TEMP), {"name": "Jackbb"}),
    "apply_bad_kwargs": (({"name": "Jack"}, A_fn_bad_kwargs_EX_TEMP), ValueError),
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
    else:
        raise ValueError(f"expected {expected} not accounted for")
