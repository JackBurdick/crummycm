import pytest

from crummycm.validation.validation import validate
from example_templates.element.text.a import (
    A_EX_TEMP,
    A_contains_one_of_true,
    A_contains_true,
    A_ends_with_True,
    A_fn,
    A_fn_bad_kwargs,
    A_fn_kwargs,
    A_is_in_list_true,
    A_required_EX_TEMP,
    A_starts_with_True,
    A_to_lower,
)

ex_config = {
    "single_value_provided": (({"my_text": "Jack"}, A_EX_TEMP), {"my_text": "Jack"}),
    "no_value_provided": (({"my_text": None}, A_EX_TEMP), {"my_text": "Jack"}),
    "required_provided": (
        ({"my_text": "Jack"}, A_required_EX_TEMP),
        {"my_text": "Jack"},
    ),
    "required_key_not_provided": (({}, A_required_EX_TEMP), KeyError),
    "required_value_not_provided": (
        ({"my_text": None}, A_required_EX_TEMP),
        ValueError,
    ),
    "to_lower_true": (({"my_text": "Jack"}, A_to_lower), {"my_text": "jack"}),
    "provided_is_in_list_true": (
        ({"my_text": "Jack"}, A_is_in_list_true),
        {"my_text": "Jack"},
    ),
    "provided_is_not_in_list_true": (
        ({"my_text": "Siren"}, A_is_in_list_true),
        ValueError,
    ),
    "A_contains_true": (
        ({"my_text": "Jack.jpg"}, A_contains_true),
        {"my_text": "Jack.jpg"},
    ),
    "A_contains_false": (({"my_text": "Jack.png"}, A_contains_true), ValueError),
    "A_contains_true": (
        ({"my_text": "Jack.jpg"}, A_contains_one_of_true),
        {"my_text": "Jack.jpg"},
    ),
    "A_contains_false": (({"my_text": "Jack.xxx"}, A_contains_one_of_true), ValueError),
    "A_startswith_true": (
        ({"my_text": "jack.jpg"}, A_starts_with_True),
        {"my_text": "jack.jpg"},
    ),
    "A_startswith_false": (({"my_text": "xack.jpg"}, A_starts_with_True), ValueError),
    "A_endswith_true": (
        ({"my_text": "jack.jpg"}, A_ends_with_True),
        {"my_text": "jack.jpg"},
    ),
    "A_endswith_false": (({"my_text": "xack.png"}, A_ends_with_True), ValueError),
    "A_fn_true": (({"my_text": "jack"}, A_fn), {"my_text": "jackB"}),
    "A_fn_kwargs_true": (({"my_text": "jack"}, A_fn_kwargs), {"my_text": "jackBBB"}),
    "A_fn_bad_kwargs_true": (({"my_text": "jack"}, A_fn_bad_kwargs), ValueError),
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
