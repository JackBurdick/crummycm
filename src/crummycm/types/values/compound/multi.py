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
        element_types=None,
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
        self.element_types = element_types or None

        if self.homogeneous:
            # TODO: this is a pretty poor check
            print(type(self.element_types))
            if type(self.element_types) in (list, tuple):
                raise ValueError(
                    f"cannot specify element_types as {self.element_types} and set homogeneous"
                )

    def transform(self, cur_value=None):
        if cur_value is not None:
            if not isinstance(cur_value, self.ALLOWED_TYPES) and not isinstance(
                cur_value, bool
            ):
                raise TypeError(
                    f"cur_value ({cur_value}) is not type {self.ALLOWED_TYPES}"
                )
        self.user_in = cur_value
        # TODO: I'm not sure what is more nature, doing the transform, then the
        # lower/upper ect. or reverse (as it is now)
        iv = super().transform(self.user_in)
        if iv:
            if self.element_types:
                if isinstance(self.element_types, (list, tuple)):
                    for cv in iv:
                        if not any([isinstance(cv, it) for it in self.element_types]):
                            raise TypeError(f"{cv} is not in {self.element_types}")
                else:
                    if isinstance(self.element_types, BaseValue):
                        # `.transform()` each value
                        nv = [self.element_types.transform(cv) for cv in iv]
                        if self.is_type:
                            # in this case convert the list to the other type
                            # (currently a list or tuple)
                            iv = self.is_type(nv)
                        else:
                            iv = nv
                    else:
                        for cv in iv:
                            if not isinstance(cv, self.element_types):
                                raise TypeError(f"{cv} is not in {self.element_types}")

            if self.homogeneous:
                first_type = type(iv[0])
                for v in iv:
                    if type(v) != first_type:
                        raise ValueError(
                            f"objects are not homogeneous. {v} is type {type(v)}, but {iv[0]} is {first_type}"
                        )

        self.out = iv
        return self.out
