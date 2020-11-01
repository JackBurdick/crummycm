import pytest

from crummycm.validation.validation import validate
from example_templates.element.bool.a import req_true, req_true_default

ex_config = {
    "req_true_v": (({"my_bool": True}, req_true), {"my_bool": True}),
    "req_true_i": (({"my_bool": None}, req_true), ValueError),
    "req_true_type_int_i": (({"my_bool": 3}, req_true), TypeError),
    "req_true_type_str_i": (({"my_bool": "3"}, req_true), TypeError),
    "req_true_type_zero_i": (({"my_bool": 0}, req_true), TypeError),
    "req_true_type_one_i": (({"my_bool": 1}, req_true), TypeError),
    "req_true_default_v_true": (
        ({"my_bool": True}, req_true_default),
        {"my_bool": True},
    ),
    "req_true_default_v_def": (
        ({"my_bool": None}, req_true_default),
        {"my_bool": True},
    ),
    "req_true_default_v_user": (
        ({"my_bool": False}, req_true_default),
        {"my_bool": False},
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
