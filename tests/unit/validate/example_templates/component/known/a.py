from crummycm.types.dicts.foundation.known_dict import KnownDict
from crummycm.types.values.foundation.numeric import Numeric
from crummycm.types.values.foundation.text import Text

# from crummycm.types.values.base import Base

A_ex = {
    "my_num": Numeric(default_value=int(0), required=False, is_type=int),
    "my_str": Text(default_value="Jack", required=False, is_type=str),
}

A_named_ex = {
    "config": KnownDict(
        {
            "my_num": Numeric(default_value=int(0), required=False, is_type=int),
            "my_str": Text(default_value="Jack", required=False, is_type=str),
        }
    )
}

A_named_out = KnownDict(
    {"my_num": Numeric(default_value=int(0), required=False, is_type=int)}
)

A_nested_known_ex = {
    "config": KnownDict(
        {
            "my_num": Numeric(default_value=int(0), required=False, is_type=int),
            "my_dict": KnownDict(
                {
                    "my_num": Numeric(default_value=0, required=False, is_type=int),
                    "my_str": Text(default_value="Jack", required=False, is_type=str),
                }
            ),
        }
    )
}


A_extra_nested_known_ex = {
    "config": KnownDict(
        {
            "my_num": Numeric(default_value=int(0), required=False, is_type=int),
            "my_dict": KnownDict(
                {
                    "my_inner_dict": KnownDict(
                        {
                            "my_val": Numeric(
                                default_value=0, required=False, is_type=int
                            ),
                            "my_extra_inner_dict": KnownDict(
                                {
                                    "my_num": Numeric(
                                        default_value=0.1, required=False, is_type=float
                                    ),
                                    "my_str": Text(
                                        default_value="Jack",
                                        required=False,
                                        is_type=str,
                                    ),
                                }
                            ),
                        }
                    ),
                    "my_str": Text(default_value="Jack", required=False, is_type=str),
                }
            ),
        }
    )
}
