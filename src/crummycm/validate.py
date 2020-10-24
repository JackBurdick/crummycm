from typing import Any

from crummycm.types.base import Base
from crummycm.types.component.base_dict import (
    BaseDict,
    KeyPlaceholder,
    ValuePlaceholder,
)
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


def _get_corresponding_template_keys(spec_in_dict, uk):
    matching_keys = []
    for k in list(spec_in_dict.keys()):
        if getattr(k, "starts_with", False):
            if uk.startswith(k.starts_with):
                if uk not in matching_keys:
                    matching_keys.append(k)
                else:
                    raise ValueError(
                        f"key {uk} matches {k.name} 's attribute starts_with ({k.starts_with})"
                        f" but {matching_keys} also match a template spec and only one can be valid"
                    )
        if getattr(k, "ends_with", False):
            if uk.endswith(k.ends_with):
                if uk not in matching_keys:
                    matching_keys.append(k)
                else:
                    raise ValueError(
                        f"key {uk} matches {k.name} 's attribute ends_with ({k.ends_with}),"
                        f" but {matching_keys} also match a template spec and only one can be valid"
                    )
        if not getattr(k, "ends_with", False) and not getattr(k, "starts_with", False):
            matching_keys.append(k)

    if len(matching_keys) == 0:
        raise ValueError(
            f"no user keys found to match the specified keys in {spec_in_dict}"
        )
    # elif len(matching_keys) > 1:
    #     raise ValueError(
    #         f"user keys: {matching_keys} match multiple spec keys {spec_in_dict}"
    #     )

    return matching_keys


def _map_user_keys_to_spec_key(raw, spec_in_dict):
    uk_to_sk = {}
    options_dict = {}
    # get all keys
    for uk in raw.keys():
        options_dict[uk] = _get_corresponding_template_keys(spec_in_dict, uk)

    # eliminate singles
    used_keys = set()
    tmp_dict = {}
    for kk, vv in options_dict.items():
        if len(vv) == 1:
            cur_v = vv[0]
            if cur_v in used_keys:
                raise ValueError(f"key {vv} matches multiple items")
            else:
                used_keys.add(cur_v)
                uk_to_sk[kk] = cur_v
        else:
            tmp_dict[kk] = vv

    # TODO: eliminate remaining

    assert len(tmp_dict) == 0, ValueError(f"keys remain unassigned: {tmp_dict}")

    return uk_to_sk


def _parse_unnamed_dict(raw, spec):
    if not raw:
        raise ValueError(f"no user entry found for {spec}")

    # TODO: keep track of used names
    uk_to_sk = _map_user_keys_to_spec_key(raw, spec.in_dict)

    # will accept the users keys
    tmp_dict = {}
    for uk, uv in raw.items():
        k = uk_to_sk[uk]
        v = spec.in_dict[k]
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
            if isinstance(k, KeyPlaceholder):
                formatted = _parse_unnamed_dict(raw, UnnamedDict(template))
        else:
            formatted[k] = _val_spec_against_user(k, raw, spec)
    return formatted


# def _split_dicts(raw, template):
#     known, unknown = {}, {}
#     named, unnamed = {}, {}

#     # split template
#     for k, v in template:
#         if is_placeholder(k):
#             if is_placeholder(v):
#                 assert len(unknown) < 1, ValueError(
#                     f"can only have 1 unknown item in {template}"
#                 )
#                 unknown[k] = v
#             else:
#                 assert len(unknown) < 1, ValueError(
#                     f"can only have 1 unnamed item in {template}"
#                 )
#                 unnamed[k] = v
#         else:
#             if is_placeholder(v):
#                 named[k] = v
#             else:
#                 known[k] = v

#     r_known, r_unknown = {}, {}
#     r_named, r_unnamed = {}, {}
#     for k in list(known.keys()):
#         r_known[k] = raw.get(k, None)
#     for k in list(r_named.keys()):
#         r_known[k] = raw.get(k, None)

# obtain corresponding dicts from raw
# NOTE: this could be done in a single loop, but this is easy to
# read/reason about for the time being


# def _parse_py_dict_v2(raw, template):
#     # split dicts
#     for k,v in spec:
#         if not isinstance(k, str):
#             if issubclass(k, KeyPlaceholder):


#     # parse seperately

#     # merge
#     formatted = {}
#     for k, spec in template.items():
#         if not isinstance(k, str):
#             if issubclass(k, KeyPlaceholder):
#                 formatted = _parse_unnamed_dict(raw, UnnamedDict(template))
#         else:
#             formatted[k] = _val_spec_against_user(k, raw, spec)
#     return formatted


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
