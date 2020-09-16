# python-stream

[![Build Status](https://travis-ci.com/SelfHacked/python-stream.svg?branch=master)](https://travis-ci.com/SelfHacked/python-stream)
[![Coverage Status](https://coveralls.io/repos/github/SelfHacked/python-stream/badge.svg?branch=master)](https://coveralls.io/github/SelfHacked/python-stream?branch=master)

## Installation

```bash
pip install git+git://github.com/SelfHacked/python-stream.git#egg=python-stream
```


## Usage

### Read file from S3

```python
from stream.io.s3 import S3ReadFile
from stream.functions.bytes import un_gzip 

# Read line by line
with S3ReadFile(bucket='bucket', key='path/to/file.txt.gz', lines=True) as s3_file:
    for line in un_gzip(s3_file):
        print(line)

# Read in chunks
with S3ReadFile(bucket='bucket', key='path/to/file.txt.gz', lines=False) as s3_file:
    while chunk := s3_file.read(10):
        print(chunk)
```

### Upload data to S3

S3WriteFile only uses binary data. Text data should be converted via an encoder before passing to S3WriteFile write methods.

```python
from stream.io.s3 import S3ReadFile
from stream.io.s3 import S3WriteFile

# write data to s3 file.
with S3WriteFile(bucket='bucket', key='path/to/file.txt.gz') as s3_file:
    s3_file.write(b'test\n')
    s3_file.writelines([b'line 1\n', b'line 2\n'])

# read from the s3 file.    
with S3ReadFile(bucket='bucket', key='path/to/file.txt.gz', lines=True) as s3_file:
    for line in s3_file:
        print(line)
```

### Encoding and Decoding

```python
from stream.functions.bytes import encode, decode

text = [f'line {i}' for i in range(0, 10)]

print('Encoded')
encoded = encode(text)
for line in encoded:
    print(f'   {line}')

print('\nDecoded')
decoded = decode(encode(text))
for line in decoded:
    print(f'   {line}')
```


### Example pipeline

```python
import gzip
import csv
from stream.io.s3 import S3ReadFile, S3WriteFile
from stream.functions.bytes import encode, decode

# Read from s3 file
with S3ReadFile('dev-varuna', 'prs/trait1/ss1/data_head.tsv.gz', lines=False) as s3_file:
    # uncompress
    gzip_in = gzip.open(s3_file, 'rb')
    
    # decode
    decode_in = decode(gzip_in)
    
    # parse the csv row
    csv_in = csv.reader(decode_in, delimiter='\t')

    # process step (process step should be in iterable format)
    process = ((line[14], line[12], line[13]) for line in csv_in)
    
    # create tsv lines using a generator
    csv_out = ('\t'.join(line) for line in process)
    
    # add new line
    text_out = (f'{line}\n' for line in csv_out)
    
    # encode text lines into bytes
    encode_out = encode(text_out)
    
    # Write to S3
    with S3WriteFile(
        'dev-varuna', 'prs/trait1/ss1/snps_custom.tsv.gz',
    ) as s3_writer, gzip.open(
        s3_writer, 'wb',
    ) as gzip_out:
        gzip_out.writelines(encode_out)
```
