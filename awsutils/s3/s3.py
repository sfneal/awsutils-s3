import os
from awsutils.s3._constants import ACL, TRANSFER_MODES


def mb_to_bytes(mb):
    """Convert Megabytes value to bytes."""
    return mb * 1024 * 1024


class S3Upload:
    def __init__(self, transfer_mode, chunk_size, multipart_threshold):
        """
        AWS CLI S3 uploader.

        :param transfer_mode: Upload/download mode
        :param chunk_size: Size of chunk in multipart upload in MB
        :param multipart_threshold: Minimum size in MB to upload using multipart.
        """
        self.transfer_mode = transfer_mode
        self.chunk_size = mb_to_bytes(chunk_size)
        self.multipart_threshold = mb_to_bytes(multipart_threshold)


class S3(S3Upload):
    def __init__(self, bucket, transfer_mode='auto', chunk_size=5, multipart_threshold=10):
        """
        AWS CLI S3 wrapper.

        :param bucket: S3 bucket name
        :param transfer_mode: Upload/download mode
        :param chunk_size: Size of chunk in multipart upload in MB
        :param multipart_threshold: Minimum size in MB to upload using multipart.
        """
        assert transfer_mode in TRANSFER_MODES, "ERROR: Invalid 'transfer_mode' value."
        assert chunk_size > 4, "ERROR: Chunk size minimum is 5MB."

        self.bucket = bucket
        S3Upload.__init__(self, transfer_mode, chunk_size, multipart_threshold)

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
        assert acl in ACL, "ACL parameter must be one of the following: {0}".format(', '.join("'{0}'".format(i)
                                                                                                 for i in ACL))
        cmd = 'aws s3 sync "{src}" s3://{bucket}/{dst} --acl {acl}'.format(src=local_path, dst=remote_path,
                                                                           bucket=self.bucket, acl=acl)
        if delete:
            cmd += ' --delete'
        os.system(cmd)

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
