import crummycm as ccm
from typing import Any


def generate(user_in: Any, template: Any):
    raw = ccm.parse(user_in)
    out = ccm.validate(raw, template)
    return out
