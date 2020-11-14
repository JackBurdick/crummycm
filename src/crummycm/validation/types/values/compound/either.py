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
        return_as_type=None,
    ):

        super().__init__(
            default_value=default_value,
            is_type=is_type,
            required=required,
            description=description,
            fn=fn,
            fn_kwargs=fn_kwargs,
        )

        if return_as_type is not None:
            if default_value is not None:
                if not isinstance(default_value, return_as_type):
                    raise ValueError(
                        f"default value ({default_value}) is not the same"
                        f" as the specified return_as_type ({return_as_type})"
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
        v_types = set()
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
            if v.__class__ in v_types:
                raise ValueError(
                    f"value in `either_seq` contains multiple types of {v.__class__.__name__}"
                    " only one instance of each type is allowed. Please modify either_set to contain"
                    " one of the specified type"
                )
            else:
                v_types.add(v.__class__)

        self.either_seq = either_seq

        self.ACCEPTED_SEQ_TYPES = {list, tuple}
        self.ACCEPTED_IND_TYPES = {str, int, float}
        self.ACCEPTED_RET_TYPES = self.ACCEPTED_SEQ_TYPES | self.ACCEPTED_IND_TYPES
        if return_as_type:
            if return_as_type not in self.ACCEPTED_RET_TYPES:
                raise ValueError(
                    f"return_as_type ({return_as_type}) is not allowed "
                    f"please choose one of {self.ACCEPTED_RET_TYPES}"
                )

        self.return_as_type = return_as_type

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
            out = super().transform(raw)

        if out is None:
            raise ValueError(f"raw value was not transformed by any of the options")

        if self.return_as_type:
            # convert from one seq to another
            if isinstance(out, tuple(self.ACCEPTED_SEQ_TYPES)):
                if self.return_as_type in self.ACCEPTED_SEQ_TYPES:
                    out = self.return_as_type(out)
                elif self.return_as_type in self.ACCEPTED_IND_TYPES:
                    # e.g. out = [1,3] and return type = str
                    raise ValueError(
                        f"user is trying to convert a sequence value ({out}, type: {type(out)})"
                        f"into a individual type {self.return_as_type}. this is currently not allowed as"
                        f"the output may be unexpected. e.g. if the user value is ['a','b'], the output would be"
                        f"'['a','b','"
                    )
                else:
                    raise ValueError(
                        f"{self.return_as_type} is not an accepted sequence of individual type"
                    )
            elif isinstance(out, tuple(self.ACCEPTED_IND_TYPES)):
                # out is a indiviual type, e.g. 1, or 1.1, 'some_str'
                if self.return_as_type in self.ACCEPTED_SEQ_TYPES:
                    # return type is a sequence, 'allowed' (as a wrapper) since
                    # it wraps the value. a straight conversion is now allowed
                    # since it may be unexpected. e.g. list("abc") becomes ['a','b','c']
                    if self.return_as_type == list:
                        out = [out]
                    elif self.return_as_type == tuple:
                        out = (out,)
                    else:
                        raise NotImplementedError(
                            f"specified sequence type ({self.return_as_type}) is not implemented"
                        )
                elif self.return_as_type in self.ACCEPTED_IND_TYPES:
                    # return type is an individual type as well
                    try:
                        out = self.return_as_type(out)
                    except ValueError as e:
                        raise ValueError(
                            f"transformed value ({out}) is type {type(out)} and is unable to be"
                            f" converted to type {self.return_as_type}. python error: {e}"
                        )
            else:
                raise ValueError(
                    f"{type(out)} is not an accepted sequence of individual type"
                )

            if self.return_as_type == list:
                if not isinstance(out, list):
                    if isinstance(out, tuple):
                        out = list(out)
                    else:
                        out = [out]
            elif self.return_as_type == tuple:
                if not isinstance(out, tuple):
                    if isinstance(out, list):
                        out = tuple(out)
                    else:
                        out = (out,)
            elif self.return_as_type:
                # TODO: additional error needed?
                out = self.return_as_type(out)

        return out

