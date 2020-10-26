from crummycm.types.component.base_dict import KeyPlaceholder, ValuePlaceholder
from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.types.component.known_dict import KnownDict
from crummycm.types.component.mixed_dict import MixedDict as MD
from crummycm.types.element.numeric import Numeric
from crummycm.types.element.text import Text

# from crummycm.types.element.base import Base
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
