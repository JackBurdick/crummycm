# import json
# from google.protobuf.json_format import Parse
from a import A_EX_DICT


# message = Parse(json.dumps(A_EX_DICT), Thing())

from google.protobuf.struct_pb2 import Struct

s = Struct()
s.update(A_EX_DICT)
with open("./a.proto", "wb") as f:
    f.write(s.SerializeToString())
