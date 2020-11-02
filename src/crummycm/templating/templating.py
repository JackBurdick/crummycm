from crummycm.validation.types.dicts.base_dict import BaseDict
from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)
from crummycm.validation.types.values.base import BaseValue


def print_key(k):
    if isinstance(k, KeyPlaceholder):
        return f"<{k.name}>"
    else:
        return k


def print_value(v):
    if isinstance(v, ValuePlaceholder):
        return f"<{v.name}>"
    elif isinstance(v, BaseValue):
        return f"{v.__class__.__name__}()"
    else:
        return v


def print_template(d):
    for k, v in d.items():
        if isinstance(v, dict):
            print_template(v)
        if isinstance(v, BaseDict):
            print_template(v.in_dict)
        else:
            print(f"{print_key(k)} : {print_value(v)}")


def template(template):
    print("\n")
    print_template(template)
    return template
