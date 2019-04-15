import os
import unittest

from dirutility import DirPaths
from looptools import Timer

from awsutils.s3 import S3
from tests import S3_BUCKET, LOCAL_BASE


class TestS3Transfer(unittest.TestCase):
    s3 = S3(S3_BUCKET)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')

    def setUp(self):
        self.test_path = None
        self.delete_path = None

    def tearDown(self):
        if self.test_path:
            self.s3.delete(self.test_path)
        if self.delete_path and os.path.isfile(self.delete_path):
            os.remove(self.test_path)

    @Timer.decorator
    def test_upload(self):
        self.test_path = 'test_s3_transfer.py'
        self.s3.upload(os.path.join(LOCAL_BASE, 'tests', self.test_path))
        self.assertTrue(self.test_path in self.s3.list())

    @Timer.decorator
    def test_download(self):
        self.test_path = 'commands.py'
        self.delete_path = 'commands.py'
        self.s3.download('awsutils/s3/commands.py', quiet=False)
        self.assertTrue(os.path.isfile(self.test_path))


class TestS3Sync(unittest.TestCase):
    s3 = S3(S3_BUCKET)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')

    def setUp(self):
        self.test_path = None
        self.delete_path = None

    @Timer.decorator
    def test_sync(self):
        target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
        self.s3.sync(target, quiet=True)

        self.assertEqual(set(self.s3.list(recursive=True)),
                         set([os.path.join('awsutils', path)
                              for path in DirPaths(os.path.join(LOCAL_BASE, 'awsutils')).walk()]))


if __name__ == '__main__':
    unittest.main()
