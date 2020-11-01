from crummycm.validation.types.values.base import BaseValue


class Bool(BaseValue):
    def __init__(
        self,
        default_value=None,
        is_type=bool,
        required=None,
        description=None,
        fn=None,
        fn_kwargs=None,
    ):

        self.ALLOWED_TYPES = (bool,)
        assert is_type in self.ALLOWED_TYPES, ValueError(
            f"{self.__class__.__name__} class can only be of type {self.ALLOWED_TYPES} not type {is_type}"
        )

        super().__init__(
            default_value=default_value,
            is_type=is_type,
            required=required,
            description=description,
            fn=fn,
            fn_kwargs=fn_kwargs,
        )

    def transform(self, cur_value=None):
        if cur_value is not None:
            if not isinstance(cur_value, self.ALLOWED_TYPES):
                raise TypeError(
                    f"cur_value ({cur_value}) is not type {self.ALLOWED_TYPES}"
                )
        self.user_in = cur_value
        iv = super().transform(self.user_in)

        self.out = iv
        return self.out
