import pytest

from crummycm.parse import parse
from example_files.simple.a import A_EX_DICT

ex_config = {
    "yml_simple_a": (
        "./tests/unit/parse/example_files/simple/a.yml",
        {
            "name": "Diesel",
            "location": {"state": "WA", "country": "USA"},
            "info": {"age": 3, "teeth": {"front": 5, "back": 9}},
        },
    ),
    "json_simple_a": (
        "./tests/unit/parse/example_files/simple/a.json",
        {
            "name": "Diesel",
            "location": {"state": "WA", "country": "USA"},
            "info": {"age": 3, "teeth": {"front": 5, "back": 9}},
        },
    ),
    "proto_simple_a": (
        "./tests/unit/parse/example_files/simple/a.proto",
        {
            "name": "Diesel",
            "location": {"state": "WA", "country": "USA"},
            "info": {"age": 3, "teeth": {"front": 5, "back": 9}},
        },
    ),
    "xml_simple_a": (
        (
            {
                "user_in": "./tests/unit/parse/example_files/simple/a.xml",
                "unsafe": True,
            },
        ),
        {
            "name": "Diesel",
            "location": {"state": "WA", "country": "USA"},
            "info": {"age": "3", "teeth": {"front": "5", "back": "9"}},
        },
    ),
    "dict_simple_a": (
        A_EX_DICT,
        {
            "name": "Diesel",
            "location": {"state": "WA", "country": "USA"},
            "info": {"age": 3, "teeth": {"front": 5, "back": 9}},
        },
    ),
    "not_a_formatted_str": ("fake_str", ValueError),
    "yml_file_doesnt_exist": ("./fake_file.yml", FileNotFoundError),
    "json_file_doesnt_exist": ("./fake_file.json", FileNotFoundError),
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
        assert expected == raw_dict
    elif issubclass(expected, ValueError):
        with pytest.raises(ValueError):
            raw_dict = call(config)
    elif issubclass(expected, FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            raw_dict = call(config)
    else:
        raise ValueError(f"expected {expected} not accounted for")
