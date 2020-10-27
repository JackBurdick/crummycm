from crummycm.validation.types.dicts.base_dict import ValuePlaceholder

# from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.dicts.foundation.named_dict import NamedDict

# from crummycm.validation.types.values.element.numeric import Numeric
# from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.base import BaseValue
A_named_single = {"known_dict": NamedDict({"some_thing": ValuePlaceholder("some_val")})}

A_named_double = {
    "known_dict": NamedDict(
        {"a": ValuePlaceholder("a_val"), "b": ValuePlaceholder("b_val")}
    )
}

A_named_outer_single = NamedDict({"some_thing": ValuePlaceholder("some_thing_val")})

A_named_outer_double = NamedDict(
    {"a": ValuePlaceholder("a_val"), "b": ValuePlaceholder("b_val")}
)

