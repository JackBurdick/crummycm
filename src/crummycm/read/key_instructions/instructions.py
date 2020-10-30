from crummycm.read.key_instructions.functions import standard
import inspect

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
    # TODO: cache this?
    standard_fns = dict(
        [o for o in inspect.getmembers(standard) if inspect.isfunction(o[1])]
    )

    # NOTE: order is important
    for d in decs.split("&"):
        if d in standard_fns.keys():
            v = standard_fns[d](v)
    return v
