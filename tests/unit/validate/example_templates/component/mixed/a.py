from crummycm.types.dicts.base_dict import KeyPlaceholder
from crummycm.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.types.dicts.foundation.known_dict import KnownDict
from crummycm.types.values.foundation.numeric import Numeric
from crummycm.types.values.foundation.text import Text

# from crummycm.types.values.base import Base
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
