class S3Commands:
    @staticmethod
    def copy(uri1, uri2, recursive=None, include=None, exclude=None):
        """

        :param uri1: S3 uri #1
        :param uri2: S3 uri #2
        :param recursive: Recursively copy all files within the directory
        :param include: Don't exclude files or objects in the command that match the specified pattern
        :param exclude: Exclude all files or objects from the command that matches the specified pattern
        :return: Command string
        """
        cmd = 'aws s3 cp {uri1} {uri2}'.format(uri1=uri1, uri2=uri2)
        if recursive:
            cmd += ' --recursive'
        if include:
            cmd += ' --include "{0}"'.format(include)
        if exclude:
            cmd += ' --exclude "{0}"'.format(exclude)
        return cmd
