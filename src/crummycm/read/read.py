import pathlib

from crummycm.read.formats import parse_path_to_dict
from crummycm.read.key_instructions.instructions import (
    apply_decs,
    parse_value,
    value_contains_instruction,
)


def _r_parse_dict(cur_in, unsafe=False):
    # NOTE: RECURSIVE
    if isinstance(cur_in, dict):
        td = {}
        for k, v in cur_in.items():
            if isinstance(v, dict):
                td[k] = _r_parse_dict(v, unsafe=unsafe)
            else:
                if value_contains_instruction(v):
                    decs, v = parse_value(v)
                    v = apply_decs(decs, v)
                    td[k] = v
                else:
                    td[k] = v
        return td
    else:
        raise ValueError("wrong type")


def parse(cur_in, unsafe=False):
    if isinstance(cur_in, str):
        if pathlib.Path(cur_in).is_file():
            temp_dict = parse_path_to_dict(cur_in, unsafe=unsafe)
            return_dict = _r_parse_dict(temp_dict)
        else:
            raise FileNotFoundError(f"specified file ({cur_in}) is not found")
    elif isinstance(cur_in, dict):
        return_dict = _r_parse_dict(cur_in)
    else:
        raise ValueError(
            f"please pass a dict or a path (as a str) not {type(cur_in)}, ({cur_in})"
        )
    return return_dict
