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
        super().__init__(name)


class KeyPlaceholder(Placeholder):
    def __init__(self, name, starts_with=None, ends_with=None):
        super().__init__(name)
        assert starts_with is None or ends_with is None, ValueError(
            f"Cannot specify both starts_with=({starts_with}) and ends_with=({ends_with})"
        )
        self.starts_with = starts_with or None
        self.ends_with = ends_with or None


def is_KeyPlaceholder(cur_obj):
    try:
        return issubclass(cur_obj, KeyPlaceholder)
    except TypeError:
        return isinstance(cur_obj, KeyPlaceholder)


def is_placeholder(cur_obj):
    try:
        return issubclass(cur_obj, Placeholder)
    except TypeError:
        return isinstance(cur_obj, Placeholder)


class BaseDict:
    def __init__(self, in_dict):
        assert isinstance(in_dict, dict), TypeError(
            f"in_dict ({type(in_dict)}) of {self.__class__} is expected to be a {dict}, not {type(in_dict)}"
        )
        for k, v in in_dict.items():
            # TODO: are there any instances in which the k would be hashable but
            # not a string? an int maybe?
            assert isinstance(k, str) or is_placeholder(k), TypeError(
                f"key {k} is expected to be type {str} or {KeyPlaceholder}, not {type(k)}"
            )
            assert (
                isinstance(v, Base)
                or isinstance(v, BaseDict)
                or issubclass(v, ValuePlaceholder)
            ), TypeError(
                f"value {v} is expected to be subclass of {Base} or subclass of {BaseDict}, not {type(v)}"
            )

        self.in_dict = in_dict or None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
