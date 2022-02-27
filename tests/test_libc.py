import errno
import os
import sys
import time

import pytest

from libc import *


def test_getpid():
    pid = getpid()
    assert pid == os.getpid()


@pytest.mark.parametrize("interval, value, count", [
    ( 0.5  , 1, 3 ),
    ( 0.125, 0.25, 4 ),
])
def test_timerfd(interval: float, value: float, count: int):
    # acceptable error is 1 msec or less.
    limit_error = 2e-3

    tfd = timerfd_create(CLOCK.REALTIME, 0)

    interval2, value2 = timerfd_settime(tfd, 0, (interval, value))
    assert(interval2 == 0)
    assert(value2 == 0)

    interval2, value2 = timerfd_settime(tfd, 0, (interval, value))
    assert(interval2 == interval)
    assert(abs(value2 - value) < limit_error)

    # check by timerfd_gettime
    interval2, value2 = timerfd_gettime(tfd)
    assert(interval2 == interval)
    assert(abs(value2 - value) < limit_error)

    t = time.perf_counter()
    for _ in range(count):
        _ = os.read(tfd, 8)
    t = time.perf_counter() - t

    total_time = value +  interval * (count - 1)
    assert(abs(t - total_time) < limit_error)

    # close timerfd
    os.close(tfd)

    # try to close the timerfd which was already closed.
    with pytest.raises(OSError) as exc_info:
        os.close(tfd)

    # check detail of OSError
    assert exc_info.value.args[0] == errno.EBADF
    assert exc_info.value.args[1] == os.strerror(errno.EBADF)


@pytest.mark.parametrize("interval, value, count", [
    ( SEC_IN_NS //   2, SEC_IN_NS     , 3 ),
    ( SEC_IN_NS //  10, SEC_IN_NS //20, 4 ),
])
def test_timerfd_ns(interval: int, value: int, count: int):
    # acceptable error is 1 msec or less.
    limit_error = SEC_IN_NS // 1000

    # check availability of `time.perf_counter_ns()`.
    # If it is not available (expected on python 3.6), define a stub.
    try:
        _ = time.perf_counter_ns()
    except AttributeError:
        time.perf_counter_ns = lambda: int(time.perf_counter() * SEC_IN_NS)

    tfd = timerfd_create(CLOCK.REALTIME, 0)

    interval2, value2 = timerfd_settime_ns(tfd, 0, (interval, value))
    assert(interval2 == 0)
    assert(value2 == 0)

    interval2, value2 = timerfd_settime_ns(tfd, 0, (interval, value))
    assert(interval2 == interval)
    assert(abs(value2 - value) < limit_error)

    # check by timerfd_gettime_ns
    interval2, value2 = timerfd_gettime_ns(tfd)
    assert(interval2 == interval)
    assert(abs(value2 - value) < limit_error)

    t = time.perf_counter_ns()
    for _ in range(count):
        _ = os.read(tfd, 8)
    t = time.perf_counter_ns() - t

    total_time = value +  interval * (count - 1)
    assert(abs(t - total_time) < limit_error)

    # close timerfd
    os.close(tfd)

    # try to close the timerfd which was already closed.
    with pytest.raises(OSError) as exc_info:
        os.close(tfd)

    # check detail of OSError
    assert exc_info.value.args[0] == errno.EBADF
    assert exc_info.value.args[1] == os.strerror(errno.EBADF)

def test_eventfd():
    efd = eventfd(0, 0)

    a = 10

    _ = os.write(efd, a.to_bytes(8, byteorder=sys.byteorder))
    b = os.read(efd, 8)
    os.close(efd)

    c = int.from_bytes(b, byteorder=sys.byteorder)
    assert a == c

    # try to close the eventfd which was already closed.
    with pytest.raises(OSError) as exc_info:
        os.close(efd)

    # check detail of OSError
    assert exc_info.value.args[0] == errno.EBADF
    assert exc_info.value.args[1] == os.strerror(errno.EBADF)


def test_memfd():
    mfd = memfd_create("test", 0)
    pid = getpid()
    name = os.readlink(f"/proc/{pid}/fd/{mfd}")
    assert name.startswith(f"/memfd:test ")

    # close memfd
    os.close(mfd)
    assert not os.path.exists(f"/proc/{pid}/fd/{mfd}")

    # try to close the memfd which was already closed.
    with pytest.raises(OSError) as exc_info:
        os.close(mfd)

    # check detail of OSError
    assert exc_info.value.args[0] == errno.EBADF
    assert exc_info.value.args[1] == os.strerror(errno.EBADF)
