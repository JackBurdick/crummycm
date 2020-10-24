from crummycm.types.component.base_dict import ValuePlaceholder

# from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.types.component.named_dict import NamedDict

# from crummycm.types.element.numeric import Numeric
# from crummycm.types.element.text import Text

# from crummycm.types.element.base import Base
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

