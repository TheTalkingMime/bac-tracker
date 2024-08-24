import time
import logging
from functools import wraps
import copy

logger = logging.getLogger(__name__)

def retry_on_exception(exception_types, retries=3, delay=1):
    if isinstance(exception_types, type):
        exception_types = (exception_types,)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mutable_types = (list, dict, set)            
            n = 0
            while n < retries:
                try:
                    original_args = [copy.deepcopy(arg) if isinstance(arg, mutable_types) else arg for arg in args]
                    original_kwargs = {k: copy.deepcopy(v) if isinstance(v, mutable_types) else v for k, v in kwargs.items()}
                    return func(*original_args, **original_kwargs)
                except exception_types as e:
                    n += 1
                    args_str = ", ".join(map(str, args))
                    kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
                    logger.warning(f"{func.__name__}({args_str}, {kwargs_str}) failed on attempt # {n}")
                    time.sleep(delay)
                    if n >= retries:
                        logger.warning(f"Failed after {retries} retries with {delay} second delay. Error: {e}")
                        raise
        return wrapper
    return decorator

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f'Calling function: {func.__name__}')
        result = func(*args, **kwargs)
        logger.debug(f'Function {func.__name__} finished')
        return result
    return wrapper
