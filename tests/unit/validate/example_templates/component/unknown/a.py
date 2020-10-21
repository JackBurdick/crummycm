from crummycm.types.component.base_dict import KeyPlaceholder, ValuePlaceholder
from crummycm.types.component.unknown_dict import UnknownDict
from crummycm.types.element.numeric import Numeric
from crummycm.types.element.text import Text

# from crummycm.types.element.base import Base

A_inner_unknown = {"some_config": UnknownDict({KeyPlaceholder: ValuePlaceholder})}

A_outer_unknown = UnknownDict({KeyPlaceholder: ValuePlaceholder})
