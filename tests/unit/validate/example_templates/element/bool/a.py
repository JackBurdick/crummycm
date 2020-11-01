from crummycm.validation.types.values.element.bool import Bool

req_true = {"my_bool": Bool(required=True)}
req_true_default = {"my_bool": Bool(required=True, default_value=True)}
