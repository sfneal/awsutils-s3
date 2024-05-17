import os
import unittest

from looptools import Timer

from awsutils.s3 import url_validator
from tests import TestCase


class TestS3PreSign(TestCase):
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')
        super().tearDownClass()

    @Timer.decorator
    def test_pre_sign(self):
        self.assertTrue(url_validator(self.s3.pre_sign('awsutils/s3/helpers.py', 10)))

    @Timer.decorator
    def test_bucket_url(self):
        self.assertTrue(url_validator(self.s3.bucket_url))

    @Timer.decorator
    def test_object_url(self):
        self.assertTrue(url_validator(self.s3.url('awsutils/s3/helpers.py')))


if __name__ == '__main__':
    unittest.main()
