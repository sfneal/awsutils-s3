class S3Commands:
    @staticmethod
    def copy(uri1, uri2, recursive=False, include=None, exclude=None):
        """
        Copy file(s)/folder(s) from one S3 bucket location to another

        :param uri1: S3 uri #1
        :param uri2: S3 uri #2
        :param recursive: Recursively copy all files within the directory
        :param include: Don't exclude files or objects in the command that match the specified pattern
        :param exclude: Exclude all files or objects from the command that matches the specified pattern
        :return: Command string
        """
        cmd = 'aws s3 cp {uri1} {uri2}'
        cmd += ' --recursive' if recursive else ''
        cmd += ' --include "{0}"'.format(include) if include else ''
        cmd += ' --exclude "{0}"'.format(exclude) if exclude else ''
        return cmd.format(uri1=uri1, uri2=uri2)

    @staticmethod
    def remove(uri, recursive=False, include=None, exclude=None):
        """
        Delete an S3 object from a bucket.

        :param uri: S3 object uri
        :param recursive: Recursively copy all files within the directory
        :param include: Don't exclude files or objects in the command that match the specified pattern
        :param exclude: Exclude all files or objects from the command that matches the specified pattern
        :return: Command string
        """
        cmd = 'aws s3 rm {uri}'
        cmd += ' --recursive' if recursive else ''
        cmd += ' --include "{0}"'.format(include) if include else ''
        cmd += ' --exclude "{0}"'.format(exclude) if exclude else ''
        return cmd.format(uri=uri)

    @staticmethod
    def sync(source_path, destination_uri, delete=False, acl='private'):
        """
        Synchronize local files with an S3 bucket.

        :param source_path: Local source directory
        :param destination_uri: URI of destination S3 bucket (with path)
        :param delete: Sync with deletion, disabled by default
        :param acl: Access permissions, must be either 'private', 'public-read' or 'public-read-write'
        :return: Command string
        """
        cmd = 'aws s3 sync "{source_path}" {destination_uri} --acl {acl}'
        cmd += ' --delete' if delete else ''
        return cmd.format(source_path=source_path, destination_uri=destination_uri, acl=acl)

    @staticmethod
    def list(uri='', recursive=False, human_readable=False, summarize=False):
        """
        List files/folders in a bucket if a URI is specified or list available buckets.

        :param uri: S3 bucket URI
        :param recursive: Recursively list files/folders
        :param human_readable: Displays file sizes in human readable format
        :param summarize: Displays summary information (number of objects, total size)
        :return: Command string
        """
        cmd = 'aws s3 ls {uri}'
        cmd += ' --recursive' if recursive else ''
        cmd += ' --human-readable' if human_readable else ''
        cmd += ' --summarize' if summarize else ''
        return cmd.format(uri=uri)

    @staticmethod
    def make_bucket(uri, region=None):
        """
        Creates an S3 bucket.

        :param uri: S3 bucket uri
        :param region: AWS region
        :return: Command string
        """
        cmd = 'aws s3 mb {uri}'
        cmd += ' --region {region}'.format(region=region) if region else ''
        return cmd.format(uri=uri)

    @staticmethod
    def remove_bucket(uri, force=False):
        """
        Delete an S3 bucket if it is empty.

        :param uri: S3 bucket uri
        :param force: Deletes all objects in the bucket including the bucket itself
        :return: Command string
        """
        cmd = 'aws s3 rb {uri}'
        cmd += ' --force' if force else ''
        return cmd.format(uri=uri)

    @staticmethod
    def pre_sign(uri, expiration=3600):
        """
        Generate a pre-signed URL for an Amazon S3 object.

        This allows anyone who receives the pre-signed URL to retrieve the S3 object
        with an HTTP GET request.

        :param uri: S3 object URI
        :param expiration: Number of seconds until the pre-signed URL expires
        :return: Command string
        """
        return 'aws s3 presign {uri} --expires-in {expiration}'.format(uri=uri, expiration=expiration)
