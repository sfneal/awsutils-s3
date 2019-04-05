import unittest

from looptools import Timer

from awsutils.s3.s3 import url_host, bucket_name, key_extract

URL1 = 'https://hpadesign-projects.s3.amazonaws.com/tests/20160273_fp.1.png'
URL2 = 'https://s3.amazonaws.com/hpadesign-projects/tests/20160273_fp.1.png'
BUCKET_NAME = 'hpadesign-projects'


class TestS3URL(unittest.TestCase):
    @Timer.decorator
    def test_s3url_url_host(self):
        """Extract a URL's host domain."""
        self.assertEqual(url_host(URL1), 'https://hpadesign-projects.s3.amazonaws.com/')
        self.assertEqual(url_host(URL2), 'https://s3.amazonaws.com/')

    @Timer.decorator
    def test_s3url_bucket_name(self):
        """Extract a S3 bucket name from an S3 url."""
        self.assertEqual(bucket_name(URL1), BUCKET_NAME)
        self.assertEqual(bucket_name(URL2), BUCKET_NAME)

    @Timer.decorator
    def test_s3url_key_extract(self):
        """Extract an S3 bucket key from an S3 url."""
        self.assertEqual(key_extract(URL1), 'tests/20160273_fp.1.png')
        self.assertEqual(key_extract(URL2), 'tests/20160273_fp.1.png')


if __name__ == '__main__':
    unittest.main()
