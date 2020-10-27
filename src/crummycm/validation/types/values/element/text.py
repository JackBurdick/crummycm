from crummycm.validation.types.values.base import BaseValue


class Text(BaseValue):
    def __init__(
        self,
        default_value=None,
        is_type=str,  # by default
        required=None,
        description=None,
        fn=None,
        fn_kwargs=None,
        # specific
        to_lower=False,
        is_in_list=None,
        contains=None,
        contains_one_of=None,
        starts_with=None,
        ends_with=None,
    ):

        self.ALLOWED_TYPES = (str,)
        assert is_type in self.ALLOWED_TYPES, ValueError(
            f"Text class can only be of type {self.ALLOWED_TYPES} not {is_type}"
        )

        super().__init__(
            default_value=default_value,
            is_type=is_type,
            required=required,
            description=description,
            fn=fn,
            fn_kwargs=fn_kwargs,
        )

        self.is_in_list = is_in_list or None
        self.to_lower = to_lower
        self.contains = contains or None
        if contains_one_of:
            if not hasattr(contains_one_of, "__iter__"):
                raise ValueError(f"{contains_one_of} is not iterable")
        self.contains_one_of = contains_one_of or None
        self.starts_with = starts_with or None
        self.ends_with = ends_with or None

    def transform(self, cur_value=None):
        if cur_value is not None:
            if not isinstance(cur_value, self.ALLOWED_TYPES):
                raise TypeError(
                    f"cur_value ({cur_value}) is not type {self.ALLOWED_TYPES}"
                )
        self.user_in = cur_value
        iv = super().transform(self.user_in)
        if iv:
            if self.is_in_list:
                if not iv in self.is_in_list:
                    raise ValueError(f"{iv} is not in {self.is_in_list}")
            if self.to_lower:
                iv = iv.lower()
            if self.contains:
                # contains all of
                if hasattr(self.contains, "__iter__"):
                    for v in self.contains:
                        if v not in iv:
                            raise ValueError(f"{v} of {self.contains} not in {iv}")
                else:
                    if not self.contains in iv:
                        raise ValueError(f"{self.contains} is not in {iv}")
            if self.contains_one_of:
                if hasattr(self.contains_one_of, "__iter__"):
                    if not any([i in iv for i in self.contains_one_of]):
                        raise ValueError(
                            f"{iv} does not contain one of {self.contains_one_of}"
                        )
            if self.starts_with:
                if not iv.startswith(self.starts_with):
                    raise ValueError(f"{iv} does not start with {self.starts_with}")
            if self.ends_with:
                if not iv.endswith(self.ends_with):
                    raise ValueError(f"{iv} does not end with {self.ends_with}")

        self.out = iv
        return self.out
