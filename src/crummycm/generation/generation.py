import crummycm as ccm
from typing import Any


def generate(user_in: Any, template: Any, disallow_unused=True):
    raw = ccm.parse(user_in)
    out = ccm.validate(raw, template, disallow_unused)
    return out
