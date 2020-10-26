from crummycm.types.dicts.base_dict import KeyPlaceholder, ValuePlaceholder
from crummycm.types.dicts.unnamed_dict import UnnamedDict
from crummycm.types.dicts.known_dict import KnownDict
from crummycm.types.dicts.mixed_dict import MixedDict as MD
from crummycm.types.values.numeric import Numeric
from crummycm.types.values.text import Text

# from crummycm.types.values.base import Base
A_mixed_all_single = {
    "my_mixed": MD(
        {
            "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
            KeyPlaceholder("some_str", ends_with="_str"): Text(),
            KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
            "wild_card": ValuePlaceholder("wild_card_value"),
        }
    )
}

A_mixed_outter = MD(
    {
        "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
        KeyPlaceholder("some_str", ends_with="_str"): Text(),
        KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
        "wild_card": ValuePlaceholder("wild_card_value"),
    }
)

A_mixed_all_single_nested = {
    "my_mixed": MD(
        {
            "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
            KeyPlaceholder("some_str", ends_with="_str"): Text(),
            KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
            "wild_card": ValuePlaceholder("wild_card_value"),
            "nested_md": MD(
                {
                    "kd_num": Numeric(
                        default_value=int(0), required=False, is_type=int
                    ),
                    KeyPlaceholder("some_str", ends_with="_str"): Text(),
                    KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
                    "wild_card": ValuePlaceholder("wild_card_value"),
                }
            ),
        }
    )
}

A_mixed_outter_nested = MD(
    {
        "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
        KeyPlaceholder("some_str", ends_with="_str"): Text(),
        KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
        "wild_card": ValuePlaceholder("wild_card_value"),
        "nested_md": MD(
            {
                "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
                KeyPlaceholder("some_str", ends_with="_str"): Text(),
                KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
                "wild_card": ValuePlaceholder("wild_card_value"),
            }
        ),
    }
)
