import crummycm as ccm


class ConfigDict(ccm.validation.types.dicts.base_dict.BaseDict):
    # a wrapper that contains a combination of base dict types
    def __init__(self, in_dict):
        super().__init__(in_dict)
