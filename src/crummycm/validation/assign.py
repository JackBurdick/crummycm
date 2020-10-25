from collections import Counter


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

    return matching_keys


def _eliminate_single_keys(opt_dict, uk_to_sk, used_keys):
    unsolved_opt_dict, unsolved_m_opt_dict = {}, {}
    for uk, sks in opt_dict.items():
        if len(sks) == 1:
            sk = sks[0]
            if sk.multi:
                unsolved_m_opt_dict[uk] = sk
            else:
                if sk in used_keys:
                    raise ValueError(
                        f"key {sk.name} matches multiple items: {[v.name for v in list(used_keys)]}"
                    )
                else:
                    used_keys.add(sk)
                    uk_to_sk[uk] = sk
        else:
            # multiple specs might match the user value, but we will match the
            # user value to the stricter of the definitions. That is, if the
            # user key is `my_val` and one is a generic placeholder and the other
            # calls for ends_with=`_val` we will assign to the ends with
            stricter = []
            for sk in sks:
                if sk.starts_with or sk.ends_with:
                    stricter.append(sk)

            if len(stricter) == 1:
                sk = stricter[0]
                if sk.multi:
                    unsolved_m_opt_dict[uk] = sk
                else:
                    if sk in used_keys:
                        raise ValueError(
                            f"key {sk.name} matches multiple items: {[v.name for v in list(used_keys)]}"
                        )
                    else:
                        used_keys.add(sk)
                        uk_to_sk[uk] = sk
            else:
                unsolved_opt_dict[uk] = sks

    return unsolved_opt_dict, unsolved_m_opt_dict


def _remove_used_options(unsolved_opt_dict, used_keys):
    for k, v in unsolved_opt_dict.items():
        new_options = []
        for vv in v:
            if vv not in used_keys:
                new_options.append(vv)
        unsolved_opt_dict[k] = new_options

    return unsolved_opt_dict


def _assign_multi_keys(unsolved_m_opt_dict, uk_to_sk):
    sk_to_uks = {}
    c = Counter()
    # reverse dict
    for k, v in unsolved_m_opt_dict.items():
        try:
            sk_to_uks[v].append(k)
        except KeyError:
            sk_to_uks[v] = [k]
        c[k] += 1

    # ensure no overlap
    errs = []
    for uk, uk_count in c.items():
        if uk_count > 1:
            errs.append((uk, uk_count))
    if errs:
        err_str = ""
        for t in errs:
            uk, uk_count = t
            err_str += f" - {uk} used {uk_count} times: {unsolved_m_opt_dict[uk]}\n"
        raise ValueError(
            f"the following keys cannot be discerned as they match multiple template keys:\n{err_str}"
        )

    for sk, uks in sk_to_uks.items():
        for uk in uks:
            uk_to_sk[uk] = sk

    return uk_to_sk


def _assign_keys(opt_dict, uk_to_sk, used_keys):
    # this function is ..tricky.. I don't trust that I've implemented this
    # correctly yet

    # eliminate single
    unsolved_opt_dict, unsolved_m_opt_dict = _eliminate_single_keys(
        opt_dict, uk_to_sk, used_keys
    )
    if len(unsolved_opt_dict) > 0:
        # remove used keys from options
        unsolved_opt_dict = _remove_used_options(unsolved_opt_dict, used_keys)
        uk_to_sk, unsolved_opt_dict = _assign_keys(
            unsolved_opt_dict, uk_to_sk, used_keys
        )

    # this block may belong above the _remove_used_options(unsolved_opt_dict,
    # used_keys) to help eliminate additional keys?
    if len(unsolved_m_opt_dict) > 0:
        uk_to_sk = _assign_multi_keys(unsolved_m_opt_dict, uk_to_sk)

    return uk_to_sk, unsolved_opt_dict


def map_user_keys_to_spec_key(raw, spec_in_dict):

    # create initial options
    opt_dict = {}
    for uk in raw.keys():
        opt_dict[uk] = _get_corresponding_template_keys(spec_in_dict, uk)

    # eliminate and assign
    uk_to_sk, used_keys = {}, set()
    uk_to_sk, unsolved_opt_dict = _assign_keys(opt_dict, uk_to_sk, used_keys)

    assert len(unsolved_opt_dict) == 0, ValueError(
        f"keys remain unassigned: {unsolved_opt_dict}"
    )

    return uk_to_sk
