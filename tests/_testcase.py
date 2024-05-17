import unittest
from uuid import uuid4

from awsutils.s3 import S3
from tests._config import S3_BUCKET


class TestCase(unittest.TestCase):
    _bucket = S3_BUCKET + '-' + str(uuid4())
    s3 = S3(_bucket, quiet=True)

    @classmethod
    def setUpClass(cls):
        if cls.s3.bucket_name not in cls.s3.buckets:
            cls.s3.create_bucket()

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete_bucket(force=True)
