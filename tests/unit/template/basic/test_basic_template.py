import pytest

from crummycm.templating.templating import template
from example_files.a import flat_a, nested_a

ex_config = {
    "flat_a_yml_0": (
        (flat_a, "tests/unit/template/basic/example_files/out_yml/flat_a.yml", 0),
        {
            "my_mixed": {
                "kd_num": "<class 'int'>[Numeric]*",
                "[KPH]^": "[Text](DIESEL)*",
                "[KPH]*": "[ValuePlaceholder]*",
                "wild_card": "[ValuePlaceholder]*",
            }
        },
    ),
    "nested_a_yml_0": (
        (nested_a, "tests/unit/template/basic/example_files/out_yml/nested_a.yml", 0),
        {
            "my_mixed": {
                "kd_num": "<class 'int'>[Numeric]",
                "[KPH]^*": "[Text]*",
                "[KPH]*": "[ValuePlaceholder]*",
                "wild_card": "[ValuePlaceholder]*",
                "nested_md": {
                    "kd_num": "<class 'int'>[Numeric]",
                    "[KPH]^*": "[Text]*",
                    "[KPH]*": "[ValuePlaceholder]*",
                    "wild_card": "[ValuePlaceholder]*",
                },
            }
        },
    ),
    "flat_a_yml_1": (
        (flat_a, "tests/unit/template/basic/example_files/out_yml/flat_a.yml", 1),
        {
            "my_mixed": {
                "kd_num": "<class 'int'>[Numeric]*",
                "[KPH](ends_with='_str')": "[Text](DIESEL)*",
                "[KPH]*": "[ValuePlaceholder]*",
                "wild_card": "[ValuePlaceholder]*",
            }
        },
    ),
    "nested_a_yml_1": (
        (nested_a, "tests/unit/template/basic/example_files/out_yml/nested_a.yml", 1),
        {
            "my_mixed": {
                "kd_num": "<class 'int'>[Numeric]",
                "[KPH](ends_with='_str')*": "[Text]*",
                "[KPH]*": "[ValuePlaceholder]*",
                "wild_card": "[ValuePlaceholder]*",
                "nested_md": {
                    "kd_num": "<class 'int'>[Numeric]",
                    "[KPH](ends_with='_str')*": "[Text]*",
                    "[KPH]*": "[ValuePlaceholder]*",
                    "wild_card": "[ValuePlaceholder]*",
                },
            }
        },
    ),
    "flat_a_json": (
        (flat_a, "tests/unit/template/basic/example_files/out_yml/flat_a.json", 0),
        {
            "my_mixed": {
                "kd_num": "<class 'int'>[Numeric]*",
                "[KPH]^": "[Text](DIESEL)*",
                "[KPH]*": "[ValuePlaceholder]*",
                "wild_card": "[ValuePlaceholder]*",
            }
        },
    ),
    "nested_a_json": (
        (nested_a, "tests/unit/template/basic/example_files/out_yml/nested_a.json", 0),
        {
            "my_mixed": {
                "kd_num": "<class 'int'>[Numeric]",
                "[KPH]^*": "[Text]*",
                "[KPH]*": "[ValuePlaceholder]*",
                "wild_card": "[ValuePlaceholder]*",
                "nested_md": {
                    "kd_num": "<class 'int'>[Numeric]",
                    "[KPH]^*": "[Text]*",
                    "[KPH]*": "[ValuePlaceholder]*",
                    "wild_card": "[ValuePlaceholder]*",
                },
            }
        },
    ),
    "flat_a_proto": (
        (flat_a, "tests/unit/template/basic/example_files/out_yml/flat_a.proto", 0),
        NotImplementedError,
    ),
    "nested_a_proto": (
        (nested_a, "tests/unit/template/basic/example_files/out_yml/nested_a.proto", 0),
        NotImplementedError,
    ),
    "flat_a_xml": (
        (flat_a, "tests/unit/template/basic/example_files/out_yml/flat_a.xml", 0),
        NotImplementedError,
    ),
    "nested_a_xml": (
        (nested_a, "tests/unit/template/basic/example_files/out_yml/nested_a.xml", 0),
        NotImplementedError,
    ),
}


def call(temp):
    raw_dict = template(temp[0], temp[1], temp[2])
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
    elif issubclass(expected, NotImplementedError):
        with pytest.raises(NotImplementedError):
            raw_dict = call(config)
    else:
        raise ValueError(f"expected {expected} not accounted for")

