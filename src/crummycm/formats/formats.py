from typing import Any, Dict

from crummycm.formats.format.json import parse_json_from_path, write_dict_to_json
from crummycm.formats.format.proto import parse_proto_from_path, write_dict_to_proto
from crummycm.formats.format.xml import parse_xml_from_path, write_dict_to_xml
from crummycm.formats.format.yaml import parse_yaml_from_path, write_dict_to_yaml


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


def _write_dict_to_path(data: Dict[str, Any], cur_path: str, in_format: str) -> str:
    out_path = None
    if in_format == "json":
        out_path = write_dict_to_json(data=data, path=cur_path)
    elif in_format == "yaml":
        out_path = write_dict_to_yaml(data=data, path=cur_path)
    elif in_format == "proto":
        raise NotImplementedError("unable to write proto format correctly")
        # out_path = write_dict_to_proto(data=data, path=cur_path)
    elif in_format == "xml":
        raise NotImplementedError("unable to write xml format correctly")
        # out_path = write_dict_to_xml(data=data, path=cur_path)
    else:
        raise ValueError(f"the specified {in_format} is not valid")

    if not out_path:
        raise ValueError(f"The dict was not written as {in_format}")
    return out_path


# TODO: parse nested
def parse_path_to_dict(user_in, unsafe=False):
    in_format: str = _determine_file_format(user_in)
    raw_dict: Dict[str, Any] = _extract_dict_from_path(
        user_in, in_format, ignore_types=unsafe
    )
    return raw_dict


def write_dict_to_file(data, write_path):
    in_format: str = _determine_file_format(write_path)
    out_path: str = _write_dict_to_path(data, write_path, in_format)
    return out_path
