from typing import Any, Dict

from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct

"""
proto information: 
- https://developers.google.com/protocol-buffers/docs/pythontutorial
- https://stackoverflow.com/questions/56303736/how-do-you-create-a-protobuf-struct-from-a-python-dict

"""


def parse_proto_from_path(path: str) -> Dict[str, Any]:
    try:
        s = Struct()
        with open(path, "rb") as data_file:
            try:
                r = data_file.read()
                s.ParseFromString(r)
                data = MessageToDict(s)
                return data
            except:
                print(f"Error loading proto to dict for file {path}")
                return dict()
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file {path} was not found")
