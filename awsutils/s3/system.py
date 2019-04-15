import os
from subprocess import Popen, PIPE


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
