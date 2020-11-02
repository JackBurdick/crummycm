import pytest

from crummycm.read.read import parse

ex_config = {
    "no_parse_path_v": (
        "./tests/unit/key_instructions/example_files/spec/no_parse.yml",
        {"data": {"schema": "./tests/unit/key_instructions/example_files/schema.json"}},
    ),
    "path_exists_v": (
        "./tests/unit/key_instructions/example_files/spec/path_exists.yml",
        {"data": {"schema": "./tests/unit/key_instructions/example_files/schema.json"}},
    ),
    "path_exists_i": (
        "./tests/unit/key_instructions/example_files/spec/path_exists_i.yml",
        ValueError,
    ),
    "parse_path_v": (
        "./tests/unit/key_instructions/example_files/spec/parse_path.yml",
        {
            "data": {
                "schema": {
                    "x_image": {"shape": [28, 28, 1], "dtype": "float32"},
                    "y_target": {"shape": [1, 1], "dtype": "int32", "label": True},
                }
            }
        },
    ),
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
    elif issubclass(expected, TypeError):
        with pytest.raises(TypeError):
            raw_dict = call(config)
    elif issubclass(expected, KeyError):
        with pytest.raises(KeyError):
            raw_dict = call(config)
    else:
        raise ValueError(f"expected {expected} not accounted for")
