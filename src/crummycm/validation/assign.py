def _get_corresponding_template_keys(spec_in_dict, uk):
    matching_keys = []
    for k in list(spec_in_dict.keys()):
        if getattr(k, "starts_with", False):
            if uk.startswith(k.starts_with):
                if uk not in matching_keys:
                    matching_keys.append(k)
                else:
                    raise ValueError(
                        f"key {uk} matches {k.name} 's attribute starts_with ({k.starts_with})"
                        f" but {matching_keys} also match a template spec and only one can be valid"
                    )
        if getattr(k, "ends_with", False):
            if uk.endswith(k.ends_with):
                if uk not in matching_keys:
                    matching_keys.append(k)
                else:
                    raise ValueError(
                        f"key {uk} matches {k.name} 's attribute ends_with ({k.ends_with}),"
                        f" but {matching_keys} also match a template spec and only one can be valid"
                    )
        if not getattr(k, "ends_with", False) and not getattr(k, "starts_with", False):
            matching_keys.append(k)

    if len(matching_keys) == 0:
        raise ValueError(
            f"no user keys found to match the specified keys in {spec_in_dict}"
        )
    # elif len(matching_keys) > 1:
    #     raise ValueError(
    #         f"user keys: {matching_keys} match multiple spec keys {spec_in_dict}"
    #     )

    return matching_keys


def _eliminate_single_keys(options_dict, uk_to_sk, used_keys):
    tmp_dict = {}
    for kk, vv in options_dict.items():
        if len(vv) == 1:
            cur_v = vv[0]
            if cur_v in used_keys:
                if cur_v.multi:
                    pass
                else:
                    raise ValueError(
                        f"key {cur_v.name} matches multiple items: {[v.name for v in list(used_keys)]}"
                    )
            else:
                used_keys.add(cur_v)
                uk_to_sk[kk] = cur_v
        else:
            tmp_dict[kk] = vv
    print(tmp_dict)

    return tmp_dict


def _remove_used_options(tmp_dict, used_keys):
    for k, v in tmp_dict.items():
        new_options = []
        for vv in v:
            if vv not in used_keys:
                new_options.append(vv)
        tmp_dict[k] = new_options

    return tmp_dict


def _assign_keys(options_dict, uk_to_sk, used_keys):
    # eliminate single
    # used_keys and uk_to_sk are modified in place

    tmp_dict = _eliminate_single_keys(options_dict, uk_to_sk, used_keys)
    if len(tmp_dict) > 0:
        print("hi")
        # remove used keys from options
        tmp_dict = _remove_used_options(tmp_dict, used_keys)
        uk_to_sk, tmp_dict = _assign_keys(tmp_dict, uk_to_sk, used_keys)

    return uk_to_sk, tmp_dict


def _assign_multi_keys(uk_to_sk, tmp_dict):
    print(f"assign_multi: {tmp_dict}")
    return uk_to_sk, tmp_dict


def map_user_keys_to_spec_key(raw, spec_in_dict):

    # create initial options
    options_dict = {}
    for uk in raw.keys():
        options_dict[uk] = _get_corresponding_template_keys(spec_in_dict, uk)

    # eliminate and assign
    used_keys = set()
    uk_to_sk = {}
    uk_to_sk, tmp_dict = _assign_keys(options_dict, uk_to_sk, used_keys)
    if len(tmp_dict) > 0:
        uk_to_sk, tmp_dict = _assign_multi_keys(uk_to_sk, tmp_dict)
    assert len(tmp_dict) == 0, ValueError(f"keys remain unassigned: {tmp_dict}")

    return uk_to_sk
