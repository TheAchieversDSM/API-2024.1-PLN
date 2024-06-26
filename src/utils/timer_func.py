from functools import wraps
from time import perf_counter


def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        elapsed_time_ms = round(((end_time - start_time) * 1000), 2)
        return result, elapsed_time_ms

    return wrapper
