from crummycm.types.component.base_dict import KeyPlaceholder
from crummycm.types.component.unnamed_dict import UnnamedDict
from crummycm.types.element.numeric import Numeric
from crummycm.types.element.text import Text

# from crummycm.types.element.base import Base
A_ex = {
    "val": Numeric(default_value=int(0), required=False, is_type=int),
}

A_unnamed_single_num_ex = {
    "config": UnnamedDict(
        {
            KeyPlaceholder: Numeric(default_value=int(0), required=False, is_type=int),
        }
    )
}

A_nested_unnamed_num = {
    "config": UnnamedDict(
        {
            KeyPlaceholder: UnnamedDict(
                {
                    KeyPlaceholder: Numeric(
                        default_value=int(0), required=False, is_type=int
                    ),
                }
            ),
        }
    )
}

A_quad_nested_unnamed_num = {
    "config": UnnamedDict(
        {
            KeyPlaceholder: UnnamedDict(
                {
                    KeyPlaceholder: UnnamedDict(
                        {
                            KeyPlaceholder: UnnamedDict(
                                {
                                    KeyPlaceholder: Numeric(
                                        default_value=int(0),
                                        required=False,
                                        is_type=int,
                                    ),
                                }
                            ),
                        }
                    ),
                }
            ),
        }
    )
}