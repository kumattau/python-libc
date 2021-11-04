#
# Copyright (c) 2021 kumattau
#
# Use of this source code is governed by a MIT License
#

"""
A python raw libc bindings
"""

__version__ = "0.0.1"

import ctypes.util

_libc = ctypes.CDLL(ctypes.util.find_library("c"))


def getpid() -> int:
    return int(_libc.getpid())
