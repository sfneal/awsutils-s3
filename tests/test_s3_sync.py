import unittest
import os
from looptools import Timer
from dirutility import DirPaths
from awsutils.s3 import S3


S3_BUCKET = 'awsutils-tests'
TEST_PATH = 'awsutils/s3'
LOCAL_BASE = os.path.dirname(os.path.dirname(__file__))
LOCAL_PATH = os.path.join(LOCAL_BASE, 'awsutils', 's3')


class TestManipulateInsert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_sync(self):
        target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
        self.s3.sync(target)

        s3_files = self.s3.list(recursive=True)
        local_files = [os.path.join('awsutils', path) for path in DirPaths(os.path.join(LOCAL_BASE, 'awsutils')).walk()]
        # printer('Remote S3 Files', s3_files)
        # printer('Local Files', local_files)
        self.assertEqual(set(s3_files), set(local_files))


if __name__ == '__main__':
    unittest.main()
