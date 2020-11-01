from typing import Optional
from crummycm.validation.types.values.base import BaseValue
from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
    Placeholder,
)


class BaseDict:
    def __init__(self, in_dict):
        assert isinstance(in_dict, dict), TypeError(
            f"in_dict ({type(in_dict)}) of {self.__class__} is expected to be a {dict}, not {type(in_dict)}"
        )

        # use sets to prevent overwrite
        str_key = set()
        sw_val = set()
        ew_val = set()
        named_keys = set()

        for k, v in in_dict.items():
            # TODO: are there any instances in which the k would be hashable but
            # not a string? an int maybe?
            if isinstance(k, str):
                if k not in str_key:
                    str_key.add(k)
                else:
                    raise ValueError(f"k {k} already exists in {in_dict.keys()}")
            elif isinstance(k, Placeholder):
                if k.starts_with:
                    if k not in sw_val:
                        sw_val.add(k.starts_with)
                    else:
                        raise ValueError(
                            f"k ({k}) invalid, duplicate keys starts_with={k.starts_with} in {in_dict.keys()}"
                        )
                elif k.ends_with:
                    if k not in ew_val:
                        ew_val.add(k.ends_with)
                    else:
                        raise ValueError(
                            f"k ({k}) invalid, duplicate keys ends_with={k.ends_with} in {in_dict.keys()}"
                        )
                elif k.name:
                    if k not in named_keys:
                        named_keys.add(k.name)
                    else:
                        raise ValueError(
                            f"duplicate keys detected: key {k} already in {in_dict.keys()}"
                        )
                else:
                    str_key.add("UNAMED_KEY")
            else:
                raise TypeError(
                    f"key {k} is expected to be type {str} or {KeyPlaceholder}, not {type(k)}"
                )

            assert (
                isinstance(v, BaseValue)
                or isinstance(v, BaseDict)
                or isinstance(v, ValuePlaceholder)
            ), TypeError(
                f"value {v} is expected to be subclass of {BaseValue} or subclass of {BaseDict}, not {type(v)}"
            )

        assert len(str_key) + len(sw_val) + len(ew_val) + len(named_keys) == len(
            in_dict.keys()
        ), ValueError(
            f"keys provided aren't unique:\n"
            f"keys defined by string: {str_key}\n"
            f"named keys defined by name: {named_keys}\n"
            f"starts_with descriptors: {sw_val}\n"
            f"ends_with descriptors: {ew_val}\n"
            f"in_dict keys: {in_dict.keys()}"
        )

        self.in_dict = in_dict or None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
