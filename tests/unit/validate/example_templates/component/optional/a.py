from crummycm.validation.types.placeholders.placeholder import (
    KeyPlaceholder,
    ValuePlaceholder,
)

# from crummycm.validation.types.dicts.foundation.unnamed_dict import UnnamedDict
from crummycm.validation.types.dicts.foundation.named_dict import NamedDict
from crummycm.validation.types.dicts.config_dict import ConfigDict as CD

# from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text

# from crummycm.validation.types.values.base import BaseValue
required_num_false = {
    "my_conf": CD({KeyPlaceholder("my_val"): ValuePlaceholder("some_val")})
}

required_num_true = {
    "my_conf": CD(
        {KeyPlaceholder("my_val", required=True): ValuePlaceholder("some_val")}
    )
}
required_num_true_true = {
    "my_conf": CD({KeyPlaceholder("my_text", required=True): Text(required=True)})
}

required_num_true_false = {
    "my_conf": CD({KeyPlaceholder("my_text", required=True): Text(required=False)})
}

required_num_true_false_default = {
    "my_conf": CD(
        {KeyPlaceholder("my_text", required=True): Text(default_value="Jack")}
    )
}

# if the key is present, the value is required
# if the key isn't present, ignore
required_num_false_true = {
    "my_conf": {KeyPlaceholder("my_text", required=False): Text(required=True)}
}

req_unknown = {
    "my_conf": {
        KeyPlaceholder("my_text", required=False): ValuePlaceholder("my_text_value")
    }
}

req_unknown_populate = {
    "my_conf": {
        KeyPlaceholder(
            "my_text", required=False, exact=True, populate=True
        ): ValuePlaceholder("my_text_value")
    }
}

req_unnammed_populate = {
    "my_conf": {
        KeyPlaceholder("my_text", required=False, exact=True, populate=True): Text(
            required=True, default_value="hello"
        )
    }
}

req_unnammed_populate_nested = {
    "my_conf": {
        KeyPlaceholder("my_text", required=False, exact=True, populate=True): {
            "inner_text": Text(required=True, default_value="hello")
        }
    }
}
