import os
from awsutils.s3._constants import S3_ACL


class S3:
    def __init__(self, bucket):
        self.bucket = bucket

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
        :return:
        """
        assert acl in S3_ACL, "ACL parameter must be one of the following: {0}".format(', '.join("'{0}'".format(i)
                                                                                                 for i in S3_ACL))
        cmd = 'aws s3 sync "{src}" s3://{bucket}/{dst} --acl {acl}'.format(src=local_path, dst=remote_path,
                                                                           bucket=self.bucket, acl=acl)
        if delete:
            cmd += ' --delete'
        os.system(cmd)
