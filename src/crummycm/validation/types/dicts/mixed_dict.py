from crummycm.validation.types.dicts.base_dict import BaseDict


class MixedDict(BaseDict):
    # a wrapper that contains a combination of base dict types
    def __init__(self, in_dict):
        super().__init__(in_dict)
