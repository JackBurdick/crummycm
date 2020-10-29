import pytest

from crummycm.read.read import parse
from example_files.simple.a import A_EX_DICT

ex_config = {
    "yml_simple_a": (
        "./tests/unit/parse/example_files/config_path/main.yml",
        {
            "name": "Diesel",
            "location": {"state": "WA", "country": "USA"},
            "info": {"age": 3, "teeth": {"front": 5, "back": 9}},
        },
    )
}


def call(config):
    # wrapping the intput in a tuple such that I can ** the internal dict to
    # expand the commands..this isn't great, but it works.
    if isinstance(config, tuple):
        raw_dict = parse(**config[0])
    else:
        raw_dict = parse(config)
    return raw_dict


@pytest.mark.parametrize(
    "config,expected", ex_config.values(), ids=list(ex_config.keys())
)
def test_basic_parse(config, expected):
    """test whether the user input can be parsed to a dict"""
    if isinstance(expected, dict):
        raw_dict = call(config)
        print(raw_dict)
        assert expected == raw_dict
    elif issubclass(expected, ValueError):
        with pytest.raises(ValueError):
            raw_dict = call(config)
    elif issubclass(expected, FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            raw_dict = call(config)
    else:
        raise ValueError(f"expected {expected} not accounted for")
