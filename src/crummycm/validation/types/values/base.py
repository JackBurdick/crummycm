import inspect


class BaseValue:
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
        self.default_value = default_value if default_value is not None else None

        # ran in transform
        self.required = True if required is None else required

        if not self.required and self.default_value:
            raise ValueError(
                f"Value is not specified as required, but does include a default_value {self.default_value}\n"
                "please either:\n"
                "i) set as required\n"
                "i) remove the default value\n"
                "------\n"
                "if these do not solve the issue, you may wish to make the Key optional\n"
                "e.g. `{KeyPlaceholder(required=False): <this value>`}"
            )

        self.is_type = is_type or None
        self.fn = fn or None
        self.fn_kwargs = fn_kwargs or None

        if description is None:
            self.description = "The description for this entry hasn't been written yet"
        else:
            self.description = description

    def _set_init(self, raw):
        self.user_in = raw
        cur_val = raw
        if raw is None:
            if self.default_value is not None:
                cur_val = self.default_value
        return cur_val

    def _mandatory_exists(self, raw):
        if self.required:
            if raw is None:
                raise ValueError(f"variable is required but not specified")

    def _check_type(self, raw):
        # NOTE: None is passed through
        if raw:
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
            # TODO: when debugging, print errors
            temp = raw

        return temp

    def transform(self, raw):
        # init
        cur_val = self._set_init(raw)
        # checks
        self._mandatory_exists(cur_val)
        # tranform
        intermediate = self._check_type(cur_val)
        intermediate = self._apply_fn(intermediate)
        self.out = intermediate
        return self.out

    def __str__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)
