import pytest

from crummycm.templating.templating import template
from example_files.a import flat_a, nested_a

ex_config = {
    "flat_a": (
        (flat_a, "tests/unit/template/basic/example_files/out_yml/flat_a.yml"),
        {
            "my_mixed": {
                "kd_num": "[Numeric]",
                "[KeyPlaceholder]": "[ValuePlaceholder]",
                "wild_card": "[ValuePlaceholder]",
            }
        },
    ),
    "nested_a": (
        (nested_a, "tests/unit/template/basic/example_files/out_yml/nested_a.yml"),
        {
            "my_mixed": {
                "kd_num": "[Numeric]",
                "[KeyPlaceholder]": "[ValuePlaceholder]",
                "wild_card": "[ValuePlaceholder]",
                "nested_md": {
                    "kd_num": "[Numeric]",
                    "[KeyPlaceholder]": "[ValuePlaceholder]",
                    "wild_card": "[ValuePlaceholder]",
                },
            }
        },
    ),
}


def call(temp):
    raw_dict = template(temp[0], temp[1])
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

