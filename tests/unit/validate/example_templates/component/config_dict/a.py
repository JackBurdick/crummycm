from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)
from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.dicts.foundation.known_dict import KnownDict
from crummycm.validation.types.dicts.config_dict import ConfigDict as CD
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.base import BaseValue
cd_outer = CD(
    {
        "my_mixed": CD(
            {
                "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
                KeyPlaceholder("some_str", ends_with="_str"): Text(),
                KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
                "wild_card": ValuePlaceholder("wild_card_value"),
            }
        )
    }
)

no_cd_single = {
    "my_mixed": {
        "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
        KeyPlaceholder("some_str", ends_with="_str"): Text(),
        KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
        "wild_card": ValuePlaceholder("wild_card_value"),
    }
}

no_cd_single_nested = {
    "my_mixed": {
        "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
        KeyPlaceholder("some_str", ends_with="_str"): Text(),
        KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
        "wild_card": ValuePlaceholder("wild_card_value"),
        "nested_md": {
            "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
            KeyPlaceholder("some_str", ends_with="_str"): Text(),
            KeyPlaceholder("some_num"): ValuePlaceholder("user_num"),
            "wild_card": ValuePlaceholder("wild_card_value"),
        },
    }
}
