from crummycm.validation.types.values.base import BaseValue


A_EX_TEMP = {"name": BaseValue(default_value="Sam")}
# type
A_required_EX_TEMP = {"name": BaseValue(required=True)}
# type
A_int_EX_TEMP = {"name": BaseValue(is_type=int)}
A_bool_EX_TEMP = {"name": BaseValue(is_type=bool)}
A_str_EX_TEMP = {"name": BaseValue(is_type=str)}
A_float_EX_TEMP = {"name": BaseValue(is_type=float)}
# fn
def add_letter_n_times(raw, letter="a", times=3):
    out = raw + f"{letter}" * times
    return out


A_fn_EX_TEMP = {"name": BaseValue(fn=add_letter_n_times)}
A_fn_kwargs_EX_TEMP = {
    "name": BaseValue(fn=add_letter_n_times, fn_kwargs={"letter": "b", "times": 2})
}
A_fn_bad_kwargs_EX_TEMP = {
    "name": BaseValue(fn=add_letter_n_times, fn_kwargs={"xxxx": "b", "times": 2})
}
