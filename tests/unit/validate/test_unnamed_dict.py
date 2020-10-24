import pytest

from crummycm.validate import validate
from example_templates.component.unnamed.a import (
    A_ex,
    A_unnamed_single_num_ex,
    A_unnamed_single_num_multi_ex,
    A_unnamed_single_num_startswith_ex,
    A_unnamed_single_num_endswith_ex,
    A_nested_unnamed_num,
    A_quad_nested_unnamed_num,
    A_unnamed_out,
    A_unnamed_double_dist,
)

ex_config = {
    "two_elements_both_provided": (({"val": 4}, A_ex), {"val": 4}),
    "single_unnamed_num": (
        ({"config": {"some_user_defined_string": 4}}, A_unnamed_single_num_ex),
        {"config": {"some_user_defined_string": 4}},
    ),
    "single_unnamed_num_starts_with_valid": (
        ({"config": {"val_the_thing": 4}}, A_unnamed_single_num_startswith_ex),
        {"config": {"val_the_thing": 4}},
    ),
    "single_unnamed_num_starts_with_invalid": (
        ({"config": {"the_thing": 4}}, A_unnamed_single_num_startswith_ex),
        ValueError,
    ),
    "single_unnamed_num_starts_with_valid": (
        ({"config": {"the_thing_val": 4}}, A_unnamed_single_num_endswith_ex),
        {"config": {"the_thing_val": 4}},
    ),
    "single_unnamed_num_starts_with_invalid": (
        ({"config": {"the_thing": 4}}, A_unnamed_single_num_endswith_ex),
        ValueError,
    ),
    "single_unnamed_num_num_as_key": (
        ({"config": {3: 4}}, A_unnamed_single_num_ex),
        {"config": {3: 4}},
    ),
    "multi_unnamed_num": (
        ({"config": {"a": 4, "b": 3, "c": 2}}, A_unnamed_single_num_multi_ex),
        {"config": {"a": 4, "b": 3, "c": 2}},
    ),
    "multi_unnamed_bad_type": (
        ({"config": {"a": 4, "b": 3, "c": "3"}}, A_unnamed_single_num_multi_ex),
        TypeError,
    ),
    "triple_nested_unnamed_num": (
        ({"config": {"my_dict": {"user_val": 3}}}, A_nested_unnamed_num),
        {"config": {"my_dict": {"user_val": 3}}},
    ),
    "quad_nested_unnamed_num": (
        (
            {"config": {"1st": {"2nd": {"third": {"fourth": 4}}}}},
            A_quad_nested_unnamed_num,
        ),
        {"config": {"1st": {"2nd": {"third": {"fourth": 4}}}}},
    ),
    "user_named_out": (({"my_conf": 3}, A_unnamed_out), {"my_conf": 3}),
    "nested_unnamed_num": (
        ({"config": {"personal_key": 3, "up_val": 4}}, A_unnamed_double_dist),
        {"config": {"personal_key": 3, "up_val": 4}},
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
