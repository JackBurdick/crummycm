import pathlib

from crummycm.read.read import parse_path_to_dict


def parse_path(v, unsafe=True):
    v = parse_path_to_dict(v, unsafe)
    return v


def path_exists(v):
    if pathlib.Path(v).exists():
        return v
    else:
        raise ValueError(f"specified path {v} does not exists")
