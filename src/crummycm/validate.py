from typing import Any

from crummycm.types.base import Base
from crummycm.types.component.base_dict import (
    BaseDict,
    KeyPlaceholder,
    ValuePlaceholder,
    Placeholder,
)
from crummycm.types.component.known_dict import KnownDict
from crummycm.types.component.named_dict import NamedDict
from crummycm.types.component.unknown_dict import UnknownDict
from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.validation.assign import map_user_keys_to_spec_key

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

    # TODO: keep track of used names
    uk_to_sk = map_user_keys_to_spec_key(raw, spec.in_dict)

    # will accept the users keys
    tmp_dict = {}
    for uk, uv in raw.items():
        sk = uk_to_sk[uk]
        sv = spec.in_dict[sk]
        if isinstance(sv, Base):
            cur_val = _transform_from_spec(uk, raw, sv)
        elif isinstance(sv, BaseDict):
            cur_val = validate(raw[uk], sv.in_dict)
        else:
            raise TypeError(f"type of {sv} ({type(sv)}) is invalid")
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
        tmp_dict = raw.copy()
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


def _val_spec_against_user(sk, raw, sv):
    tmp = None
    if isinstance(sv, BaseDict):
        tmp = _parse_dict(raw[sk], sv)
    elif isinstance(sv, Base):
        tmp = _transform_from_spec(sk, raw, sv)
    else:
        raise TypeError(f"type of {sv} ({type(sv)}) is invalid")
    return tmp


def _parse_py_dict(raw, template):
    formatted = {}
    for sk, sv in template.items():
        if not isinstance(sk, str):
            if isinstance(sk, KeyPlaceholder):
                formatted = _parse_unnamed_dict(raw, UnnamedDict(template))
        else:
            formatted[sk] = _val_spec_against_user(sk, raw, sv)
    return formatted


def _split_dicts(raw, template):
    known, unknown = {}, {}
    named, unnamed = {}, {}

    # split template
    for k, v in template.items():
        if isinstance(k, Placeholder):
            if isinstance(v, Placeholder):
                assert len(unknown) < 1, ValueError(
                    f"can only have 1 unknown item in {template}"
                )
                unknown[k] = v
            else:
                assert len(unknown) < 1, ValueError(
                    f"can only have 1 unnamed item in {template}"
                )
                unnamed[k] = v
        else:
            if isinstance(v, Placeholder):
                named[k] = v
            else:
                known[k] = v

    if known:
        known = KnownDict(known)
    if named:
        named = NamedDict(named)
    if unnamed:
        unnamed = UnnamedDict(unnamed)
    if unknown:
        unknown = UnknownDict(unknown)
    return known, named, unnamed, unknown


# obtain corresponding dicts from raw
# NOTE: this could be done in a single loop, but this is easy to
# read/reason about for the time being


def _parse_py_dicts_and_merge(raw, template):
    formatted = {}
    # split dicts
    known_t, named_t, unnamed_t, unknown_t = _split_dicts(raw, template)

    # parse seperately
    # the order is important --known keys, to unknown keys
    if isinstance(known_t, BaseDict):
        # print(f"known: {known_t.in_dict.keys()}")
        ok = _parse_dict(raw, known_t)
        for k in ok.keys():
            try:
                del raw[k]
            except KeyError:
                pass
        # print(f"ok: {ok}")
    else:
        ok = {}

    if isinstance(named_t, BaseDict):
        # print(f"named_t: {named_t.in_dict.keys()}")
        on = _parse_dict(raw, named_t)
        for k in on.keys():
            try:
                del raw[k]
            except KeyError:
                pass
        # print(f"on: {on}")
    else:
        on = {}

    if isinstance(unnamed_t, BaseDict):
        # print(f"unnamed_t: {unnamed_t.in_dict.keys()}")
        oun = _parse_dict(raw, unnamed_t)
        for k in oun.keys():
            try:
                del raw[k]
            except KeyError:
                pass
        # print(f"oun: {oun}")
    else:
        oun = {}

    if isinstance(unknown_t, BaseDict):
        # print(f"unknown_t: {unknown_t.in_dict.keys()}")
        ouk = _parse_dict(raw, unknown_t)
        for k in ouk.keys():
            try:
                del raw[k]
            except KeyError:
                pass
        # print(f"ouk: {ouk}")
    else:
        ouk = {}

    # merge
    formatted = {**ok, **on, **oun, **ouk}

    return formatted


def validate(raw: Any, template: Any):
    # check unused keys
    formatted = {}
    if isinstance(template, dict):
        # formatted = _parse_py_dict(raw, template)
        formatted = _parse_py_dicts_and_merge(raw, template)
    elif isinstance(template, BaseDict):
        formatted = _parse_dict(raw, template)
    else:
        raise ValueError(
            f"{template} is of type {type(template)} not {dict} or {BaseDict}"
        )

    return formatted
