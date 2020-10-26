import pytest

from crummycm.validation.validation import validate
from example_templates.component.unknown.a import (
    A_inner_unknown,
    A_inner_unknown_multi,
    A_outer_unknown,
    A_inner_unknown_required_false,
    A_outer_unknown_req_false,
    double_inner_unknown,
    double_inner_unknown_multi,
    double_inner_unknown_unstrict_multi,
    double_inner_unknown_mixed_req_multi,
    double_inner_unknown_mixed_req_multi_b,
)

ex_config = {
    "some_config": (
        ({"some_config": {"my_val": 4}}, A_inner_unknown),
        {"some_config": {"my_val": 4}},
    ),
    "nested_unknown_not_spec_as_many": (
        ({"some_config": {"kd_num": 3, "uk_dict": {"user_num": 4}}}, A_inner_unknown),
        ValueError,
    ),
    "nested_unknown_spec_as_many": (
        (
            {"some_config": {"kd_num": 3, "uk_dict": {"user_num": 4}}},
            A_inner_unknown_multi,
        ),
        {"some_config": {"kd_num": 3, "uk_dict": {"user_num": 4}}},
    ),
    "outter_config": (({"anything": 3}, A_outer_unknown), {"anything": 3}),
    "anything_config": (
        ({"anything": {"doesnt_matter": {"ok": 3}}}, A_outer_unknown),
        {"anything": {"doesnt_matter": {"ok": 3}}},
    ),
    "A_inner_unknown_required_false_a": (
        ({"some_config": {"doesnt_matter": {"ok": 3}}}, A_inner_unknown_required_false),
        {"some_config": {"doesnt_matter": {"ok": 3}}},
    ),
    "A_inner_unknown_required_false_b": (
        ({"some_config": {}}, A_inner_unknown_required_false),
        ValueError,
    ),
    "A_inner_unknown_required_false_c": (
        ({"some_config": {"hello": None}}, A_inner_unknown_required_false),
        {"some_config": {"hello": None}},
    ),
    "A_outer_unknown_req_false_a": (
        ({"anything": 4}, A_outer_unknown_req_false),
        {"anything": 4},
    ),
    "A_outer_unknown_req_false_b": (
        ({"anything": {"my_val": 4}}, A_outer_unknown_req_false),
        {"anything": {"my_val": 4}},
    ),
    "A_outer_unknown_req_false_c": (({}, A_outer_unknown_req_false), ValueError),
    "A_outer_unknown_req_false_d": ((None, A_outer_unknown_req_false), ValueError),
    "req_outter_empty": (({}, A_outer_unknown), ValueError),
    "req_inner_empty": (({"some_config": {}}, A_inner_unknown), ValueError),
    "double_inner_unknown_a": (
        ({"some_config": {"my_val": 4, "other": 2}}, double_inner_unknown),
        {"some_config": {"my_val": 4, "other": 2}},
    ),
    "double_inner_unknown_b_no_user_keys_for_req": (
        ({"some_config": {"my_val": 4, "my_other": 2}}, double_inner_unknown),
        ValueError,
    ),
    "double_inner_unknown_b_no_user_keys_for_req": (
        ({"some_config": {"my_val": 4, "my_other": 2}}, double_inner_unknown),
        ValueError,
    ),
    "double_inner_not_multi": (
        (
            {"some_config": {"my_val": 4, "my_other_val": 0, "other": 2}},
            double_inner_unknown,
        ),
        ValueError,
    ),
    "double_inner_unknown_multi": (
        (
            {"some_config": {"my_val": 4, "my_other_val": 0, "other": 2}},
            double_inner_unknown_multi,
        ),
        {"some_config": {"my_val": 4, "my_other_val": 0, "other": 2}},
    ),
    "double_inner_unknown_unstrict_multi_a": (
        (
            {"some_config": {"my_val": 4, "other_other": 0, "other": 2}},
            double_inner_unknown_unstrict_multi,
        ),
        {"some_config": {"my_val": 4, "other_other": 0, "other": 2}},
    ),
    "double_inner_unknown_unstrict_multi_b": (
        (
            {"some_config": {"my_val": 4, "other_other": 0, "other": 2}},
            double_inner_unknown,
        ),
        ValueError,
    ),
    "double_inner_unknown_mixed_req_multi_a": (
        (
            {"some_config": {"my_val": 4, "my_other_val": 0, "other": 2}},
            double_inner_unknown_mixed_req_multi,
        ),
        {"some_config": {"my_val": 4, "my_other_val": 0, "other": 2}},
    ),
    "double_inner_unknown_mixed_req_multi_b": (
        (
            {"some_config": {"my_val": 4, "my_other_val": 0}},
            double_inner_unknown_mixed_req_multi,
        ),
        {"some_config": {"my_val": 4, "my_other_val": 0}},
    ),
    "double_inner_unknown_mixed_req_multi_c": (
        (
            {"some_config": {"my_val": 4, "my_other_val": 0}},
            double_inner_unknown_mixed_req_multi_b,
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
    elif expected is None:
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
