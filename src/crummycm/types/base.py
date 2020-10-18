import inspect


class Base:
    def __init__(
        self,
        default_value=None,
        is_type=None,
        required=None,
        description=None,
        fn=None,
        fn_kwargs=None,
    ):
        # assigned in outter loop
        self.default_value = default_value or None

        # ran in transform
        self.required = required or True
        self.is_type = is_type or None
        self.fn = fn or None
        self.fn_kwargs = fn_kwargs or None

        if description is None:
            self.description = "The description for this entry hasn't been written yet"
        else:
            self.description = description

    def _mandatory_exists(self, raw):
        if self.required:
            if raw is None:
                raise ValueError(f"variable is required but not specified")

    def _check_type(self, raw):
        if self.is_type:
            if not isinstance(raw, self.is_type):
                # ints can be converted to floats, but the opposite isn't true
                if issubclass(self.is_type, float):
                    if isinstance(raw, int):
                        return float(raw)
                raise TypeError(
                    f"specified value {raw} is type {type(raw)}, not {self.is_type}"
                )
        return raw

    def _apply_fn(self, raw):
        try:
            if self.fn_kwargs:
                try:
                    temp = self.fn(raw, **self.fn_kwargs)
                except TypeError as err:
                    if not set(self.fn_kwargs.keys()).issubset(
                        inspect.getfullargspec(self.fn).args
                    ):
                        raise (
                            ValueError(
                                f"the parameters passed ({self.fn_kwargs.keys()})"
                                f" are not a subset of the function ({inspect.getfullargspec(self.fn).args})"
                            )
                        )
                    raise TypeError(err)
            else:
                temp = self.fn(raw)
        except TypeError:
            temp = raw

        return temp

    def transform(self, raw):
        self._mandatory_exists(raw)
        intermediate = self._check_type(raw)
        intermediate = self._apply_fn(intermediate)
        out = intermediate
        return out

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
