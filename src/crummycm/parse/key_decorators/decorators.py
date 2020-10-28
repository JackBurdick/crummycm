DECORATOR_STR = "::"


def is_value_decorated(v):
    global DECORATOR_STR
    if isinstance(v, str):
        if DECORATOR_STR in v:
            return True
    return False


def parse_value(v):
    global DECORATOR_STR
    decs, v = v.split(DECORATOR_STR)
    return decs, v


def apply_decs(decs, v):
    # TODO: try: split decs on decs_split
    # TODO: look up dec
    # TODO: apply dec
    return v
