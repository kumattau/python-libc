import os

import libc


def test_getpid():
    pid = libc.getpid()
    assert pid == os.getpid()
