from crummycm.read.key_instructions.functions.standard import parse_path

INSTRUCTION_STR = "::"


def value_contains_instruction(v):
    global INSTRUCTION_STR
    if isinstance(v, str):
        if INSTRUCTION_STR in v:
            return True
    return False


def parse_value(v):
    global INSTRUCTION_STR
    decs, v = v.split(INSTRUCTION_STR)
    return decs, v


def apply_decs(decs, v):
    # TODO: try: split decs on decs_split
    for d in decs.split("&"):
        if d == "path":
            v = parse_path(v)

    # TODO: look up dec
    # TODO: apply dec
    return v
