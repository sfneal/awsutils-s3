# https://docs.aws.amazon.com/cli/latest/reference/s3/
import os
from subprocess import Popen, PIPE
from awsutils.s3._constants import ACL, TRANSFER_MODES
from awsutils.s3.helpers import S3Helpers
from awsutils.s3.commands import S3Commands


def bucket_uri(bucket):
    """Convert a S3 bucket name string in to a S3 bucket uri."""
    return 's3://{bucket}'.format(bucket=bucket)


def system_cmd(cmd, decode_output=True):
    """
    Execute a system command.

    When decode_output is True, console output is captured, decoded
    and returned in list a list of strings.

    :param cmd: Command to execute
    :param decode_output: Optionally capture and decode console output
    :return: List of output strings
    """
    if decode_output:
        # Capture and decode system output
        with Popen(cmd, shell=True, stdout=PIPE) as process:
            return [i.decode("utf-8").strip() for i in process.stdout]
    else:
        os.system(cmd)
        return True


class S3(S3Helpers):
    def __init__(self, bucket_name, transfer_mode='auto', chunk_size=5, multipart_threshold=10):
        """
        AWS CLI S3 wrapper.

        :param bucket_name: S3 bucket name
        :param transfer_mode: Upload/download mode
        :param chunk_size: Size of chunk in multipart upload in MB
        :param multipart_threshold: Minimum size in MB to upload using multipart.
        """
        assert transfer_mode in TRANSFER_MODES, "ERROR: Invalid 'transfer_mode' value."
        assert chunk_size > 4, "ERROR: Chunk size minimum is 5MB."

        self.bucket_name = bucket_name
        S3Helpers.__init__(self, transfer_mode, chunk_size, multipart_threshold)
        self.cmd = S3Commands()

    @property
    def bucket_uri(self):
        """Retrieve a S3 bucket name in URI form."""
        return bucket_uri(self.bucket_name)

    @property
    def buckets(self):
        """
        List all available S3 buckets.

        Execute the `aws s3 ls` command and decode the output
        """
        return [out.rsplit(' ', 1)[-1] for out in system_cmd(self.cmd.list())]

    def sync(self, local_path, remote_path=None, delete=False, acl='private'):
        """
        Synchronize local files with an S3 bucket.

        S3 sync only copies missing or outdated files or objects between
        the source and target.  However, you can also supply the --delete
        option to remove files or objects from the target that are not
        present in the source.

        :param local_path: Local source directory
        :param remote_path: Destination directory (relative to bucket root)
        :param delete: Sync with deletion, disabled by default
        :param acl: Access permissions, must be either 'private', 'public-read' or 'public-read-write'
        """
        assert acl in ACL, "ERROR: Invalid ACL parameter ({0})".format(', '.join("'{0}'".format(i) for i in ACL))
        system_cmd(self.cmd.sync(local_path, '{0}/{1}'.format(self.bucket_uri, remote_path), delete, acl), False)

    def upload(self, local_path, remote_path):
        """
        Upload a local file to an S3 bucket.

        :param local_path: Path to file on local disk
        :param remote_path: S3 key, aka remote path relative to S3 bucket's root
        """
        pass

    def download(self, local_path, remote_path):
        """
        Download a file or folder from an S3 bucket.

        :param local_path: Path to file on local disk
        :param remote_path: S3 key, aka remote path relative to S3 bucket's root
        """
        pass

    def copy(self, src_path, dst_path, dst_bucket=None, recursive=False, include=None, exclude=None):
        """
        Copy an S3 file or folder to another

        :param src_path: Path to source file or folder in S3 bucket
        :param dst_path: Path to destination file or folder
        :param dst_bucket: Bucket to copy to, defaults to same bucket
        :param recursive: Recursively copy all files within the directory
        :param include: Don't exclude files or objects in the command that match the specified pattern
        :param exclude: Exclude all files or objects from the command that matches the specified pattern

        More on inclusion and exclusion parameters...
        http://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters
        """
        uri1 = '{uri}/{src}'.format(uri=self.bucket_uri, src=src_path)
        uri2 = '{uri}/{dst}'.format(uri=bucket_uri(dst_bucket) if dst_bucket else self.bucket_uri, dst=dst_path)
        system_cmd(self.cmd.copy(uri1, uri2, recursive, include, exclude), False)

    def create_bucket(self, region='us-east-1'):
        """
        Create a new S3 bucket.

        :param region: Bucket's hosting region
        """
        # Validate that the bucket does not already exist
        assert self.bucket_name not in self.buckets, 'ERROR: Bucket `{0}` already exists.'.format(self.bucket_name)
        system_cmd(self.cmd.make_bucket(self.bucket_uri, region), False)

    def delete_bucket(self, force=False):
        """
        Deletes an empty S3 bucket. A bucket must be completely empty of objects and versioned
        objects before it can be deleted. However, the force parameter can be used to delete
        the non-versioned objects in the bucket before the bucket is deleted.

        :param force: Deletes all objects in the bucket including the bucket itself
        """
        # Validate that the bucket does exist
        assert self.bucket_name in self.buckets, 'ERROR: Bucket `{0}` does not exists.'.format(self.bucket_name)
        system_cmd(self.cmd.remove_bucket(self.bucket_uri, force), False)
