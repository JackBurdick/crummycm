from crummycm.read.formats import parse_path_to_dict
from crummycm.read.key_instructions.instructions import (
    value_contains_instruction,
    parse_value,
    apply_decs,
)
import pathlib


# def _r_maybe_expand_dict(cur_d: Dict[str, Any], unsafe: bool):
#     temp_dict = {}
#     for k, v in cur_d.items():
#         if k == "config_path":
#             if isinstance(v, str):
#                 if pathlib.Path(v).is_file():
#                     vd = parse_path_to_dict(v, unsafe=unsafe)
#                     vd = _r_maybe_expand_dict(vd)
#                 else:
#                     raise FileNotFoundError(f"file {v} specified by {k} does not exist")
#                 return vd
#             else:
#                 raise ValueError(
#                     f"value specified ({v}) is type ({type(v)}), not a str indicating a path"
#                 )
#         else:
#             temp_dict[k] = v
#     return temp_dict


def _r_parse_dict(cur_in, unsafe=False):
    # NOTE: RECURSIVE
    if isinstance(cur_in, dict):
        td = {}
        for k, v in cur_in.items():
            # if
            # # if k == "config_path":
            # #     td[k] = parse_path_to_dict(v, unsafe=unsafe)
            # else:
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
