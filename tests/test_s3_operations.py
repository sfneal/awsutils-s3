import os
import unittest

from looptools import Timer

from awsutils.s3 import S3
from tests import S3_BUCKET


class TestS3Copy(unittest.TestCase):
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

    def tearDown(self):
        if self.test_path:
            self.s3.delete(self.test_path)

    @Timer.decorator
    def test_file(self):
        self.test_path = 'helpers.py'
        self.s3.copy('awsutils/s3/helpers.py', self.test_path)
        self.assertTrue(self.test_path in self.s3.list())

    @Timer.decorator
    def test_directory(self):
        self.test_path = 's4'
        print(self.s3.exists('awsutils/s3'))
        self.s3.copy('awsutils/s3', self.test_path, quiet=False)
        print(self.s3.list())
        self.assertTrue(self.test_path in self.s3.list())


class TestS3Exists(unittest.TestCase):
    s3 = S3(S3_BUCKET)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete(cls.target)

    @Timer.decorator
    def test_file(self):
        self.assertTrue(self.s3.exists('awsutils/s3/helpers.py'))

    @Timer.decorator
    def test_directory(self):
        self.assertTrue(self.s3.exists('awsutils/s3'))

    @Timer.decorator
    def test_directory_not(self):
        self.assertFalse(self.s3.exists('awsutils/s4'))


class TestS3Move(unittest.TestCase):
    s3 = S3(S3_BUCKET)

    @classmethod
    def setUpClass(cls):
        cls.s3.copy('awsutils/s3/helpers.py', 'awsutils/s3/helpers2.py')

    def setUp(self):
        self.test_file = None

    def tearDown(self):
        if self.test_file:
            self.s3.delete(self.test_file)

    @Timer.decorator
    def test_file(self):
        self.test_file = 'helpers2.py'

        self.s3.move('awsutils/s3/helpers2.py', self.test_file)
        self.assertTrue(self.test_file in self.s3.list())


class TestS3Delete(unittest.TestCase):
    s3 = S3(S3_BUCKET)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
    file = 'awsutils/s3/helpers.py'
    directory = ''

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)
        # cls.s3.copy('awsutils/s3', 'awsutils/s4')

    @Timer.decorator
    def test_file(self):
        self.s3.delete(self.file)
        self.assertFalse(self.file in self.s3.list(os.path.dirname(self.file)))


if __name__ == '__main__':
    unittest.main()
