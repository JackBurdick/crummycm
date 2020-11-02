from crummycm.validation.types.dicts.base_dict import BaseDict
from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)
from crummycm.validation.types.values.base import BaseValue
from crummycm.read.read_format.yaml import write_dict_to_yaml


def print_key(k, level):
    if isinstance(k, KeyPlaceholder):
        return k.template(level=level)
    else:
        return k


def print_value(v, level):
    if isinstance(v, ValuePlaceholder):
        return v.template(level=level)
    elif isinstance(v, BaseValue):
        return v.template(level=level)
    else:
        return v


def generate_example_template(d, level=0):
    out_d = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = generate_example_template(v, level)
        if isinstance(v, BaseDict):
            v = generate_example_template(v.in_dict, level)
        else:
            v = print_value(v, level)
        out_d[print_key(k, level)] = v
    return out_d


def template(template, write_path, level=0):
    o = generate_example_template(template, level)
    if write_path.endswith("yml"):
        write_dict_to_yaml(data=o, path=write_path)
    return o
