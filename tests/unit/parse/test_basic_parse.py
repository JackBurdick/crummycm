import pytest

from crummycm.parse import parse
from example_files.simple.a import A_EX_DICT

ex_config = {
    # ----- REQUIRED
    # missing
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


@pytest.mark.parametrize(
    "config,expected", ex_config.values(), ids=list(ex_config.keys())
)
def test_basic_parse(config, expected):
    """test whether the user input can be parsed to a dict"""
    if isinstance(expected, dict):
        raw_dict = parse(config)
        assert expected == raw_dict
    elif issubclass(expected, ValueError):
        with pytest.raises(ValueError):
            raw_dict = parse(config)
    elif issubclass(expected, FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            raw_dict = parse(config)
    else:
        raise ValueError(f"expected {expected} not accounted for")
