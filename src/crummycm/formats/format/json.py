import json
from typing import Any, Dict


def _dict_raise_on_duplicates(ordered_pairs):
    """
    Reject duplicate keys. (used by json load)

    src: https://stackoverflow.com/questions/14902299/json-loads-allows-duplicate-keys-in-a-dictionary-overwriting-the-first-value
    """

    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError("duplicate key: %r" % (k,))
        else:
            d[k] = v
    return d


def parse_json_from_path(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as data_file:
            try:
                # TODO: validate that duplicates are flagged
                data = json.loads(
                    data_file.read(), object_pairs_hook=_dict_raise_on_duplicates
                )
                return data
            except:
                print(f"Error loading json to dict for file {path}")
                return dict()
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file {path} was not found")


def write_dict_to_json(data: Dict[str, Any], path: str):
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=2)
    return outfile
