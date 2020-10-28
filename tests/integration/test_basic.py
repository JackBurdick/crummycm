import pytest

import crummycm as ccm
from example_files.basic_yaml.template import TEMPLATE

ex_config = {
    "yml_simple_a": (
        ("./tests/integration/example_files/basic_yaml/mnist.yml", TEMPLATE),
        {
            "data": {
                "name": "mnist",
                "schema": {
                    "x_image": {"shape": [28, 28, 1], "dtype": "float32"},
                    "y_target": {"shape": [1, 1], "dtype": "int32"},
                },
                "source": "http://yann.lecun.com/exdb/mnist/",
            }
        },
    )
}


def call(example):
    # wrapping the intput in a tuple such that I can ** the internal dict to
    # expand the commands..this isn't great, but it works.
    if isinstance(example, tuple):
        raw_dict = ccm.generate(*example)
    elif isinstance(example, dict):
        raw_dict = ccm.generate(**example)
    else:
        raw_dict = ccm.generate(example)
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
