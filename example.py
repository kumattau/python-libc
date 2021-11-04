#
# Copyright (c) 2021 kumattau
#
# Use of this source code is governed by a MIT License
#

"""
libc example
"""

import os
import libc

def main():
    pid = libc.getpid()
    assert pid == os.getpid()

if __name__ == "__main__":
    main()

