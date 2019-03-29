import unittest
import os
from looptools import Timer
from awsutils.s3 import S3


S3_BUCKET = 'awsutils-tests'
TEST_PATH = 'awsutils/s3'
LOCAL_BASE = os.path.dirname(os.path.dirname(__file__))
LOCAL_PATH = os.path.join(LOCAL_BASE, 'awsutils', 's3')


def printer(header, body):
    """Pretty print lists for visual check that correct output was returned."""
    print('\n{0}:\n'.format(header.upper()) + '\n'.join('\t{0}'.format(b) for b in body))


class TestS3Upload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_upload(self):
        target = 'test_s3_upload.py'
        self.s3.upload(os.path.join(LOCAL_BASE, 'tests', target))
        self.assertTrue(target in self.s3.list())

        self.s3.delete(target)
        self.assertFalse(target in self.s3.list())


if __name__ == '__main__':
    unittest.main()
