# from crummycm.types.element.numeric import Numeric
# from crummycm.types.element.text import Text
from crummycm.types.base import Base
from crummycm.types.component.base_dict import BaseDict, ValuePlaceholder


class KnownDict(BaseDict):
    def __init__(self, in_dict):
        super().__init__(in_dict)
        for k, v in self.in_dict.items():
            # key must be a string
            assert isinstance(k, str), TypeError(
                f"key {k} is expected to be type str, not {type(k)}"
            )

            # value must not be a placeholder
            assert not isinstance(v, ValuePlaceholder), TypeError(
                f"value {v} in a KnownDict is not allowed to be {ValuePlaceholder}, not {type(v)}"
            )
