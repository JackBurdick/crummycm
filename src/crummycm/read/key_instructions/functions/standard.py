import crummycm as ccm

# TODO: I'm not sure why I'm having trouble with the import here
# from crummycm.read.read import parse
# from crummycm import parse
# ^ neither work and I'm unsure why


def parse_path(v, unsafe=True):
    v = ccm.parse(v, unsafe)
    return v
