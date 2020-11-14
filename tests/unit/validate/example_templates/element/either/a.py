from crummycm.validation.types.values.compound.multi import Multi
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text
from crummycm.validation.types.values.compound.either import Either

Num_or_Text_list = {
    "my_either": Either(
        either_seq=[Numeric(required=False, is_type=float), Text(required=False)]
    )
}

Num_or_Text_tuple = {
    "my_either": Either(
        either_seq=(Numeric(required=False, is_type=float), Text(required=False))
    )
}

return_list = {
    "my_either": Either(
        either_seq=[Numeric(required=False, is_type=float), Text(required=False)],
        return_as_type=list,
    )
}

text_or_list = {
    "my_either": Either(either_seq=[Text(required=False), Multi(required=False)])
}

list_or_text = {
    "my_either": Either(either_seq=[Multi(required=False), Text(required=False)])
}

list_or_text_return_list = {
    "my_either": Either(
        either_seq=[Multi(required=False), Text(required=False)], return_as_type=list
    )
}

list_or_text_return_tuple = {
    "my_either": Either(
        either_seq=[Multi(required=False), Text(required=False)], return_as_type=tuple
    )
}

l_or_t_default_list = {
    "my_either": Either(
        either_seq=[Multi(required=False), Text(required=False)],
        default_value=["a", "b"],
    )
}

f_or_t = {
    "my_either": Either(
        either_seq=[Numeric(required=False, is_type=float), Text(required=False)],
        default_value=3.3,
    )
}

f_or_t_ret_float = {
    "my_either": Either(
        either_seq=[Numeric(required=False, is_type=float), Text(required=False)],
        default_value=1.3,
        return_as_type=float,
    )
}

text_or_list_ret_str = {
    "my_either": Either(
        either_seq=[Text(required=False), Multi(required=False)], return_as_type=str
    )
}


# NOTE: not valid since it contains multiple elements of the same type
# l_or_l = {
#     "my_either": Either(
#         either_seq=[Multi(required=False), Multi(required=False)],
#         default_value=["a", "b"],
#     )
# }


# NOTE: not valid since Multi is not required, but does have a default value
# inner_default_a = {
#     "my_either": Either(
#         either_seq=[
#             Multi(required=False, default_value=["a", "b"]),
#             Text(required=False),
#         ]
#     )
# }

