import os
import psutil
from datetime import datetime


def elapsed_since(start):
    return datetime.now() - start


def get_process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = datetime.now()
        result = func(*args, **kwargs)
        elapsed_time = elapsed_since(start)
        mem_after = get_process_memory()
        print(
            "{}: memory before: {:,}, after: {:,}, consumed: {:,}; exec time: {}".format(
                func.__name__,
                mem_before,
                mem_after,
                mem_after - mem_before,
                elapsed_time,
            )
        )
        return result

    return wrapper
