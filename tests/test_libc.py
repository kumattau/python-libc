import time

from libc import *


def test_getpid():
    pid = getpid()
    assert pid == os.getpid()


def test_timerfd():
    tfd = timerfd_create(CLOCK.REALTIME, 0)
    timerfd_settime(tfd, 0, (0.5, 1))
    t = time.perf_counter()
    _ = os.read(tfd, 8)
    _ = os.read(tfd, 8)
    _ = os.read(tfd, 8)
    t = time.perf_counter() - t
    assert 2 - 1e-3 < t < 2 + 1e-3
