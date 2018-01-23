

import os
import subprocess


def silent_check_call(*args, **kwargs):
    """Wrapper for `subprocess.check_call` which silences all output"""
    with open(os.devnull, 'w') as devnull:
        return subprocess.check_call(*args, stdout=devnull, stderr=devnull, **kwargs)
