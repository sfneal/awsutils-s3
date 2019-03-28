import unittest
from looptools import Timer
from awsutils.s3 import S3


S3_BUCKET = 'awsutils-tests'


class TestManipulateInsert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_list_buckets(self):
        print(self.s3.buckets)


if __name__ == '__main__':
    unittest.main()
