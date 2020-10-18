from typing import Any

# def has_method(o, name):
#     # https://stackoverflow.com/questions/7580532/how-to-check-whether-a-method-exists-in-python
#     return callable(getattr(o, name, None))


def _obtain_init_value(k, raw, spec):
    # obtain value
    if spec.required:
        cur_raw_v = raw[k]
    else:
        try:
            cur_raw_v = raw[k]
        except KeyError:
            try:
                cur_raw_v = spec.default
            except AttributeError:
                raise ValueError(
                    f"no value is specified for {k}, but it is required and no default is specified"
                )
    return cur_raw_v


def validate(raw: Any, template: Any):
    # assert raw.keys() == template.keys(), f"not equal"  # check unused keys
    formatted = {}
    if isinstance(template, dict):
        for k, spec in template.items():
            _obtain_init_value(k, raw, spec)
            try:
                formatted[k] = spec.transform(raw[k])
            except AttributeError:
                formatted[k] = raw[k]
    return formatted
