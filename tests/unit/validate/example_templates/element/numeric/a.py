from crummycm.validation.types.values.element.numeric import Numeric

A_EX_TEMP = {"my_num": Numeric(default_value=int(0), required=False, is_type=int)}
# type
A_required_EX_TEMP = {"my_num": Numeric(required=True, is_type=float)}
# # type
A_int_EX_TEMP = {"my_num": Numeric(is_type=int)}
A_float_EX_TEMP = {"my_num": Numeric(is_type=float)}

# fn
def add_number_n_times(raw, number=1, times=1):
    out = raw + (number * times)
    return out


A_fn_EX_TEMP = {"my_num": Numeric(fn=add_number_n_times, is_type=int)}
A_fn_kwargs_EX_TEMP = {
    "my_num": Numeric(
        fn=add_number_n_times, fn_kwargs={"number": 1, "times": 10}, is_type=int
    )
}
A_fn_bad_kwargs_EX_TEMP = {
    "my_num": Numeric(
        fn=add_number_n_times, fn_kwargs={"xxxx": 3, "times": 2}, is_type=int
    )
}

numeric_bounds_inf = {
    "my_num": Numeric(
        default_value=int(0), required=False, is_type=int, bounds=(0, float("inf"))
    )
}

numeric_bounds_1_1 = {
    "my_num": Numeric(default_value=int(0), required=False, is_type=int, bounds=(-1, 1))
}

numeric_bounds_1_1_inc = {
    "my_num": Numeric(
        default_value=int(0),
        required=False,
        is_type=int,
        bounds=(-1, 1),
        bounds_inclusive=(True, True),
    )
}
