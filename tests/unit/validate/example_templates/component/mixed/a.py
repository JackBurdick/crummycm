from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder
from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.dicts.foundation.known_dict import KnownDict
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.base import BaseValue
A_known_uk = {
    "known_dict": KnownDict(
        {
            "kd_num": Numeric(default_value=int(0), required=False, is_type=int),
            "uk_dict": UnnamedDict(
                {
                    KeyPlaceholder("a_num"): Numeric(
                        default_value=int(0), required=False, is_type=int
                    )
                }
            ),
        }
    )
}

A_uk_k = {
    "my_conf": UnnamedDict(
        {
            KeyPlaceholder("a_num"): KnownDict(
                {"my_num": Numeric(default_value=int(0), required=False, is_type=int)}
            )
        }
    )
}


A_outter_nested_uk_uk = UnnamedDict(
    {
        KeyPlaceholder("a_dict"): UnnamedDict(
            {
                KeyPlaceholder("a_num"): Numeric(
                    default_value=0, required=False, is_type=int
                )
            }
        )
    }
)
