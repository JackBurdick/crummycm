from crummycm.validation.types.dicts.config_dict import ConfigDict as MD
from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder as KPH
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text
from crummycm.validation.types.values.compound.multi import Multi

"""
data:
  name: "mnist"
  schema:
    x_image:
      shape: [28, 28, 1]
      dtype: "float32"
    y_target:
      shape: [1, 1]
      dtype: "int32"
  source: "http://yann.lecun.com/exdb/mnist/"

"""
ACCEPTED_DTYPES = ["int32", "float32", "int64", "float64"]

TEMPLATE = MD(
    {
        "data": MD(
            {
                "name": Text(required=True, to_lower=True),
                "schema": MD(
                    {
                        KPH(name="feature_name", multi=True, required=True): MD(
                            {
                                "shape": Multi(
                                    required=True,
                                    is_type=list,
                                    element_types=Numeric(is_type=int),
                                ),
                                "dtype": Text(
                                    required=True, is_in_list=ACCEPTED_DTYPES
                                ),
                            }
                        )
                    }
                ),
                "source": Text(required=True, starts_with="http:"),
            }
        )
    }
)

