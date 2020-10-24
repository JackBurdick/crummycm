from crummycm.types.component.base_dict import KeyPlaceholder
from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.types.element.numeric import Numeric
from crummycm.types.element.text import Text

# from crummycm.types.element.base import Base
A_ex = {"val": Numeric(default_value=int(0), required=False, is_type=int)}

A_unnamed_single_num_ex = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("some_key"): Numeric(
                default_value=int(0), required=False, is_type=int
            )
        }
    )
}

A_unnamed_single_num_multi_ex = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("some_key", multi=True): Numeric(
                default_value=int(0), required=False, is_type=int
            )
        }
    )
}

A_unnamed_single_num_startswith_ex = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("my_key", starts_with="val_"): Numeric(
                default_value=int(0), required=False, is_type=int
            )
        }
    )
}

A_unnamed_double_dist = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("my_key"): Numeric(
                default_value=int(0), required=False, is_type=int
            ),
            KeyPlaceholder("my_other_key", ends_with="_val"): Numeric(
                default_value=int(0), required=False, is_type=int
            ),
        }
    )
}


A_unnamed_single_num_endswith_ex = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("my_key", ends_with="_val"): Numeric(
                default_value=int(0), required=False, is_type=int
            )
        }
    )
}


A_unnamed_out = UnnamedDict(
    {
        KeyPlaceholder("my_num"): Numeric(
            default_value=int(0), required=False, is_type=int
        )
    }
)


A_nested_unnamed_num = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("some_dict"): UnnamedDict(
                {
                    KeyPlaceholder("inner_num"): Numeric(
                        default_value=int(0), required=False, is_type=int
                    )
                }
            )
        }
    )
}

A_quad_nested_unnamed_num = {
    "config": UnnamedDict(
        {
            KeyPlaceholder("some_dict"): UnnamedDict(
                {
                    KeyPlaceholder("another_dict"): UnnamedDict(
                        {
                            KeyPlaceholder("yet_another_dict"): UnnamedDict(
                                {
                                    KeyPlaceholder("some_num"): Numeric(
                                        default_value=int(0),
                                        required=False,
                                        is_type=int,
                                    )
                                }
                            )
                        }
                    )
                }
            )
        }
    )
}