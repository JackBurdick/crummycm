from typing import Type
import pytest

from crummycm.validation.validation import validate
from example_templates.element.either.a import (
    Num_or_Text_list,
    Num_or_Text_tuple,
    return_list,
    text_or_list,
    list_or_text,
    list_or_text_return_list,
    list_or_text_return_tuple,
    l_or_t_default_list,
)

ex_config = {
    "Num_or_Text_number_provided": (
        ({"my_either": 3}, Num_or_Text_list),
        {"my_either": 3},
    ),
    "Num_or_Text_text_provided": (
        ({"my_either": "cat"}, Num_or_Text_list),
        {"my_either": "cat"},
    ),
    "Num_or_Text_None": (({"my_either": None}, Num_or_Text_list), ValueError),
    "Num_or_Text_number_provided_tup": (
        ({"my_either": 3}, Num_or_Text_tuple),
        {"my_either": 3},
    ),
    "Num_or_Text_text_provided_tup": (
        ({"my_either": "cat"}, Num_or_Text_tuple),
        {"my_either": "cat"},
    ),
    "Num_or_Text_None_tup": (({"my_either": None}, Num_or_Text_tuple), ValueError),
    "Return_list_num": (({"my_either": 3}, return_list), {"my_either": [3]}),
    "Return_list_text": (({"my_either": "3"}, return_list), {"my_either": ["3"]}),
    "text_or_list_text": (({"my_either": "cat"}, text_or_list), {"my_either": "cat"}),
    "list_or_text_text": (({"my_either": "cat"}, list_or_text), {"my_either": "cat"}),
    "list_or_text_list": (
        ({"my_either": ["cat"]}, list_or_text),
        {"my_either": ["cat"]},
    ),
    "list_or_text_return_list_text": (
        ({"my_either": "cat"}, list_or_text_return_list),
        {"my_either": ["cat"]},
    ),
    "list_or_text_return_list_list": (
        ({"my_either": ["cat"]}, list_or_text_return_list),
        {"my_either": ["cat"]},
    ),
    "list_or_text_return_tuple_text": (
        ({"my_either": "cat"}, list_or_text_return_tuple),
        {"my_either": ("cat",)},
    ),
    "list_or_text_return_tuple_list": (
        ({"my_either": ["cat"]}, list_or_text_return_tuple),
        {"my_either": ("cat",)},
    ),
    "l_or_t_default_list_provided": (
        ({"my_either": ["cat"]}, l_or_t_default_list),
        {"my_either": ["cat"]},
    ),
    "l_or_t_default_list_fallback": (
        ({"my_either": None}, l_or_t_default_list),
        {"my_either": ["a", "b"]},
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
