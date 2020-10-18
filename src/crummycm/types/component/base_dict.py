from crummycm.types.base import Base


class ValuePlaceholder:
    def __init__(self):
        pass


class KeyPlaceholder:
    def __init__(self):
        pass


class BaseDict:
    def __init__(self, in_dict):
        for k, v in in_dict.items():
            assert isinstance(k, str) or isinstance(k, KeyPlaceholder), TypeError(
                f"key {k} is expected to be type str, not {type(k)}"
            )
            assert isinstance(v, Base) or isinstance(v, BaseDict), TypeError(
                f"key {v} is expected to be subclass of {Base} or subclass of {BaseDict}, not {type(v)}"
            )

        self.in_dict = in_dict or None