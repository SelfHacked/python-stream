from stream.functions.control import (
    preload as _preload,
)
from . import (
    from_function as _from_function,
)

preload = _from_function(_preload, has_params=True)
