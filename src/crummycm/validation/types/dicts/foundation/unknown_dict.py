from crummycm.validation.types.dicts.base_dict import (
    BaseDict,
    KeyPlaceholder,
    ValuePlaceholder,
)


class UnknownDict(BaseDict):
    # neither keys nor values are known
    def __init__(self, in_dict):
        super().__init__(in_dict)
        for k, v in self.in_dict.items():
            assert isinstance(k, KeyPlaceholder), TypeError(
                f"For an {self.__class__}, the key {k} is expected to be type {KeyPlaceholder}, not {type(k)}"
            )

            # value must be a placeholder
            assert isinstance(v, ValuePlaceholder), TypeError(
                f"For an {self.__class__}, the value {v} is expected to be type {ValuePlaceholder}, not {type(ValuePlaceholder)}"
            )
