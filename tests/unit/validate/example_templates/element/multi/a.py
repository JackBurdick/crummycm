from crummycm.types.values.compound.multi import Multi

SINGLE = {"my_multi": Multi(required=True)}
SINGLE_default = {"my_multi": Multi(default_value=["a", "b"], required=True)}
SINGLE_req_false = {"my_multi": Multi(required=False)}
