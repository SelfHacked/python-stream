from setuptools import setup, find_packages

extra_s3 = [
    'boto3>=1.9',
    'botocore',
]
extra_all = extra_s3

extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-cov>=2',
    'pytest-dependency @ https://github.com/SelfHacked/pytest-dependency/archive/master.zip',
    'cached-property',
]
extra_dev = extra_all + extra_test

extra_ci = extra_test + [
    'python-coveralls',
]

setup(
    name='python-stream',

    version='dev',

    python_requires='>=3.6',

    install_requires=[
        'returns-decorator',
        'gimme-cached-property',
    ],

    extras_require={
        's3': extra_s3,

        'all': extra_all,

        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    packages=find_packages(),

    url='https://github.com/SelfHacked/python-stream',
    author='SelfHacked',

    entry_points={
        'console_scripts': [
            's3-upload=stream.io.s3:upload_cmd',
            's3-download=stream.io.s3:download_cmd',
            's3-get=stream.io.s3:get_cmd',
            's3-copy=stream.io.s3:copy_cmd',
        ],
    },
)
