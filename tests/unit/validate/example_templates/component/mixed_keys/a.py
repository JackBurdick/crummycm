from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)
from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.dicts.foundation.known_dict import KnownDict
from crummycm.validation.types.dicts.mixed_dict import MixedDict as MD
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.base import BaseValue
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


mixed_all_single_key_unnamed_req_false = {
    "my_mixed": MD(
        {
            "kd_num": Numeric(default_value=int(0), is_type=int),
            KeyPlaceholder("some_str", ends_with="_str", required=False): Text(),
            KeyPlaceholder("some_num", required=True): ValuePlaceholder("user_num"),
            "wild_card": ValuePlaceholder("wild_card_value"),
        }
    )
}

mixed_all_single_key_unnamed_req_false_v_req_false = {
    "my_mixed": MD(
        {
            "kd_num": Numeric(default_value=int(0), is_type=int),
            KeyPlaceholder("some_str", ends_with="_str", required=False): Text(
                required=False
            ),
            KeyPlaceholder("some_num", required=True): ValuePlaceholder("user_num"),
            "wild_card": ValuePlaceholder("wild_card_value"),
        }
    )
}

mixed_all_single_key_unnamed_req_false_v_req_false_default = {
    "my_mixed": MD(
        {
            "kd_num": Numeric(default_value=int(0), is_type=int),
            KeyPlaceholder("some_str", ends_with="_str", required=False): Text(
                default_value="DIESEL"
            ),
            KeyPlaceholder("some_num", required=True): ValuePlaceholder("user_num"),
            "wild_card": ValuePlaceholder("wild_card_value"),
        }
    )
}
