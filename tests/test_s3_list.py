import unittest
from looptools import Timer
from awsutils.s3 import S3


S3_BUCKET = 'awsutils-tests'


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
        self.assertIsInstance(buckets, list)
        printer('Available S3 Buckets', buckets)


if __name__ == '__main__':
    unittest.main()
