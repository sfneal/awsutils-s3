import os
import unittest

from looptools import Timer

from tests import TEST_PATH, LOCAL_PATH, TestCase


class TestS3List(TestCase):
    target = os.path.join(os.path.dirname(os.path.dirname(__file__)), TEST_PATH)

    @classmethod
    def setUpClass(cls):
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete('dist')

    @Timer.decorator
    def test_s3_list(self):
        s3_files = self.s3.list(TEST_PATH)
        local_files = os.listdir(LOCAL_PATH)
        self.assertEqual(set(s3_files), set(local_files))

    @Timer.decorator
    def test_s3_list_recursive(self):
        s3_files = self.s3.list(recursive=True)
        local_files = ['/'.join(['dist', path]) for path in
                       os.listdir(LOCAL_PATH)]
        self.assertEqual(set(s3_files), set(local_files))


if __name__ == '__main__':
    unittest.main()
