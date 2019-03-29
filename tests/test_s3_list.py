import unittest
import os
from looptools import Timer
from dirutility import DirPaths
from awsutils.s3 import S3


S3_BUCKET = 'awsutils-tests'
TEST_PATH = 'awsutils/s3'
LOCAL_BASE = os.path.dirname(os.path.dirname(__file__))
LOCAL_PATH = os.path.join(LOCAL_BASE, 'awsutils', 's3')


def printer(header, body):
    """Pretty print lists for visual check that correct output was returned."""
    print('\n{0}:\n'.format(header.upper()) + '\n'.join('\t{0}'.format(b) for b in body))


class TestManipulateInsert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_list_buckets(self):
        buckets = self.s3.buckets
        # printer('Available S3 Buckets', buckets)
        self.assertIsInstance(buckets, list)

    @Timer.decorator
    def test_s3_list(self):
        s3_files = self.s3.list(TEST_PATH)
        local_files = os.listdir(LOCAL_PATH)
        # printer('Remote S3 Files', s3_files)
        # printer('Local Files', local_files)
        self.assertEqual(set(s3_files), set(local_files))

    @Timer.decorator
    def test_s3_list_recursive(self):
        s3_files = self.s3.list(recursive=True)
        local_files = [os.path.join('awsutils', path) for path in DirPaths(os.path.join(LOCAL_BASE, 'awsutils')).walk()]
        # printer('Remote S3 Files', s3_files)
        # printer('Local Files', local_files)
        self.assertEqual(set(s3_files), set(local_files))


if __name__ == '__main__':
    unittest.main()
