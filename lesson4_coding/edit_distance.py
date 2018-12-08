# encoding=utf-8
from functools import wraps


def memo(func):
    buff = {}
    @wraps(func)
    def _wraps(*args, **kwargs):
        str_key = str(args) + str(kwargs)
        if str_key not in buff:
            buff[str_key] = func(*args, **kwargs)
        return buff[str_key]
    return _wraps


@memo
def get_edit_distance(string1, string2):
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)

    return min(
        [get_edit_distance(string1[:-1], string2) + 1,
         get_edit_distance(string1, string2[:-1]) + 1,
         get_edit_distance(string1[:-1], string2[:-1]) + (0 if string1[-1] == string2[-1] else 2)]
    )

print(get_edit_distance('beijing', 'biejgin'))