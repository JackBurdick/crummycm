# from crummycm.types.element.numeric import Numeric
# from crummycm.types.element.text import Text
# from crummycm.types.element.base import Base
from crummycm.types.component.base_dict import (
    BaseDict,
    KeyPlaceholder,
    ValuePlaceholder,
)


class UnnamedDict(BaseDict):
    # keys are unknown but values are known
    def __init__(self, in_dict):
        super().__init__(in_dict)
        for k, v in self.in_dict.items():
            assert issubclass(k, KeyPlaceholder), TypeError(
                f"key {k} is expected to be type {KeyPlaceholder}, not {type(k)}"
            )

            # value must not be a placeholder
            assert not isinstance(v, ValuePlaceholder), TypeError(
                f"value {v} in a KnownDict is not allowed to be {ValuePlaceholder}, not {type(v)}"
            )
