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


class TestS3Operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_copy(self):
        target = 'helpers.py'
        self.s3.copy('awsutils/s3/helpers.py', target)
        self.assertTrue(target in self.s3.list())
        self.s3.delete(target)

    @Timer.decorator
    def test_s3_move(self):
        target = 'helpers2.py'
        self.s3.copy('awsutils/s3/helpers.py', 'awsutils/s3/helpers2.py')
        self.assertTrue(target in self.s3.list('awsutils/s3'))

        self.s3.move('awsutils/s3/helpers2.py', target)
        self.s3.delete(target)
        self.assertFalse(target in self.s3.list())

    @Timer.decorator
    def test_s3_delete(self):
        target = 'helpers.py'
        self.s3.copy('awsutils/s3/helpers.py', target)

        self.s3.delete(target)
        self.assertFalse(target in self.s3.list())


if __name__ == '__main__':
    unittest.main()
