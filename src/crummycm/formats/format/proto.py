from typing import Any, Dict


"""
proto information: 
- https://developers.google.com/protocol-buffers/docs/pythontutorial
- https://stackoverflow.com/questions/56303736/how-do-you-create-a-protobuf-struct-from-a-python-dict

"""


def parse_proto_from_path(path: str) -> Dict[str, Any]:
    from google.protobuf.json_format import MessageToDict
    from google.protobuf.struct_pb2 import Struct

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


def write_dict_to_proto(data: Dict[str, Any], path: str) -> str:
    from google.protobuf.struct_pb2 import Struct

    s = Struct()
    s.update(data)
    with open(f"{path}", "wb") as f:
        f.write(s.SerializeToString())
    return f"{path}"
