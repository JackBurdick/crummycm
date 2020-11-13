from typing import Type
import pytest

from crummycm.validation.validation import validate
from example_templates.element.either.a import Num_or_Text

ex_config = {
    "Num_or_Text_number_provided": (({"my_either": 3}, Num_or_Text), {"my_either": 3}),
    "Num_or_Text_text_provided": (
        ({"my_either": "cat"}, Num_or_Text),
        {"my_either": "cat"},
    ),
    "Num_or_Text_None": (({"my_either": None}, Num_or_Text), ValueError),
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
