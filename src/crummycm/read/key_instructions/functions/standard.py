from crummycm.read.read import parse_path_to_dict


def parse_path(v, unsafe=True):
    v = parse_path_to_dict(v, unsafe)
    return v
