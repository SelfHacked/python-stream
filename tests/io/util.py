import pytest


def depends_with(*other_dependencies):
    return pytest.mark.dependency(
        depends=[
            ('session', 'tests/io/test_base.py::test_with'),
            *other_dependencies,
        ]
    )
