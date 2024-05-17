import unittest

from looptools import Timer

from tests import TestCase


class TestS3Buckets(TestCase):
    @Timer.decorator
    def test_list_buckets(self):
        buckets = self.s3.buckets
        self.assertIsInstance(buckets, list)


class TestS3BucketCreate(TestCase):
    @classmethod
    def setUpClass(cls):
        if cls.s3.bucket_name in cls.s3.buckets:
            cls.s3.delete_bucket(force=True)

    @Timer.decorator
    def test_create(self):
        self.s3.create_bucket()
        self.assertTrue(self.s3.bucket_name in self.s3.buckets)


class TestS3BucketDelete(TestCase):
    @Timer.decorator
    def test_delete(self):
        self.s3.delete_bucket(force=True)
        self.assertFalse(self.s3.bucket_name in self.s3.buckets)

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
