from crummycm.types.base import Base


class Placeholder:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Placeholder) and self.name == other.name

    def __hash__(self):
        # allows to be used as key
        return hash(self.name + f"{__class__}")

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class ValuePlaceholder(Placeholder):
    def __init__(self, name):
        if not name:
            raise ValueError("no name was provided for ValuePlaceholder")
        elif not isinstance(name, str):
            raise ValueError(f"name {name} should be type {str}, not {type(name)}")
        super().__init__(name)


class KeyPlaceholder(Placeholder):
    def __init__(self, name, starts_with=None, ends_with=None, multi=False):
        if not name:
            raise ValueError("no name was provided for KeyPlaceholder")
        elif not isinstance(name, str):
            raise ValueError(f"name {name} should be type {str}, not {type(name)}")
        super().__init__(name)
        assert starts_with is None or ends_with is None, ValueError(
            f"Cannot specify both starts_with=({starts_with}) and ends_with=({ends_with})"
        )
        self.starts_with = starts_with or None
        self.ends_with = ends_with or None
        self.multi = multi


def is_KeyPlaceholder(cur_obj):
    try:
        return issubclass(cur_obj, KeyPlaceholder)
    except TypeError:
        return isinstance(cur_obj, KeyPlaceholder)


class BaseDict:
    def __init__(self, in_dict):
        assert isinstance(in_dict, dict), TypeError(
            f"in_dict ({type(in_dict)}) of {self.__class__} is expected to be a {dict}, not {type(in_dict)}"
        )

        # use sets to prevent overwrite
        str_key = set()
        sw_val = set()
        ew_val = set()

        for k, v in in_dict.items():
            # TODO: are there any instances in which the k would be hashable but
            # not a string? an int maybe?
            if isinstance(k, str):
                if k not in str_key:
                    str_key.add(k)
                else:
                    raise ValueError(f"k {k} already exists in {in_dict.keys()}")
            elif isinstance(k, Placeholder):
                print(k)
                print(k.starts_with)
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
                else:
                    str_key.add("UNAMED_KEY")
            else:
                raise TypeError(
                    f"key {k} is expected to be type {str} or {KeyPlaceholder}, not {type(k)}"
                )

            assert (
                isinstance(v, Base)
                or isinstance(v, BaseDict)
                or isinstance(v, ValuePlaceholder)
            ), TypeError(
                f"value {v} is expected to be subclass of {Base} or subclass of {BaseDict}, not {type(v)}"
            )

        assert len(str_key) + len(sw_val) + len(ew_val) == len(
            in_dict.keys()
        ), ValueError(
            f"keys provided aren't unique:\n"
            f"keys defined by string: {str_key}\n"
            f"starts_with descriptors: {sw_val}\n"
            f"ends_with descriptors: {ew_val}\n"
            f"in_dict keys: {in_dict.keys()}"
        )

        self.in_dict = in_dict or None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
