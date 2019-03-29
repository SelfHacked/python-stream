from stream.functions.control import (
    preload as _preload,
)
from . import from_function

preload = from_function(_preload, has_params=True)
