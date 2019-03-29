from functools import wraps

from stream.typing import Function


class from_function(object):
    """
    Change a iterator function to a generator decorator
    """

    def __init__(self, func: Function, *, has_params: bool):
        self.__doc__ = func.__doc__
        self.__has_params = has_params

        class __new_func(object):
            def __init__(self, *args, **kwargs):
                if has_params:
                    self.__f = func(*args, **kwargs)
                else:
                    self.__f = func

            def __call__(self, gen):
                @wraps(gen)
                def __new_gen(*args, **kwargs):
                    return self.__f(gen(*args, **kwargs))

                return __new_gen

        self.__new_func = __new_func

    def __call__(self, *args, **kwargs):
        if self.__has_params:
            return self.__new_func(*args, **kwargs)
        else:
            return self.__new_func()(args[0])
