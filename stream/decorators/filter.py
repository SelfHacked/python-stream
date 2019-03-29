from stream.functions.filter import (
    filter_ as _filter,
    remove_empty as _remove_empty,
)
from . import from_function

filter_ = from_function(_filter, has_params=True)
remove_empty = from_function(_remove_empty, has_params=False)
