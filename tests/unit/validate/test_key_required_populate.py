import pytest

from crummycm.validation.validation import validate
from example_templates.component.optional.a import (
    required_num_false,
    required_num_true,
    required_num_true_true,
    required_num_true_false,
    required_num_true_false_default,
    required_num_false_true,
    req_unknown,
    req_unknown_populate,
    req_unnammed_populate,
    req_unnammed_populate_nested,
    req_unnammed_double_nested_outer_pop,
    req_unnammed_double_nested_inner_pop,
)

ex_config = {
    "optional_num_false": (
        ({"my_conf": {"my_num": 0}}, required_num_false),
        {"my_conf": {"my_num": 0}},
    ),
    "optional_num_true": (({"my_conf": {}}, required_num_true), ValueError),
    "required_num_true_true_v": (
        ({"my_conf": {"my_text": "jack"}}, required_num_true_true),
        {"my_conf": {"my_text": "jack"}},
    ),
    "required_num_true_false_v": (
        ({"my_conf": {"my_text": "jack"}}, required_num_true_false),
        {"my_conf": {"my_text": "jack"}},
    ),
    "required_num_true_true_i": (
        ({"my_conf": {"my_text": None}}, required_num_true_true),
        ValueError,
    ),
    "required_num_true_false_i": (
        ({"my_conf": {"my_text": None}}, required_num_true_false),
        {"my_conf": {"my_text": None}},
    ),
    "required_num_true_false_default_v": (
        ({"my_conf": {"my_text": None}}, required_num_true_false_default),
        {"my_conf": {"my_text": "Jack"}},
    ),
    "required_num_true_false_default_i": (
        ({"my_conf": {"my_text": "Diesel"}}, required_num_true_false_default),
        {"my_conf": {"my_text": "Diesel"}},
    ),
    "required_num_false_true_v": (
        ({"my_conf": {}}, required_num_false_true),
        {"my_conf": {}},
    ),
    "required_unknown": (({"my_conf": {}}, req_unknown), {"my_conf": {}}),
    "required_unknown_populate": (
        ({"my_conf": {}}, req_unknown_populate),
        {"my_conf": {"my_text": None}},
    ),
    "req_unnammed_populate": (
        ({"my_conf": {}}, req_unnammed_populate),
        {"my_conf": {"my_text": "hello"}},
    ),
    "req_unnammed_populate_b": (
        ({"my_conf": {"my_text": None}}, req_unnammed_populate),
        {"my_conf": {"my_text": "hello"}},
    ),
    "req_unnammed_populate_nested_a": (
        ({"my_conf": {"my_text": {"inner_text": None}}}, req_unnammed_populate_nested),
        {"my_conf": {"my_text": {"inner_text": "hello"}}},
    ),
    "req_unnammed_populate_nested_a": (
        ({"my_conf": {}}, req_unnammed_populate_nested),
        {"my_conf": {"my_text": {"inner_text": "hello"}}},
    ),
    "req_unnammed_double_nested_outer_prop_a": (
        ({"my_conf": {}}, req_unnammed_double_nested_outer_pop),
        {"my_conf": {"my_inner": {"my_double_inner": {"inner_text": "hello"}}}},
    ),
    # NOTE: I currently like this approach since the value is not a ValuePlaceholder
    "req_unnammed_double_nested_outer_prop_none": (
        ({"my_conf": None}, req_unnammed_double_nested_outer_pop),
        ValueError,
    ),
    "req_unnammed_double_nested_outer_prop_b": (
        (
            {"my_conf": {"my_inner": {"my_double_inner": {"inner_text": "hello"}}}},
            req_unnammed_double_nested_outer_pop,
        ),
        {"my_conf": {"my_inner": {"my_double_inner": {"inner_text": "hello"}}}},
    ),
    "req_unnammed_double_nested_inner_pop_a": (
        ({"my_conf": {"my_inner": {}}}, req_unnammed_double_nested_inner_pop),
        {"my_conf": {"my_inner": {"my_double_inner": {"inner_text": "hello"}}}},
    ),
    # if the user supplies the key, it is expected they will also supply the
    # value(s) when the object is another dict/BaseDict/non-standard value
    # NOTE: if the None is {}, the error is cryptic a `KeyError`, not a
    # `ValueError`.. this might need to be adjusted at some point
    "req_unnammed_double_nested_inner_pop_b": (
        (
            {"my_conf": {"my_inner": {"my_double_inner": None}}},
            req_unnammed_double_nested_inner_pop,
        ),
        ValueError,
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

