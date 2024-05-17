import unittest
from uuid import uuid4

from awsutils.s3 import S3
from tests._config import S3_BUCKET


class TestCase(unittest.TestCase):
    _bucket = S3_BUCKET + '-' + str(uuid4())
    s3 = S3(_bucket, quiet=True)
