import os


S3_BUCKET = 'py-awsutils-tests'
TEST_PATH = 'data'
LOCAL_BASE = os.path.dirname(os.path.dirname(__file__))
LOCAL_PATH = os.path.join(LOCAL_BASE, TEST_PATH)
