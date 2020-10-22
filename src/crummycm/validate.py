from typing import Any

from crummycm.types.base import Base
from crummycm.types.component.base_dict import BaseDict, KeyPlaceholder
from crummycm.types.component.known_dict import KnownDict
from crummycm.types.component.named_dict import NamedDict
from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.types.component.unknown_dict import UnknownDict

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


def _parse_known_dict(raw, spec):
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


def _parse_named_dict(raw, spec):
    # blindly accept user value and place in spec
    temp_dict = {}
    for k, v in spec.in_dict.items():
        try:
            cur_val = raw[k]
        except KeyError:
            raise ValueError(
                f"key {k} is expected in {spec}, but is not in {raw.keys()}"
            )
        temp_dict[k] = cur_val

    return temp_dict


def _parse_unnamed_dict(raw, spec):
    if not raw:
        raise ValueError(f"no user entry found for {spec}")

    # will accept the users keys
    tmp_dict = {}
    v = spec.in_dict[KeyPlaceholder]
    for uk, uv in raw.items():
        if isinstance(v, Base):
            cur_val = _transform_from_spec(uk, raw, v)
        elif isinstance(v, BaseDict):
            cur_val = validate(raw[uk], v.in_dict)
        else:
            raise TypeError(f"type of {v} ({type(v)}) is invalid")
        tmp_dict[uk] = cur_val
    return tmp_dict


def _parse_dict(raw, spec):
    tmp_dict = {}
    if isinstance(spec, KnownDict):
        tmp_dict = _parse_known_dict(raw, spec)
    elif isinstance(spec, NamedDict):
        tmp_dict = _parse_named_dict(raw, spec)
    elif isinstance(spec, UnnamedDict):
        tmp_dict = _parse_unnamed_dict(raw, spec)
    elif isinstance(spec, UnknownDict):
        tmp_dict = raw
    else:
        raise TypeError(f"{spec} ({type(spec)}) is not an accepted type")

    return tmp_dict


def _transform_from_spec(k, raw, spec):
    cur_val = _obtain_init_value(k, raw, spec)
    try:
        rv = spec.transform(cur_val)
    except AttributeError:
        rv = cur_val
    return rv


def _val_spec_against_user(k, raw, spec):
    tmp = None
    if isinstance(spec, BaseDict):
        tmp = _parse_dict(raw[k], spec)
    elif isinstance(spec, Base):
        tmp = _transform_from_spec(k, raw, spec)
    else:
        raise TypeError(f"type of {spec} ({type(spec)}) is invalid")
    return tmp


def _parse_py_dict(raw, template):
    formatted = {}
    for k, spec in template.items():
        if not isinstance(k, str):
            if issubclass(k, KeyPlaceholder):
                formatted = _parse_unnamed_dict(raw, UnnamedDict(template))
        else:
            formatted[k] = _val_spec_against_user(k, raw, spec)
    return formatted


def validate(raw: Any, template: Any):
    # check unused keys
    formatted = {}
    if isinstance(template, dict):
        formatted = _parse_py_dict(raw, template)
    elif isinstance(template, BaseDict):
        formatted = _parse_dict(raw, template)
    else:
        raise ValueError(
            f"{template} is of type {type(template)} not {dict} or {BaseDict}"
        )

    return formatted
