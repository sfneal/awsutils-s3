import os
import unittest

from dirutility import DirPaths
from looptools import Timer

from awsutils.s3 import S3
from tests import S3_BUCKET, TEST_PATH, LOCAL_BASE, LOCAL_PATH


class TestS3List(unittest.TestCase):
    s3 = S3(S3_BUCKET)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')

    @Timer.decorator
    def test_s3_list(self):
        s3_files = self.s3.list(TEST_PATH)
        local_files = os.listdir(LOCAL_PATH)
        self.assertEqual(set(s3_files), set(local_files))

    @Timer.decorator
    def test_s3_list_recursive(self):
        s3_files = self.s3.list(recursive=True)
        local_files = [os.path.join('awsutils', path) for path in DirPaths(os.path.join(LOCAL_BASE, 'awsutils')).walk()]
        self.assertEqual(set(s3_files), set(local_files))


if __name__ == '__main__':
    unittest.main()
