from crummycm.validation.types.dicts.base_dict import KeyPlaceholder, ValuePlaceholder
from crummycm.validation.types.dicts.foundation.unknown_dict import UnknownDict
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.base import BaseValue

A_inner_unknown = {
    "some_config": UnknownDict(
        {KeyPlaceholder("something", required=True): ValuePlaceholder("someval")}
    )
}

A_inner_unknown_multi = {
    "some_config": UnknownDict(
        {
            KeyPlaceholder("something", required=True, multi=True): ValuePlaceholder(
                "someval"
            )
        }
    )
}

A_outer_unknown = UnknownDict({KeyPlaceholder("unsure"): ValuePlaceholder("unsure")})

A_inner_unknown_required_false = {
    "some_config": UnknownDict(
        {KeyPlaceholder("something", required=False): ValuePlaceholder("someval")}
    )
}

A_outer_unknown_req_false = UnknownDict(
    {KeyPlaceholder("unsure", required=False): ValuePlaceholder("unsure")}
)

double_inner_unknown = {
    "some_config": UnknownDict(
        {
            KeyPlaceholder("something", required=True): ValuePlaceholder("someval"),
            KeyPlaceholder(
                "my_something", required=True, starts_with="my_"
            ): ValuePlaceholder("someval"),
        }
    )
}

double_inner_unknown_multi = {
    "some_config": UnknownDict(
        {
            KeyPlaceholder("something", required=True): ValuePlaceholder("someval"),
            KeyPlaceholder(
                "my_something_multi", required=True, starts_with="my_", multi=True
            ): ValuePlaceholder("someval"),
        }
    )
}

double_inner_unknown_unstrict_multi = {
    "some_config": UnknownDict(
        {
            KeyPlaceholder("something", required=True, multi=True): ValuePlaceholder(
                "someval"
            ),
            KeyPlaceholder(
                "my_something_multi", required=True, starts_with="my_"
            ): ValuePlaceholder("someval"),
        }
    )
}

double_inner_unknown_mixed_req_multi = {
    "some_config": UnknownDict(
        {
            KeyPlaceholder("something", required=False): ValuePlaceholder("someval"),
            KeyPlaceholder(
                "my_something_multi", required=True, starts_with="my_", multi=True
            ): ValuePlaceholder("someval"),
        }
    )
}

double_inner_unknown_mixed_req_multi_b = {
    "some_config": UnknownDict(
        {
            KeyPlaceholder("something", required=True): ValuePlaceholder("someval"),
            KeyPlaceholder(
                "my_something_multi", required=False, starts_with="my_", multi=True
            ): ValuePlaceholder("someval"),
        }
    )
}

# TODO: don't allow multi same name on initialization of UnknownDict
