import functools
from time import perf_counter


def time_spent(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start_time = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = perf_counter() - start_time
            print(f"time_taken: {elapsed_time}")

    return clocked
