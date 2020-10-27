from pkg_resources import get_distribution, DistributionNotFound
import os.path


# this block is adapted from
# https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
# I'm not 100% sure this is the best way to do this yet
try:
    _dist = get_distribution("crummycm")
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, "crummycm")):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "Please install this project with setup.py (e.g.`pip install ./crummycm/` or `pip install -e ./crummycm/`)"
else:
    __version__ = _dist.version


# Config
from crummycm.parse.read import parse
from crummycm.validation.validation import validate

# from crummycm.generate import config
