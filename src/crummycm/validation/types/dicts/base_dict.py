import crummycm as ccm
from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    Placeholder,
    ValuePlaceholder,
)
from crummycm.validation.types.values.base import BaseValue
from crummycm.validation.types.values.compound.multi import Multi
from crummycm.validation.types.values.element.bool import Bool
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text


"""
# NOTE: I could use some help with imports
# from crummycm.validation.types.dicts.config_dict import ConfigDict as CD
# from .config_dict import ConfigDict
^above do not work, and so instead I do
`import crummycm as ccm`
then use:
`ccm.validation.types.dicts.config_dict.ConfigDict(v)`
this may be related to circular imports, but I'm unsure at this point
+ https://stackoverflow.com/questions/22187279/python-circular-importing

"""


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

            if (
                isinstance(v, BaseValue)
                or isinstance(v, BaseDict)
                or isinstance(v, ValuePlaceholder)
                # This is rough
                or isinstance(v, Text)
                or isinstance(v, Multi)
                or isinstance(v, Numeric)
                or isinstance(v, Bool)
                # I think this is still a result of poor import management on my part
                or isinstance(v, ccm.validation.types.dicts.config_dict.ConfigDict)
            ):
                pass
            elif isinstance(v, dict):
                v = ccm.validation.types.dicts.config_dict.ConfigDict(v)
                in_dict[k] = v
            else:
                raise TypeError(
                    f"value {v} is expected to be a dict or a subclass of {BaseValue} or subclass of {BaseDict}, not {type(v)}"
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

    def __repr__(self):
        return str(self.__class__.__name__) + ": " + f"{self.in_dict}"
