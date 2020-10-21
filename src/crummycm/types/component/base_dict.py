from crummycm.types.base import Base


class ValuePlaceholder:
    def __init__(self):
        pass


class KeyPlaceholder:
    def __init__(self):
        pass

    def __hash__(self):
        # allows to be used as key
        return 0


class BaseDict:
    def __init__(self, in_dict):
        assert isinstance(in_dict, dict), TypeError(
            f"in_dict ({type(in_dict)}) of {self.__class__} is expected to be a {dict}, not {type(in_dict)}"
        )
        for k, v in in_dict.items():
            assert isinstance(k, str) or issubclass(k, KeyPlaceholder), TypeError(
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