from typing import Any, Dict


"""
import xmltodict
"""


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    """
    Example usage:
    from xml.etree import cElementTree as ElementTree

    >>> tree = ElementTree.to_dict('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    """

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            """
            TODO: I'm not sure how to specify types in xml at this point since every
            time I use the schema, the parser does not work and I haven't dug into
            this yet.. so for now, the types are all returned as string.
            one idea is to create the schema then apply use element.attrib to
            test for various types.
            """
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


def elements_equal(e1, e2):
    if type(e1) != type(e2):
        return False
    if e1.tag != e1.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False
    return all([elements_equal(c1, c2) for c1, c2 in zip(e1, e2)])


def parse_xml_from_path(path: str) -> dict:
    import xml.etree.ElementTree as ET

    # https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary
    # http://code.activestate.com/recipes/410469-xml-as-dictionary/
    try:
        with open(path, encoding="utf-8") as data_file:
            try:
                # https://stackoverflow.com/questions/37089533/check-and-remove-duplicated-children-tags-in-xml
                tree = ET.parse(path)
                root = tree.getroot()
                # root = ElementTree.XML(xml_string)
                prev = None
                for page in root:  # iterate over pages
                    for elem in page:
                        if elements_equal(elem, prev):
                            raise ValueError("duplicate detected")
                        prev = elem
                xmldict = XmlDictConfig(root)
                return xmldict

            except:
                print(f"Error loading xml to dict for file {path}")
                return dict()
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file {path} was not found")


E_D = {
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    '"': "&qote;",
    "'": "&apos;",
    "[": "&lsqb;",
    "]": "&rsqb;",
}


# def replace_entities(data):
#     # https://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
#     global E_D
#     out_d = {}
#     for k, v in data.items():

#         k = "".join([E_D[kc] if kc in E_D.keys() else kc for kc in k])
#         if isinstance(v, str):
#             v = "".join([E_D[vc] if vc in E_D.keys() else vc for vc in v])
#         elif isinstance(v, dict):
#             v = replace_entities(v)
#         out_d[k] = v
#     return out_d


def write_dict_to_xml(data: Dict[str, Any], path: str):
    from dict2xml import dict2xml

    # TODO: this cannot handle entities
    # ent.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # d = replace_entities(data)
    xml_str = dict2xml(data, wrap="all", indent="  ")
    with open(path, "w") as outfile:
        outfile.write(xml_str)
    return outfile
