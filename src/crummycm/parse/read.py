from typing import Any, Dict
from crummycm.parse.read_format.json import parse_json_from_path
from crummycm.parse.read_format.yaml import parse_yaml_from_path
from crummycm.parse.read_format.xml import parse_xml_from_path
from crummycm.parse.read_format.proto import parse_proto_from_path
import pathlib


def _determine_file_format(user_in: Any) -> str:
    # basic check based on file extention
    if isinstance(user_in, str):
        if user_in.endswith(".json"):
            return "json"
        elif user_in.endswith(".yaml") or user_in.endswith(".yml"):
            return "yaml"
        elif user_in.endswith(".xml"):
            return "xml"
        elif user_in.endswith(".proto"):
            return "proto"
        else:
            raise ValueError(f"format {user_in} is not allowed")
    else:
        raise ValueError(f"type {type(user_in)} ({user_in}) is not allowed")


def _extract_dict_from_path(cur_path: str, in_format: str, ignore_types=False) -> dict:
    if in_format == "json":
        raw_dict = parse_json_from_path(cur_path)
    elif in_format == "yaml":
        raw_dict = parse_yaml_from_path(cur_path)
    elif in_format == "proto":
        raw_dict = parse_proto_from_path(cur_path)
    elif in_format == "xml":
        raw_dict = parse_xml_from_path(cur_path)
        if not ignore_types:
            raise NotImplementedError(
                f"XML parsing is occuring, but the type may not be preserved"
            )
    else:
        raise ValueError(f"the specified {in_format} is not valid")

    if not raw_dict:
        raise ValueError(
            f"The config file was found in {cur_path} as format {in_format}, but appears to be empty. It is also possible the file is not valid"
        )
    return raw_dict


# TODO: parse nested
def _parse_path_to_dict(user_in, unsafe=False):
    in_format: str = _determine_file_format(user_in)
    raw_dict: Dict[str, Any] = _extract_dict_from_path(
        user_in, in_format, ignore_types=unsafe
    )
    return raw_dict


def _r_maybe_expand_dict(cur_d: Dict[str, Any], unsafe: bool):
    temp_dict = {}
    for k, v in cur_d.items():
        if k == "config_path":
            if isinstance(v, str):
                if pathlib.Path(v).is_file():
                    vd = _parse_path_to_dict(v, unsafe=unsafe)
                    vd = _r_maybe_expand_dict(vd)
                else:
                    raise FileNotFoundError(f"file {v} specified by {k} does not exist")
                return vd
            else:
                raise ValueError(
                    f"value specified ({v}) is type ({type(v)}), not a str indicating a path"
                )
        else:
            temp_dict[k] = v
    return temp_dict


def _r_parse_dict(cur_in, unsafe=False):
    # NOTE: RECURSIVE
    if isinstance(cur_in, dict):
        td = {}
        for k, v in cur_in.items():
            if k == "config_path":
                td[k] = _parse_path_to_dict(v, unsafe=unsafe)
            else:
                if isinstance(v, dict):
                    td[k] = _r_parse_dict(v, unsafe=unsafe)
                else:
                    td[k] = v
        return td
    else:
        raise ValueError("wrong type")


def parse(cur_in, unsafe=False):
    if isinstance(cur_in, str):
        if pathlib.Path(cur_in).is_file():
            temp_dict = _parse_path_to_dict(cur_in, unsafe=unsafe)
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
