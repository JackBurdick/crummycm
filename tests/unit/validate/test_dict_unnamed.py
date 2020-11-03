import pytest

from crummycm.validation.validation import validate
from example_templates.component.unnamed.a import (
    A_ex,
    A_unnamed_single_num_ex,
    A_unnamed_single_num_multi_ex,
    A_unnamed_single_num_startswith_ex,
    A_unnamed_single_num_endswith_ex,
    A_unnamed_single_num_endswith_req,
    A_unnamed_single_exact,
    A_nested_unnamed_num,
    A_quad_nested_unnamed_num,
    A_unnamed_out,
    A_unnamed_double_dist,
    A_unnamed_triple_dist,
    A_unnamed_quad_dist,
    A_unnamed_quad_inner_quad,
    A_unnamed_quad_nested_inner_quad,
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
        ({"config": {"val_the_thing": None}}, A_unnamed_single_num_startswith_ex),
        {"config": {"val_the_thing": 0}},
    ),
    "single_unnamed_num_ends_with_valid": (
        ({"config": {"the_thing_val": 4}}, A_unnamed_single_num_endswith_ex),
        {"config": {"the_thing_val": 4}},
    ),
    "single_unnamed_num_ends_with_invalid": (
        ({"config": {"the_thing_val": None}}, A_unnamed_single_num_endswith_ex),
        {"config": {"the_thing_val": 0}},
    ),
    "single_unnamed_num_ends_with_req_v": (
        ({"config": {"the_thing_val": 3}}, A_unnamed_single_num_endswith_req),
        {"config": {"the_thing_val": 3}},
    ),
    "single_unnamed_num_ends_with_req_i": (
        ({"config": {"the_thing_val": None}}, A_unnamed_single_num_endswith_req),
        {"config": {"the_thing_val": 0}},
    ),
    "single_exact_v": (
        ({"config": {"some_key": None}}, A_unnamed_single_exact),
        {"config": {"some_key": 2}},
    ),
    "single_exact_i": (
        ({"config": {"v_some_key": None}}, A_unnamed_single_exact),
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
    "nested_unnamed_num_multi_2": (
        (
            {"config": {"personal_key": 3, "up_val": 4, "down_val": 2, "side_val": 3}},
            A_unnamed_double_dist,
        ),
        {"config": {"personal_key": 3, "up_val": 4, "down_val": 2, "side_val": 3}},
    ),
    "nested_unnamed_num_multi_1": (
        (
            {
                "config": {
                    "personal_key": 3,
                    "up_val": 4,
                    "down_val": 2,
                    "side_val": 3,
                    "val_up": 6,
                    "val_down": 7,
                    "val_side": 8,
                }
            },
            A_unnamed_triple_dist,
        ),
        {
            "config": {
                "personal_key": 3,
                "up_val": 4,
                "down_val": 2,
                "side_val": 3,
                "val_up": 6,
                "val_down": 7,
                "val_side": 8,
            }
        },
    ),
    "nested_unnamed_num_multi_0": (
        (
            {
                "config": {
                    "personal_key": 3,
                    "up_val": 4,
                    "down_val": 2,
                    "side_val": 3,
                    "val_up": 6,
                    "val_down": 7,
                    "val_side": 8,
                    "x_a": 10,
                    "x_b": 11,
                }
            },
            A_unnamed_quad_dist,
        ),
        {
            "config": {
                "personal_key": 3,
                "up_val": 4,
                "down_val": 2,
                "side_val": 3,
                "val_up": 6,
                "val_down": 7,
                "val_side": 8,
                "x_a": 10,
                "x_b": 11,
            }
        },
    ),
    "nested_unnamed_nest_multi_a": (
        (
            {
                "config": {
                    "personal_key": {
                        "jack": 0,
                        "next_up_val": 4,
                        "next_down_val": 2,
                        "next_side_val": 3,
                        "val_next_up": 6,
                        "val_next_down": 7,
                        "val_next_side": 8,
                        "x_next_a": 10,
                        "x_next_b": 11,
                    },
                    "up_val": 4,
                    "down_val": 2,
                    "side_val": 3,
                    "val_up": 6,
                    "val_down": 7,
                    "val_side": 8,
                    "x_anything": 9,
                }
            },
            A_unnamed_quad_inner_quad,
        ),
        {
            "config": {
                "personal_key": {
                    "jack": 0,
                    "next_up_val": 4,
                    "next_down_val": 2,
                    "next_side_val": 3,
                    "val_next_up": 6,
                    "val_next_down": 7,
                    "val_next_side": 8,
                    "x_next_a": 10,
                    "x_next_b": 11,
                },
                "up_val": 4,
                "down_val": 2,
                "side_val": 3,
                "val_up": 6,
                "val_down": 7,
                "val_side": 8,
                "x_anything": 9,
            }
        },
    ),
    "nested_unnamed_nest_multi_b": (
        (
            {
                "config": {
                    "personal_key": {
                        "my_dict": {
                            "my_number": 3,
                            "inner_down_val": 2,
                            "inner_side_val": 3,
                            "val_inner_up": 6,
                            "val_inner_down": 7,
                            "val_inner_side": 8,
                            "x_inner_a": 10,
                            "x_inner_b": 11,
                        },
                        "next_down_val": 2,
                        "next_side_val": 3,
                        "val_next_up": 6,
                        "val_next_down": 7,
                        "val_next_side": 8,
                        "x_next_a": 10,
                        "x_next_b": 11,
                    },
                    "up_val": 4,
                    "down_val": 2,
                    "side_val": 3,
                    "val_up": 6,
                    "val_down": 7,
                    "val_side": 8,
                    "x_anything": 9,
                }
            },
            A_unnamed_quad_nested_inner_quad,
        ),
        {
            "config": {
                "personal_key": {
                    "my_dict": {
                        "my_number": 3,
                        "inner_down_val": 2,
                        "inner_side_val": 3,
                        "val_inner_up": 6,
                        "val_inner_down": 7,
                        "val_inner_side": 8,
                        "x_inner_a": 10,
                        "x_inner_b": 11,
                    },
                    "next_down_val": 2,
                    "next_side_val": 3,
                    "val_next_up": 6,
                    "val_next_down": 7,
                    "val_next_side": 8,
                    "x_next_a": 10,
                    "x_next_b": 11,
                },
                "up_val": 4,
                "down_val": 2,
                "side_val": 3,
                "val_up": 6,
                "val_down": 7,
                "val_side": 8,
                "x_anything": 9,
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
