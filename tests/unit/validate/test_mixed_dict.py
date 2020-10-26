import pytest

from crummycm.validate import validate
from example_templates.component.mixed_keys.a import A_mixed_all_single

ex_config = {
    "known_contains_unknown": (
        (
            {
                "my_mixed": {
                    "kd_num": 0,
                    "my_str": "Jack",
                    "my_num": 11,
                    "wild_card": 2.3,
                }
            },
            A_mixed_all_single,
        ),
        {"my_mixed": {"kd_num": 0, "my_str": "Jack", "my_num": 11, "wild_card": 2.3}},
    )
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

