from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)
from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.dicts.foundation.known_dict import KnownDict
from crummycm.validation.types.dicts.config_dict import ConfigDict as CD
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

no_catchall = CD(
    {
        "my_mixed": CD(
            {
                "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
                KeyPlaceholder("some_str", ends_with="_str"): Text(),
                "wild_card": ValuePlaceholder("wild_card_value"),
            }
        )
    }
)

inner_multi_catchall = CD(
    {
        "my_mixed": CD(
            {
                "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
                KeyPlaceholder("some_str", ends_with="_str"): Text(),
                "wild_card": ValuePlaceholder("wild_card_value"),
                KeyPlaceholder("anything", multi=True): ValuePlaceholder(
                    "anything_value"
                ),
            }
        )
    }
)

inner_single_catchall = CD(
    {
        "my_mixed": CD(
            {
                "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
                KeyPlaceholder("some_str", ends_with="_str"): Text(),
                "wild_card": ValuePlaceholder("wild_card_value"),
                KeyPlaceholder("anything"): ValuePlaceholder("anything_value"),
            }
        )
    }
)
