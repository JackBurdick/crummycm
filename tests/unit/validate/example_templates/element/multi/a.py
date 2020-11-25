from crummycm.validation.types.values.compound.multi import Multi
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

SINGLE = {"my_multi": Multi(required=True)}
SINGLE_default = {"my_multi": Multi(default_value=["a", "b"], required=True)}
SINGLE_default_tup = {"my_multi": Multi(default_value=("a", "b"), required=True)}
SINGLE_req_false = {"my_multi": Multi(required=False)}
SINGLE_inner_str = {"my_multi": Multi(required=True, element_types=str)}
SINGLE_homogeneous = {"my_multi": Multi(required=True, homogeneous=True)}
SINGLE_homogeneous_float = {
    "my_multi": Multi(required=True, homogeneous=True, element_types=float)
}
SINGLE_is_list = {"my_multi": Multi(required=True, is_type=list)}
SINGLE_multi_inner_types = {"my_multi": Multi(element_types=(int, str))}
SINGLE_Numeric_float = {"my_multi": Multi(element_types=Numeric(is_type=float))}
SINGLE_Text_lower = {"my_multi": Multi(element_types=Text(to_lower=True))}
SINGLE_Text_lower_tuple = {
    "my_multi": Multi(element_types=Text(to_lower=True), is_type=tuple)
}
SINGLE_bool = {"my_multi": Multi(element_types=bool)}
multi_int_unique = {"my_multi": Multi(element_types=int, elements_unique=True)}


# fn
def add_letter_n_times(raw, letter="B", times=1):
    for i, r in enumerate(raw):
        raw[i] = r + f"{letter}" * times
    return raw


def reversed_plus_letter(raw, letter="Z", times=1):
    out = raw[::-1] + f"{letter}" * times
    return out


SINGLE_fn = {"my_multi": Multi(fn=add_letter_n_times)}
SINGLE_fn_kwargs = {
    "my_multi": Multi(fn=add_letter_n_times, fn_kwargs={"letter": "B", "times": 3})
}
SINGLE_fn_bad_kwargs = {
    "my_multi": Multi(fn=add_letter_n_times, fn_kwargs={"xxxx": "B", "times": 2})
}

SINGLE_fn_lower_d = {
    "my_multi": Multi(
        element_types=Text(to_lower=True, fn=reversed_plus_letter),
        fn=add_letter_n_times,
    )
}
SINGLE_fn_d = {
    "my_multi": Multi(
        element_types=Text(fn=reversed_plus_letter), fn=add_letter_n_times
    )
}
