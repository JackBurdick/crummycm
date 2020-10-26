from typing import Optional
from crummycm.types.values.base import BaseValue


class Multi(BaseValue):
    def __init__(
        self,
        default_value=None,
        is_type=None,
        required=None,
        description=None,
        fn=None,
        fn_kwargs=None,
        # specific
        homogeneous=None,
        inner_types=None,
    ):

        self.ALLOWED_TYPES = (list, tuple)
        if is_type:
            assert is_type in self.ALLOWED_TYPES, ValueError(
                f"Numeric class can only be of type {self.ALLOWED_TYPES} not {is_type}"
            )

        super().__init__(
            default_value=default_value,
            is_type=is_type,
            required=required,
            description=description,
            fn=fn,
            fn_kwargs=fn_kwargs,
        )

        self.homogeneous = homogeneous or None
        self.inner_types = inner_types or None

    def transform(self, cur_value=None):
        if cur_value is not None:
            if not isinstance(cur_value, self.ALLOWED_TYPES) and not isinstance(
                cur_value, bool
            ):
                raise TypeError(
                    f"cur_value ({cur_value}) is not type {self.ALLOWED_TYPES}"
                )
        self.user_in = cur_value
        iv = super().transform(self.user_in)
        if iv:
            if self.inner_types:
                for v in iv:
                    if not isinstance(v, self.inner_types) and not isinstance(
                        cur_value, bool
                    ):
                        raise TypeError(
                            f"cur_value ({v}) is not type {self.inner_types}"
                        )

            if self.homogeneous:
                first_type = type(iv[0])
                for v in iv:
                    if type(v) != first_type:
                        raise ValueError(
                            f"objects are not homogeneous. {v} is type {type(v)}, but {iv[0]} is {first_type}"
                        )

        self.out = iv
        return self.out
