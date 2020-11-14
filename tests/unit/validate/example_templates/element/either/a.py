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
        return_type=list,
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
        either_seq=[Multi(required=False), Text(required=False)], return_type=list
    )
}

list_or_text_return_tuple = {
    "my_either": Either(
        either_seq=[Multi(required=False), Text(required=False)], return_type=tuple
    )
}


# Num_or_Text = {
#     "my_either": Either(
#         either_seq={Numeric(required=False, is_type=float), Text(required=False)}
#     )
# }
