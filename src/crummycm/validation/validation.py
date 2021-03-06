from typing import Any

from crummycm.validation.assign import map_user_keys_to_spec_key, populate_dict
from crummycm.validation.types.dicts.base_dict import BaseDict, Placeholder
from crummycm.validation.types.dicts.config_dict import ConfigDict
from crummycm.validation.types.dicts.foundation.known_dict import KnownDict
from crummycm.validation.types.dicts.foundation.named_dict import NamedDict
from crummycm.validation.types.dicts.foundation.unknown_dict import UnknownDict
from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)
from crummycm.validation.types.values.base import BaseValue

"""

NOTE: i really don't like the passing of `disallow_unused` everywhere

"""

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


def _parse_known_dict(raw, spec, disallow_unused):
    tmp_dict = {}
    for k, v in spec.in_dict.items():
        if isinstance(v, BaseValue):
            cur_val = _transform_from_spec(k, raw, v)
        elif isinstance(v, BaseDict):
            cur_val = validate(raw[k], v.in_dict, disallow_unused)
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


def _set_all_to_none(cur_d):
    tmp_ud = {}
    for k, v in cur_d.items():
        # key
        if isinstance(k, str):
            tmp_uk = k
        elif isinstance(k, KeyPlaceholder):
            if k.exact:
                tmp_uk = k.name
            else:
                raise ValueError(
                    f"cannot propagate `populate` through {k}, KeyPlaceholder must be `exact=True`"
                )
        else:
            raise ValueError(
                f"cannot propagate `populate` to {k}, key must be {str}"
                f" or a KeyPlaceholder with `exact=True`"
            )

        # value
        if isinstance(v, BaseValue):
            ret_v = None
        elif isinstance(v, ValuePlaceholder):
            ret_v = None
        elif isinstance(v, BaseDict):
            ret_v = _set_all_to_none(v.in_dict)
        else:
            raise ValueError(
                f"cannot propagate `populate` to {v}, value must be {BaseValue}"
                f" or {BaseDict} or {ValuePlaceholder} with `exact=True`"
            )
        tmp_ud[tmp_uk] = ret_v

    return tmp_ud


def _parse_unnamed_dict(raw, spec, disallow_unused):

    # TODO: keep track of used names
    uk_to_sk = map_user_keys_to_spec_key(raw, spec.in_dict)

    # will accept the users keys
    tmp_dict = {}
    for uk, uv in raw.items():
        sk = uk_to_sk[uk]
        sv = spec.in_dict[sk]
        if isinstance(sv, BaseValue):
            cur_val = _transform_from_spec(uk, raw, sv)
        elif isinstance(sv, BaseDict):
            cur_val = validate(raw[uk], sv.in_dict, disallow_unused)
        else:
            raise TypeError(f"type of {sv} ({type(sv)}) is invalid")
        tmp_dict[uk] = cur_val

    # TODO: add populate keys if unused
    pop_dict = populate_dict(spec.in_dict)
    for pk, pv in pop_dict.items():
        cur_k = pk.name
        if cur_k not in tmp_dict.keys():
            if isinstance(pv, BaseValue):
                ret_v = pv.default_value
                tmp_dict[cur_k] = ret_v
            elif isinstance(pv, BaseDict):
                tmp_ud = _set_all_to_none(pv.in_dict)
                ret_v = validate(tmp_ud, pv.in_dict, disallow_unused)
                tmp_dict[cur_k] = ret_v

    return tmp_dict


def _parse_unknown_dict(raw, spec):
    tmp_dict = {}
    # the output is unused, but the function is still run to ensure inner checks
    # NOTE: need to ensure this is still required/valid
    _ = map_user_keys_to_spec_key(raw, spec.in_dict)
    tmp_dict = raw.copy()

    # TODO: add populate keys if unused
    pop_dict = populate_dict(spec.in_dict)
    for pk, pv in pop_dict.items():
        cur_k = pk.name
        if cur_k not in tmp_dict.keys():
            if isinstance(pv, ValuePlaceholder):
                ret_v = pv.default_value
                tmp_dict[cur_k] = ret_v
            else:
                raise ValueError(f"value of {pk} is {pv} not a {ValuePlaceholder}")

    return tmp_dict


class Wrapper(str):
    # https://stackoverflow.com/questions/33158501/python-keyerror-and-valueerror-inconsistency
    def __repr__(self):
        return str(self)


def _parse_comp_dict(raw, spec, disallow_unused):
    if isinstance(spec, BaseDict):
        spec_keys = list(spec.in_dict.keys())
    else:
        spec_keys = list(spec.keys())
    if raw:
        raw_keys = list(raw.keys())
    else:
        raw_keys = []
    err_str = f"current keys\n" f"> spec:({spec_keys})\n" f"> user:({raw_keys})"
    if raw is None:
        # NOTE: I'm not convinced this is how I want to handle a situation in
        # which there is no user values to parse
        raise ValueError(f"no user value for {spec}")
    tmp_dict = {}
    try:
        if isinstance(spec, KnownDict):
            tmp_dict = _parse_known_dict(raw, spec, disallow_unused)
        elif isinstance(spec, NamedDict):
            tmp_dict = _parse_named_dict(raw, spec)
        elif isinstance(spec, UnnamedDict):
            tmp_dict = _parse_unnamed_dict(raw, spec, disallow_unused)
        elif isinstance(spec, ConfigDict):
            tmp_dict = _parse_py_dicts_and_merge(raw, spec.in_dict, disallow_unused)
        elif isinstance(spec, UnknownDict):
            tmp_dict = _parse_unknown_dict(raw, spec)
        else:
            raise TypeError(f"{spec} ({type(spec)}) is not an accepted type")
    except KeyError as err:
        err_out = f"{err}\n" + err_str
        raise KeyError(Wrapper(err_out))
    except ValueError as err:
        err_out = f"{err}\n" + err_str
        raise ValueError(err_out)
    except TypeError as err:
        err_out = f"{err}\n" + err_str
        raise TypeError(err_out)

    return tmp_dict


def _transform_from_spec(k, raw, spec):
    cur_val = _obtain_init_value(k, raw, spec)
    try:
        rv = spec.transform(cur_val)
    except AttributeError:
        rv = cur_val
    return rv


def _split_dicts(raw, template):
    known, unknown = {}, {}
    named, unnamed = {}, {}

    # split template
    for k, v in template.items():
        if isinstance(k, Placeholder):
            if isinstance(v, Placeholder):
                unknown[k] = v
            else:
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
def _remove_subset_from_raw(subset, raw):
    for k in subset.keys():
        try:
            del raw[k]
        except KeyError:
            pass


def _inner(cur_t, raw, disallow_unused):
    if isinstance(cur_t, BaseDict):
        o = _parse_comp_dict(raw, cur_t, disallow_unused)
        _remove_subset_from_raw(o, raw)
    else:
        o = {}
    return o


def _determine_if_all_strict(cur_t):
    if isinstance(cur_t, BaseDict):
        bl = []
        for k in cur_t.in_dict.keys():
            # TODO: this would be nicer if the K had a method to check if it was
            # strcit or not (or even the dict)
            if k.starts_with or k.ends_with or k.exact:
                bl.append(True)
            else:
                bl.append(False)
        return all(bl)
    else:
        return False


def _create_subset(cur_t, raw):
    subset_raw = {}
    # if raw: # TODO: unsure if I want this...
    if raw is None:
        # NOTE: I'm not convinced this is how I want to handle a situation in
        # which there is no user values to parse
        raise ValueError(f"no user value for {cur_t}")
    for uk in raw.keys():
        if isinstance(cur_t, BaseDict):
            for sk in cur_t.in_dict.keys():
                if sk.matches(uk):
                    subset_raw[uk] = raw[uk]
    return subset_raw


def _parse_py_dicts_and_merge(raw, template, disallow_unused):
    formatted = {}
    # split dicts
    known_t, named_t, unnamed_t, unknown_t = _split_dicts(raw, template)

    # parse seperately
    # the order is important --known keys, to unknown keys
    # strict to less strict

    ok = _inner(known_t, raw, disallow_unused)
    on = _inner(named_t, raw, disallow_unused)
    un_strict = _determine_if_all_strict(unnamed_t)
    uk_strict = _determine_if_all_strict(unknown_t)
    # subset raw to only values that match the strict
    if un_strict:
        subset_raw = _create_subset(unnamed_t, raw)
        oun = _inner(unnamed_t, subset_raw, disallow_unused)
        _remove_subset_from_raw(oun, raw)
        ouk = _inner(unknown_t, raw, disallow_unused)
    else:
        if uk_strict:
            subset_raw = _create_subset(unknown_t, raw)
            ouk = _inner(unknown_t, subset_raw, disallow_unused)
            _remove_subset_from_raw(ouk, raw)
            oun = _inner(unnamed_t, raw, disallow_unused)
        else:
            oun = _inner(unnamed_t, raw, disallow_unused)
            ouk = _inner(unknown_t, raw, disallow_unused)

    # merge
    formatted = {**ok, **on, **oun, **ouk}

    return formatted


def validate(raw: Any, template: Any, disallow_unused: bool = True):
    # TODO: dict appear to be deleted here

    if raw:
        user_keys = set(raw.keys()).copy()
    else:
        user_keys = set({})

    # check unused keys
    formatted = {}
    if isinstance(template, dict):
        formatted = _parse_py_dicts_and_merge(raw, template, disallow_unused)
    elif isinstance(template, BaseDict):
        formatted = _parse_comp_dict(raw, template, disallow_unused)
    else:
        raise ValueError(
            f"{template} is of type {type(template)} not {dict} or {BaseDict}"
        )

    if disallow_unused:
        try:
            fmt_keys = set(formatted.keys())
        except AttributeError:
            fmt_keys = set(formatted.in_dict.keys())

        unused = user_keys - fmt_keys
        if unused:
            raise ValueError(
                f"Unused keys detected from user input:\n"
                f"unused: {unused}\n"
                f"user keys: {user_keys}\n"
                f"formatted keys: {fmt_keys}\n"
            )

    return formatted
