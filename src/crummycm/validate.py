from typing import Any
from crummycm.types.base import Base

# from crummycm.types.component.known_dict import KnownDict
from crummycm.types.component.base_dict import BaseDict

# def has_method(o, name):
#     # https://stackoverflow.com/questions/7580532/how-to-check-whether-a-method-exists-in-python
#     return callable(getattr(o, name, None))


def _obtain_init_value(k, raw, spec):
    # obtain value
    if spec.required:
        cur_raw_v = raw[k]
    else:
        try:
            cur_raw_v = raw[k]
        except ValueError:
            try:
                cur_raw_v = spec.default_value
            except AttributeError:
                raise ValueError(
                    f"no value is specified for {k} no default is specified"
                )
        except KeyError:
            try:
                cur_raw_v = spec.default_value
            except AttributeError:
                raise ValueError(
                    f"no value is specified for {k} and no default is specified"
                )
    return cur_raw_v


def _parse_dict(raw, spec):
    tmp_dict = {}
    for k, v in spec.in_dict.items():
        if isinstance(v, Base):
            cur_val = _transform_from_spec(k, raw, v)
        elif isinstance(v, BaseDict):
            cur_val = validate(raw[k], v.in_dict)
        else:
            raise TypeError(f"type of {v} ({type(v)}) is invalid")
        tmp_dict[k] = cur_val
    return tmp_dict


def _transform_from_spec(k, raw, spec):
    cur_val = _obtain_init_value(k, raw, spec)
    try:
        rv = spec.transform(cur_val)
    except AttributeError:
        rv = cur_val
    return rv


def validate(raw: Any, template: Any):
    # assert raw.keys() == template.keys(), f"not equal"  # check unused keys
    formatted = {}
    if isinstance(template, dict):
        for k, spec in template.items():
            if isinstance(spec, BaseDict):
                formatted[k] = _parse_dict(raw[k], spec)
            elif isinstance(spec, Base):
                formatted[k] = _transform_from_spec(k, raw, spec)
            else:
                raise TypeError(f"type of {spec} ({type(spec)}) is invalid")

    return formatted
