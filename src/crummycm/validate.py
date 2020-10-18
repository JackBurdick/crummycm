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
        except ValueError:
            try:
                cur_raw_v = spec.default_value
            except AttributeError:
                raise ValueError(
                    f"no value is specified for {k} no default is specified"
                )
        except KeyError:
            try:
                cur_raw_v = spec.default_value
            except AttributeError:
                raise ValueError(
                    f"no value is specified for {k} and no default is specified"
                )
    return cur_raw_v


def validate(raw: Any, template: Any):
    # assert raw.keys() == template.keys(), f"not equal"  # check unused keys
    formatted = {}
    if isinstance(template, dict):
        for k, spec in template.items():
            cur_val = _obtain_init_value(k, raw, spec)
            print(cur_val)
            try:
                formatted[k] = spec.transform(cur_val)
            except AttributeError:
                formatted[k] = cur_val
    return formatted
