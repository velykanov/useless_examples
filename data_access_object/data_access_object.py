import json
from functools import partial

from typing import Callable, Dict, List, get_args, get_origin, get_type_hints


def db_connector(get_cursor: Callable) -> Callable:
    def wrapper(klass: Callable) -> Callable:
        def _call_function(func, *args, **kwargs):
            return func(_execute_query, *args, **kwargs)

        def _execute_query(q: str, params: Dict[str, str] = None) -> List:
            cursor = get_cursor()
            q = cursor.mogrify(q, params)
            cursor.execute(q)

            return cursor.fetchall()

        for attr in dir(klass):
            value = getattr(klass, attr)
            if callable(value) and getattr(value, '_dao', False):
                setattr(klass, attr, partial(_call_function, value))

        return klass

    return wrapper


def query(q: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        def inner_wrapper(perform_query: Callable, /, *args, **kwargs):
            annotations: Dict = get_type_hints(func)
            return_value_type = annotations.pop('return', None)
            params = {}

            def _get_type(arg_name):
                type_ = annotations.pop(arg_name)
                origin_type = get_origin(type_)
                if origin_type is None:
                    origin_type = type_

                return origin_type

            def _turn_value_to_type(t, v):
                if t in (int, float, bool):
                    v = json.dumps(v)
                elif t in (set, list, tuple):
                    v = tuple(v)

                return str(v)

            for pos, arg in enumerate(args):
                arg_name: str = func.__code__.co_varnames[pos]
                origin_type = _get_type(arg_name)
                params[arg_name] = _turn_value_to_type(origin_type, arg)

            for kwarg, value in kwargs.items():
                origin_type = _get_type(kwarg)
                params[kwarg] = _turn_value_to_type(origin_type, value)

            result = perform_query(q, params)
            klass = get_args(return_value_type)
            klass = klass[0] if klass else return_value_type

            if result and isinstance(result[0], dict):
                return [klass(**kwargs_) for kwargs_ in result]

            if result:
                return [klass(*args_) for args_ in result]

            return result

        setattr(inner_wrapper, '_dao', True)

        return inner_wrapper

    return wrapper
