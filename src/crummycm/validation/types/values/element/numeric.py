from crummycm.validation.types.values.base import BaseValue
import operator


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
        bounds_inclusive=None,
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

        self.bounds = bounds
        if bounds_inclusive:
            if not isinstance(bounds_inclusive, tuple):
                raise ValueError(
                    f"`bounds_inclusive` ({bounds_inclusive}) expected to be tuple, not {type(bounds_inclusive)}"
                )
            else:
                if len(bounds_inclusive) != 2:
                    raise ValueError(
                        f"`bounds_inclusive` ({bounds_inclusive}) expected to be len 2, not {len(bounds_inclusive)}"
                    )
            for b in bounds_inclusive:
                if not isinstance(b, bool):
                    raise ValueError(
                        f"`bounds_inclusive` ({bounds_inclusive}), value ({b}) should be type {bool}, not {type(b)}"
                    )
        self.bounds_inclusive = bounds_inclusive

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
                if self.bounds_inclusive:
                    if self.bounds_inclusive[0]:
                        l_op = operator.ge
                    else:
                        l_op = operator.gt
                    if self.bounds_inclusive[1]:
                        r_op = operator.le
                    else:
                        r_op = operator.lt
                else:
                    l_op = operator.gt
                    r_op = operator.lt

                if not r_op(iv, self.bounds[1]):
                    raise ValueError(
                        f"value {cur_value} tranformed by {super()} into {iv} is greater than {self.bounds[1]} (op: {r_op}), description: {self.description}"
                    )

                if not l_op(iv, self.bounds[0]):
                    raise ValueError(
                        f"value {cur_value} tranformed by {super()} into {iv} is less than {self.bounds[0]} (op: {r_op}),, description: {self.description}"
                    )

        self.out = iv
        return self.out
