from crummycm.validation.types.values.compound.multi import Multi
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text
from crummycm.validation.types.values.compound.either import Either

Num_or_Text = {
    "my_either": Either(
        either_seq={Numeric(required=False, is_type=float), Text(required=False)}
    )
}
