import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode
from typing import Any, Dict

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class UniqueKeyLoader(Loader):
    """
    src: https://gist.github.com/pypt/94d747fe5180851196eb#gistcomment-2084028
    """

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(
                None,
                None,
                "expected a mapping node, but found %s" % node.id,
                node.start_mark,
            )
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unacceptable key (%s)" % exc,
                    key_node.start_mark,
                )
            # check for duplicate keys
            if key in mapping:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found duplicate key",
                    key_node.start_mark,
                    f"duplicate key: {key} -- please rename the key to something else",
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


yaml.SafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, UniqueKeyLoader.construct_mapping
)


def parse_yaml_from_path(path: str) -> dict:
    # return python dict from yaml path
    try:
        with open(path, "r") as stream:
            try:
                y = yaml.load(stream, Loader=yaml.SafeLoader)
                return y
            except yaml.YAMLError as exc:
                print(exc)
                return dict()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error > Exiting: the configuration file {path} was not found"
        )


def write_dict_to_yaml(data: Dict[str, Any], path: str):
    with open(path, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
