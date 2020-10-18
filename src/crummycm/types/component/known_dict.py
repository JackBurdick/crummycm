# from crummycm.types.element.numeric import Numeric
# from crummycm.types.element.text import Text
from crummycm.types.component.base_dict import BaseDict


class KnownDict(BaseDict):
    def __init__(self, in_dict):
        super().__init__(in_dict)
        for k, v in in_dict.items():
            assert isinstance(k, str), TypeError(
                f"key {k} is expected to be type str, not {type(k)}"
            )

    # defs:
