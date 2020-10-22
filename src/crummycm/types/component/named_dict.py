from crummycm.types.base import Base
from crummycm.types.component.base_dict import BaseDict, ValuePlaceholder


class NamedDict(BaseDict):
    # keys are known, values are unknown
    def __init__(self, in_dict):
        super().__init__(in_dict)
        for k, v in self.in_dict.items():
            # key must be a string
            assert isinstance(k, str), TypeError(
                f"key {k} is expected to be type str, not {type(k)}"
            )

            # value must not be a placeholder
            assert issubclass(v, ValuePlaceholder), TypeError(
                f"For an {self.__class__}, the value {v} is expected to be type {ValuePlaceholder}, not {type(ValuePlaceholder)}"
            )