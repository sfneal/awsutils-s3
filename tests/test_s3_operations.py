import os
import unittest

from looptools import Timer

from awsutils.s3 import S3
from tests import S3_BUCKET


class TestS3Copy(unittest.TestCase):
    s3 = S3(S3_BUCKET, quiet=True)
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
        self.test_path = 'commands.py'
        self.s3.copy('awsutils/s3/commands.py', self.test_path)
        self.assertTrue(self.test_path in self.s3.list())

    @Timer.decorator
    def test_directory(self):
        self.test_path = 's4/'
        self.s3.copy('awsutils/s3', self.test_path)
        self.assertTrue(self.test_path in self.s3.list())


class TestS3Exists(unittest.TestCase):
    s3 = S3(S3_BUCKET, quiet=True)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils/')

    @Timer.decorator
    def test_file(self):
        self.assertTrue(self.s3.exists('awsutils/s3/commands.py'))

    @Timer.decorator
    def test_directory(self):
        self.assertTrue(self.s3.exists('awsutils/s3'))

    @Timer.decorator
    def test_directory_not(self):
        self.assertFalse(self.s3.exists('awsutils/s4'))


class TestS3Move(unittest.TestCase):
    s3 = S3(S3_BUCKET, quiet=True)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)
        cls.s3.copy('awsutils/s3/commands.py', 'awsutils/commands2.py')

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils/')

    def setUp(self):
        self.path = None

    def tearDown(self):
        if self.path:
            self.s3.delete(self.path)

    @Timer.decorator
    def test_file(self):
        self.path = 'commands2.py'
        self.s3.move('awsutils/commands2.py', self.path)

        # Assert file is in new location
        self.assertTrue(self.path in self.s3.list())

        # Assert file is NOT in old location
        self.assertFalse(self.path in self.s3.list('awsutils'))

    @Timer.decorator
    def test_directory(self):
        self.path = 's5/'
        self.s3.move('awsutils/s3/', self.path)

        # Assert file is in new location
        self.assertTrue(self.path in self.s3.list())


class TestS3Delete(unittest.TestCase):
    s3 = S3(S3_BUCKET, quiet=True)
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
    file = 'awsutils/s3/commands.py'
    directory1 = 'awsutils/s4/'
    directory2 = 'awsutils/s5/'

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)
        cls.s3.copy('awsutils/s3/', cls.directory1)
        cls.s3.copy('awsutils/s3/', cls.directory2)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('awsutils/')

    @Timer.decorator
    def test_file(self):
        self.s3.delete(self.file)
        self.assertFalse(self.file in self.s3.list(os.path.dirname(self.file)))

    @Timer.decorator
    def test_directory(self):
        self.s3.delete(self.directory1)
        self.assertFalse('s4/' in self.s3.list('awsutils'))

    @Timer.decorator
    def test_directory_exclude(self):
        self.s3.delete(self.directory2, exclude='_*')
        self.assertTrue('__init__.py' in self.s3.list('awsutils/s5'))
        self.assertTrue('_version.py' in self.s3.list('awsutils/s5'))
        self.assertFalse('s3.py' in self.s3.list('awsutils/s5'))


if __name__ == '__main__':
    unittest.main()
