from crummycm.validation.types.dicts.config_dict import ConfigDict as CD
from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder as KPH
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text
from crummycm.validation.types.values.element.bool import Bool
from crummycm.validation.types.values.compound.multi import Multi


ACCEPTED_DTYPES = ["int32", "float32", "int64", "float64"]

DATA = CD(
    {
        "data": CD(
            {
                "name": Text(required=True, to_lower=True),
                "schema": CD(
                    {
                        KPH(name="feature_name", multi=True, required=True): CD(
                            {
                                "shape": Multi(
                                    required=True,
                                    is_type=list,
                                    element_types=Numeric(is_type=int),
                                ),
                                "dtype": Text(
                                    required=True, is_in_list=ACCEPTED_DTYPES
                                ),
                                KPH("label", exact=True, required=False): Bool(
                                    required=True
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
