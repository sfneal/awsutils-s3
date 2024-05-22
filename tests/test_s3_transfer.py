import os
import shutil
import unittest

import dirutility
from dirutility import DirPaths, SystemCommand
from looptools import Timer

from awsutils.s3 import S3
from tests import TestCase, LOCAL_BASE


class TestS3Transfer(TestCase):
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not os.path.exists('s3'):
            os.mkdir('s3')
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')
        super().tearDownClass()

    def setUp(self):
        self.test_path = None
        self.delete_path = None

    def tearDown(self):
        if self.test_path:
            self.s3.delete(self.test_path)
        if self.delete_path:
            if os.path.isfile(self.delete_path):
                os.remove(self.test_path)
            elif os.path.isdir(self.delete_path):
                shutil.rmtree(self.test_path)

    @Timer.decorator
    def test_acceleration(self):
        self.assertTrue(self.s3.is_acceleration_enabled())

    @Timer.decorator
    def test_upload(self):
        self.test_path = 'test_s3_transfer.py'
        self.s3.upload(os.path.join(LOCAL_BASE, 'tests', self.test_path))
        self.assertTrue(self.test_path in self.s3.list())

    @Timer.decorator
    def test_upload_cli(self):
        self.test_path = 'test_s3_transfer.py'

        SystemCommand("awss3 upload --bucket {bucket} --local_path {local_path} --remote_path {remote_path}".format(
            bucket=self.s3.bucket_name,
            local_path=os.path.join(LOCAL_BASE, 'tests', self.test_path),
            remote_path='test_s3_transfer.py'
        ))

        self.assertTrue(self.test_path in self.s3.list())

    @Timer.decorator
    def test_download_file(self):
        self.test_path = 'commands.py'
        self.delete_path = 'commands.py'
        self.s3.download('awsutils/s3/commands.py')
        self.assertTrue(os.path.isfile(self.test_path))

    @Timer.decorator
    def test_download_file_cli(self):
        self.test_path = 'commands.py'
        self.delete_path = 'commands.py'

        SystemCommand("awss3 download --bucket {bucket} --local_path {local_path} --remote_path {remote_path}".format(
            bucket=self.s3.bucket_name,
            local_path='commands.py',
            remote_path='awsutils/s3/commands.py'
        ))

        self.assertTrue(os.path.isfile(self.test_path))

    @Timer.decorator
    def test_download_folder(self):
        self.test_path = os.path.join(os.path.dirname(__file__), 's3')
        self.delete_path = os.path.join(os.path.dirname(__file__), 's3')
        self.s3.download('awsutils/s3', self.test_path, recursive=True)
        self.assertTrue(os.path.isdir(self.test_path))


class TestS3Sync(TestCase):
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils')
        super().tearDownClass()

    def setUp(self):
        self.test_path = None
        self.delete_path = None

    @Timer.decorator
    def test_sync(self):
        target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
        self.s3.sync(target, quiet=True)

        self.assertEqual(set(self.s3.list(recursive=True)),
                         set([os.path.join('awsutils', path).replace('\\', '/')
                              for path in DirPaths(os.path.join(LOCAL_BASE, 'awsutils')).walk()]))


if __name__ == '__main__':
    unittest.main()
