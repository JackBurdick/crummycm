from typing import Optional
from crummycm.validation.types.values.base import BaseValue


class Numeric(BaseValue):
    def __init__(
        self,
        default_value=None,
        is_type=None,
        required=None,
        description=None,
        fn=None,
        fn_kwargs=None,
        # specific
        bounds=None,
    ):

        self.ALLOWED_TYPES = (float, int, complex)
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

        self.bounds = bounds or None

    def template(self, level=0):
        ret_str = f"[{self.__class__.__name__}]"
        if self.is_type:
            ret_str = f"{self.is_type}{ret_str}"

        if self.default_value:
            ret_str += f"({self.default_value})"
        if level == 0:
            if self.bounds:
                ret_str += "^"
        elif level > 0:
            if self.bounds:
                ret_str += f"[{self.bounds}]"
        if self.fn:
            ret_str += "!"
        if self.required:
            ret_str += "*"
        return ret_str

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
            if self.bounds:
                # ensure w/in bounds
                if iv > self.bounds[1]:
                    raise ValueError(
                        f"value {cur_value} tranformed by {super()} into {iv} is greater than {self.bounds[1]}, description: {self.description}"
                    )

                if iv < self.bounds[0]:
                    raise ValueError(
                        f"value {cur_value} tranformed by {super()} into {iv} is less than {self.bounds[0]}, description: {self.description}"
                    )

        self.out = iv
        return self.out
