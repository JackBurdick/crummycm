from crummycm.types.component.base_dict import KeyPlaceholder
from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.types.component.known_dict import KnownDict
from crummycm.types.element.numeric import Numeric
from crummycm.types.element.text import Text

# from crummycm.types.element.base import Base
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
