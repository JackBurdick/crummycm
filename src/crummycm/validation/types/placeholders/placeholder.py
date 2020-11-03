class Placeholder:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Placeholder) and self.name == other.name

    def __hash__(self):
        # allows to be used as key
        return hash(self.name + f"{__class__}")

    def __str__(self):
        return "[" + str(self.__class__.__name__) + ": " + str(self.__dict__) + "]"


class ValuePlaceholder(Placeholder):
    def __init__(self, name, *, default_value=None):
        if not name:
            raise ValueError("no name was provided for ValuePlaceholder")
        elif not isinstance(name, str):
            raise ValueError(f"name {name} should be type {str}, not {type(name)}")
        super().__init__(name)
        self.default_value = default_value

    def template(self, level=0):
        ret_str = f"[{self.__class__.__name__}]"
        if level == 0:
            pass
        if self.default_value is not None:
            ret_str += f"({self.default_value})"
        if ret_str:
            ret_str += "*"
        return ret_str


class KeyPlaceholder(Placeholder):
    def __init__(
        self,
        name,
        starts_with=None,
        ends_with=None,
        exact=False,
        required=True,
        populate=False,
        multi=False,
    ):
        if not name:
            raise ValueError("no name was provided for KeyPlaceholder")
        elif not isinstance(name, str):
            raise ValueError(f"name {name} should be type {str}, not {type(name)}")
        super().__init__(name)
        assert starts_with is None or ends_with is None, ValueError(
            f"Cannot specify both starts_with=({starts_with}) and ends_with=({ends_with})"
        )
        # qualifier
        self.starts_with = starts_with or None
        self.ends_with = ends_with or None
        self.exact = exact
        self.populate = populate

        # optional
        self.required = required

        # allows many to one relationship
        self.multi = multi

        if self.populate and not self.exact:
            raise ValueError(
                f"{self.__class__.__name__} cannot populate unless `exact` is set"
            )
        if self.populate and self.multi:
            raise ValueError(
                f"{self.__class__.__name__} cannot populate if `multi` is set"
            )
        if self.multi and self.exact:
            raise ValueError(
                f"{str(self.__class__)} is not allowed to be both exact and multi"
            )

    def is_strict(self):
        if self.starts_with or self.ends_with or self.exact:
            return True
        else:
            return False

    def template(self, level=0):
        name = "KPH"
        if self.exact:
            name = self.name
        ret_str = f"[{name}]"
        if level == 0:
            if self.ends_with or self.starts_with:
                ret_str += "^"
        elif level > 0:
            if self.starts_with:
                ret_str += f"(starts_with='{self.starts_with}')"
            if self.ends_with:
                ret_str += f"(ends_with='{self.ends_with}')"
        if self.multi:
            ret_str = f"MULTI:{ret_str}"
        if self.required:
            ret_str += "*"
        if self.populate:
            ret_str = f"@:{ret_str}"
        return ret_str

    def matches(self, user_val):
        if self.starts_with:
            if user_val.startswith(self.starts_with):
                return True
            else:
                return False
        elif self.ends_with:
            if user_val.endswith(self.ends_with):
                return True
            else:
                return False
        elif self.exact:
            if user_val == self.name:
                return True
            else:
                return False
        else:
            return True


def is_KeyPlaceholder(cur_obj):
    try:
        return issubclass(cur_obj, KeyPlaceholder)
    except TypeError:
        return isinstance(cur_obj, KeyPlaceholder)
