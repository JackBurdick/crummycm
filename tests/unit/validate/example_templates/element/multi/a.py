from crummycm.types.values.compound.multi import Multi
from crummycm.types.values.element.numeric import Numeric

SINGLE = {"my_multi": Multi(required=True)}
SINGLE_default = {"my_multi": Multi(default_value=["a", "b"], required=True)}
SINGLE_default_tup = {"my_multi": Multi(default_value=("a", "b"), required=True)}
SINGLE_req_false = {"my_multi": Multi(required=False)}
SINGLE_inner_str = {"my_multi": Multi(required=True, inner_types=str)}
SINGLE_homogeneous = {"my_multi": Multi(required=True, homogeneous=True)}
SINGLE_homogeneous_float = {
    "my_multi": Multi(required=True, homogeneous=True, inner_types=float)
}
SINGLE_is_list = {"my_multi": Multi(required=True, is_type=list)}
SINGLE_multi_inner_types = {"my_multi": Multi(inner_types=(int, str))}
# SINGLE_inner_typexs = {"my_multi": Multi(inner_types=(int, str),
# homogeneous=True)} # will raise error
# SINGLE_Numeric_float = {"my_multi": Multi(inner_types=Numeric(is_type=float))}
