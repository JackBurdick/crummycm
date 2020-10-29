# TODO: I'm not sure what is happening here.
# from crummycm.read.read import parse
import crummycm as ccm


def parse_path(v, unsafe=True):
    # return parse_path_to_dict(mystr)
    v = ccm.parse(v, unsafe)  # ccm.parse.read.
    return v
