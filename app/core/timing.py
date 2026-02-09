import time
import contextlib
from fastapi import Request


@contextlib.contextmanager
def track_timing(obj, name: str):
    """
    Universal steps timer.

    obj: Request or dict
    name: step name, key "{name}_ms"
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000

        # if obj — Request
        if isinstance(obj, Request):
            if not hasattr(obj.state, "timings"):
                obj.state.timings = {}
            obj.state.timings[f"{name}_ms"] = round(elapsed_ms, 2)
        # if obj — dict
        elif isinstance(obj, dict):
            obj[f"{name}_ms"] = round(elapsed_ms, 2)
        else:
            raise TypeError("track_timing expects Request or dict")
