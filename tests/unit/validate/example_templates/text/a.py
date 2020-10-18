from crummycm.types.component.text import Text

A_EX_TEMP = {"my_text": Text(default_value="Jack", required=False)}
# type
A_required_EX_TEMP = {"my_text": Text(required=True)}

# built_in
A_to_lower = {"my_text": Text(to_lower=True)}

A_is_in_list_true = {"my_text": Text(is_in_list=["Jack", "Diesel", "Abby"])}

A_contains_true = {"my_text": Text(contains=".jpg")}

A_contains_one_of_true = {"my_text": Text(contains_one_of=[".jpg", ".png"])}

A_starts_with_True = {"my_text": Text(starts_with="j")}
A_starts_with_False = {"my_text": Text(starts_with="x")}

A_ends_with_True = {"my_text": Text(ends_with=".jpg")}
A_ends_with_False = {"my_text": Text(ends_with=".xxx")}


# fn
def add_letter_n_times(raw, letter="B", times=1):
    out = raw + f"{letter}" * times
    return out


A_fn = {"my_text": Text(fn=add_letter_n_times)}
A_fn_kwargs = {
    "my_text": Text(fn=add_letter_n_times, fn_kwargs={"letter": "B", "times": 3})
}
A_fn_bad_kwargs = {
    "my_text": Text(fn=add_letter_n_times, fn_kwargs={"xxxx": "B", "times": 2})
}
