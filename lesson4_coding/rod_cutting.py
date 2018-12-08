# encoding=utf-8
from collections import defaultdict
from functools import wraps

value_list = [1, 3, 10, 20, 30, 39, 40, 50, 60, 30, 40, 80, 85]
value_dict = defaultdict(lambda: -float('inf'))
for n, v in enumerate(value_list):
    value_dict[n + 1] = v
print(value_dict)
result_list = []
solution = {}


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
def revenue(r):
    c, value_sum = max([(0, value_dict[r])] + [(i, revenue(i) + revenue(r - i)) for i in range(1, r)], key=lambda x: x[1])
    solution[r] = (c, r - c)
    return value_sum


# print(revenue(100))
# print(solution)

def show_solution(r, solution):
    left, right = solution[r]
    if left == 0:
        return [right]
    return [left] + show_solution(right, solution)


def pretty_show(r):
    revenue(r)
    return ' + '.join(map(str, show_solution(r, solution)))

print(pretty_show(100))