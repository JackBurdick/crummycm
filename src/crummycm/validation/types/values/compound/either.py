from crummycm.validation.types.values.base import BaseValue


class Either(BaseValue):
    def __init__(
        self,
        default_value=None,
        is_type=None,
        required=None,
        description=None,
        fn=None,
        fn_kwargs=None,
        # specific
        either_seq=None,
        return_type=None,
    ):

        super().__init__(
            default_value=default_value,
            is_type=is_type,
            required=required,
            description=description,
            fn=fn,
            fn_kwargs=fn_kwargs,
        )

        # NOTE: the order of `either_seq` is relevant
        if either_seq is None:
            raise ValueError(f"Either.`either_seq` requires user specified options")
        if not isinstance(either_seq, (list, tuple)):
            raise ValueError(
                f"either_seq must be either type tuple or list, not {type(either_seq)}"
            )
        if len(either_seq) < 2:
            raise ValueError(
                "Either.`either_seq` is for specifying values that could "
                "be one of a set of options, the set of options should be larger than 1"
            )
        for v in either_seq:
            if not isinstance(v, BaseValue):
                raise ValueError(
                    f"value {v} is type {type(v)} and should be an instance of a BaseValue"
                )
            if v.required:
                raise ValueError(
                    f"Cannot specify value in {self.__class__.__name__} as required: ({v}) \n"
                    f"> likely fix: use (required=False) when instantiating {v}"
                )
            # TODO ensure required is not set

        self.either_seq = either_seq

        ACCEPTED_RET_TYPES = {list, str, int, tuple, float}
        if return_type:
            if return_type not in ACCEPTED_RET_TYPES:
                raise ValueError(
                    f"return_type ({return_type}) is not allowed "
                    f"please choose one of {ACCEPTED_RET_TYPES}"
                )

        self.return_type = return_type

    def template(self, level=0):
        # TODO: this will need to be shortened
        inner_temp = [v.template() for v in self.either_seq]
        ret_str = f"[{self.__class__.__name__}: ({inner_temp})]"
        if self.is_type:
            ret_str = f"{self.is_type}{ret_str}"
        if self.default_value:
            ret_str += f"({self.default_value})"
        if self.fn:
            ret_str += "!"
        if self.required:
            ret_str += "*"
        return ret_str

    def transform(self, raw):
        out = None
        for opt in self.either_seq:
            try:
                out = opt.transform(raw)
                break
            except (TypeError, ValueError):
                pass

        if out is None:
            raise ValueError(f"raw value was not transformed by any of the options")

        if self.return_type == list:
            if not isinstance(out, list):
                if isinstance(out, tuple):
                    out = list(out)
                else:
                    out = [out]
        elif self.return_type == tuple:
            if not isinstance(out, tuple):
                if isinstance(out, list):
                    out = tuple(out)
                else:
                    out = (out,)
        elif self.return_type:
            # TODO: additional error needed?
            out = self.return_type(out)

        return out

