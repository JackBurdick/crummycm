from crummycm.types.component.base_dict import (
    BaseDict,
    KeyPlaceholder,
    ValuePlaceholder,
)


class UnknownDict(BaseDict):
    def __init__(self, in_dict):
        super().__init__(in_dict)
        for k, v in self.in_dict.items():
            assert issubclass(k, KeyPlaceholder), TypeError(
                f"For an {self.__class__}, the key {k} is expected to be type {KeyPlaceholder}, not {type(k)}"
            )

            # value must not be a placeholder
            assert issubclass(v, ValuePlaceholder), TypeError(
                f"For an {self.__class__}, the value {v} is expected to be type {ValuePlaceholder}, not {type(ValuePlaceholder)}"
            )