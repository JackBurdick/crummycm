from crummycm.types.dicts.base_dict import KeyPlaceholder, ValuePlaceholder
from crummycm.types.dicts.unknown_dict import UnknownDict
from crummycm.types.values.numeric import Numeric
from crummycm.types.values.text import Text

# from crummycm.types.values.base import Base

A_inner_unknown = {
    "some_config": UnknownDict(
        {KeyPlaceholder("something"): ValuePlaceholder("someval")}
    )
}

A_outer_unknown = UnknownDict({KeyPlaceholder("unsure"): ValuePlaceholder("unsure")})
