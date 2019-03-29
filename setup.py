from setuptools import setup, find_packages

extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-cov>=2',
    'pytest-dependency @ https://github.com/SelfHacked/pytest-dependency/archive/master.zip',
]
extra_dev = extra_test

extra_ci = extra_test + [
    'python-coveralls',
]

setup(
    name='python-stream',

    version='dev',

    python_requires='>=3.6',

    extras_require={
        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    packages=find_packages(),

    url='https://github.com/SelfHacked/python-stream',
    author='SelfHacked',
)
