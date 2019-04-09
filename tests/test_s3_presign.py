import os
import unittest

from looptools import Timer

from awsutils.s3 import S3, url_validator
from tests import S3_BUCKET


class TestS3PreSign(unittest.TestCase):
    s3 = S3(S3_BUCKET)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')

    @Timer.decorator
    def test_pre_sign(self):
        sign = self.s3.pre_sign('awsutils/s3/helpers.py', 10)
        self.assertTrue(url_validator(sign))


if __name__ == '__main__':
    unittest.main()
