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
import enum
import os

_libc = ctypes.CDLL(ctypes.util.find_library("c"))

SEC_IN_NS = 10**9


def _oserror(errno):
    return OSError(errno, os.strerror(errno))


def _ts_to_f1(ts):
    return ts[0] + ts[1] * 1e-9


def _f1_to_ts(f1):
    ts = (ctypes.c_long * 2)()
    ts[0] = int(f1)
    ts[1] = int((f1 - ts[0]) * 1e9)
    return ts


def _it_to_f2(it):
    return it[0] + it[1] * 1e-9, it[2] + it[3] * 1e-9


def _f2_to_it(f2):
    it = (ctypes.c_long * 4)()
    it[0] = int(f2[0])
    it[1] = int((f2[0] - it[0]) * 1e9)
    it[2] = int(f2[1])
    it[3] = int((f2[1] - it[2]) * 1e9)
    return it


def _int2_to_it(int2):
    """
    Args:
        int2: (it_interval, it_value) in nano-sec.

    Returns:
        ctypes array
            The 1st element is tv_sec in it_interval.
            The 2nd element is tv_nsec in it_interval.
            The 3rd element is tv_sec in it_value.
            The 4th element is tv_nsec in it_value.
    """
    it = (ctypes.c_long * 4)()
    it[0] = int(int2[0]) // SEC_IN_NS
    it[1] = int(int2[0]) % SEC_IN_NS
    it[2] = int(int2[1]) // SEC_IN_NS
    it[3] = int(int2[1]) % SEC_IN_NS
    return it


def _it_to_int2(it):
    """
    Args:
        it :  ctypes array corresponding to  `struct itimerspec` data.

    Returns:
        two element tuple of int in nano-second.

        The 1st element is 'Interval for periodic timer' in nano-second.
        The 2nd element is 'Initial expiration' in nano-second.
    """
    return it[0] * SEC_IN_NS + it[1], it[2] * SEC_IN_NS + it[3]


class CLOCK(enum.IntEnum):
    REALTIME = 0
    MONOTONIC = 1
    PROCESS_CPUTIME_ID = 2
    THREAD_CPUTIME_ID = 3
    MONOTONIC_RAW = 4
    REALTIME_COARSE = 5
    MONOTONIC_COARSE = 6
    BOOTTIME = 7
    REALTIME_ALARM = 8
    BOOTTIME_ALARM = 9


class TIMER(enum.IntFlag):
    ABSTIME = 0x01


class TFD(enum.IntFlag):
    NONBLOCK = 0o2000000
    CLOEXEC = 0o4000


class TFD_TIMER(enum.IntFlag):
    ABSTIME = 1 << 0
    CANCEL_ON_SET = 1 << 1


class EFD(enum.IntFlag):
    NONBLOCK = 0o2000000
    CLOEXEC = 0o4000
    SEMAPHORE = 0o1


class MFD(enum.IntFlag):
    CLOEXEC = 0x1
    ALLOW_SEALING = 0x2
    HUGETLB = 0x4
    HUGE_64KB = 0x40000000
    HUGE_512KB = 0x4c000000
    HUGE_1MB = 0x50000000
    HUGE_2MB = 0x54000000
    HUGE_8MB = 0x5c000000
    HUGE_16MB = 0x60000000
    HUGE_32MB = 0x64000000
    HUGE_256MB = 0x70000000
    HUGE_512MB = 0x74000000
    HUGE_1GB = 0x78000000
    HUGE_2GB = 0x7c000000
    HUGE_16GB = 0x88000000


class SYS(enum.IntEnum):
    read = 0
    write = 1
    open = 2
    close = 3
    stat = 4
    fstat = 5
    lstat = 6
    poll = 7
    lseek = 8
    mmap = 9
    mprotect = 10
    munmap = 11
    brk = 12
    rt_sigaction = 13
    rt_sigprocmask = 14
    rt_sigreturn = 15
    ioctl = 16
    pread64 = 17
    pwrite64 = 18
    readv = 19
    writev = 20
    access = 21
    pipe = 22
    select = 23
    sched_yield = 24
    mremap = 25
    msync = 26
    mincore = 27
    madvise = 28
    shmget = 29
    shmat = 30
    shmctl = 31
    dup = 32
    dup2 = 33
    pause = 34
    nanosleep = 35
    getitimer = 36
    alarm = 37
    setitimer = 38
    getpid = 39
    sendfile = 40
    socket = 41
    connect = 42
    accept = 43
    sendto = 44
    recvfrom = 45
    sendmsg = 46
    recvmsg = 47
    shutdown = 48
    bind = 49
    listen = 50
    getsockname = 51
    getpeername = 52
    socketpair = 53
    setsockopt = 54
    getsockopt = 55
    clone = 56
    fork = 57
    vfork = 58
    execve = 59
    exit = 60
    wait4 = 61
    kill = 62
    uname = 63
    semget = 64
    semop = 65
    semctl = 66
    shmdt = 67
    msgget = 68
    msgsnd = 69
    msgrcv = 70
    msgctl = 71
    fcntl = 72
    flock = 73
    fsync = 74
    fdatasync = 75
    truncate = 76
    ftruncate = 77
    getdents = 78
    getcwd = 79
    chdir = 80
    fchdir = 81
    rename = 82
    mkdir = 83
    rmdir = 84
    creat = 85
    link = 86
    unlink = 87
    symlink = 88
    readlink = 89
    chmod = 90
    fchmod = 91
    chown = 92
    fchown = 93
    lchown = 94
    umask = 95
    gettimeofday = 96
    getrlimit = 97
    getrusage = 98
    sysinfo = 99
    times = 100
    ptrace = 101
    getuid = 102
    syslog = 103
    getgid = 104
    setuid = 105
    setgid = 106
    geteuid = 107
    getegid = 108
    setpgid = 109
    getppid = 110
    getpgrp = 111
    setsid = 112
    setreuid = 113
    setregid = 114
    getgroups = 115
    setgroups = 116
    setresuid = 117
    getresuid = 118
    setresgid = 119
    getresgid = 120
    getpgid = 121
    setfsuid = 122
    setfsgid = 123
    getsid = 124
    capget = 125
    capset = 126
    rt_sigpending = 127
    rt_sigtimedwait = 128
    rt_sigqueueinfo = 129
    rt_sigsuspend = 130
    sigaltstack = 131
    utime = 132
    mknod = 133
    uselib = 134
    personality = 135
    ustat = 136
    statfs = 137
    fstatfs = 138
    sysfs = 139
    getpriority = 140
    setpriority = 141
    sched_setparam = 142
    sched_getparam = 143
    sched_setscheduler = 144
    sched_getscheduler = 145
    sched_get_priority_max = 146
    sched_get_priority_min = 147
    sched_rr_get_interval = 148
    mlock = 149
    munlock = 150
    mlockall = 151
    munlockall = 152
    vhangup = 153
    modify_ldt = 154
    pivot_root = 155
    _sysctl = 156
    prctl = 157
    arch_prctl = 158
    adjtimex = 159
    setrlimit = 160
    chroot = 161
    sync = 162
    acct = 163
    settimeofday = 164
    mount = 165
    umount2 = 166
    swapon = 167
    swapoff = 168
    reboot = 169
    sethostname = 170
    setdomainname = 171
    iopl = 172
    ioperm = 173
    create_module = 174
    init_module = 175
    delete_module = 176
    get_kernel_syms = 177
    query_module = 178
    quotactl = 179
    nfsservctl = 180
    getpmsg = 181
    putpmsg = 182
    afs_syscall = 183
    tuxcall = 184
    security = 185
    gettid = 186
    readahead = 187
    setxattr = 188
    lsetxattr = 189
    fsetxattr = 190
    getxattr = 191
    lgetxattr = 192
    fgetxattr = 193
    listxattr = 194
    llistxattr = 195
    flistxattr = 196
    removexattr = 197
    lremovexattr = 198
    fremovexattr = 199
    tkill = 200
    time = 201
    futex = 202
    sched_setaffinity = 203
    sched_getaffinity = 204
    set_thread_area = 205
    io_setup = 206
    io_destroy = 207
    io_getevents = 208
    io_submit = 209
    io_cancel = 210
    get_thread_area = 211
    lookup_dcookie = 212
    epoll_create = 213
    epoll_ctl_old = 214
    epoll_wait_old = 215
    remap_file_pages = 216
    getdents64 = 217
    set_tid_address = 218
    restart_syscall = 219
    semtimedop = 220
    fadvise64 = 221
    timer_create = 222
    timer_settime = 223
    timer_gettime = 224
    timer_getoverrun = 225
    timer_delete = 226
    clock_settime = 227
    clock_gettime = 228
    clock_getres = 229
    clock_nanosleep = 230
    exit_group = 231
    epoll_wait = 232
    epoll_ctl = 233
    tgkill = 234
    utimes = 235
    vserver = 236
    mbind = 237
    set_mempolicy = 238
    get_mempolicy = 239
    mq_open = 240
    mq_unlink = 241
    mq_timedsend = 242
    mq_timedreceive = 243
    mq_notify = 244
    mq_getsetattr = 245
    kexec_load = 246
    waitid = 247
    add_key = 248
    request_key = 249
    keyctl = 250
    ioprio_set = 251
    ioprio_get = 252
    inotify_init = 253
    inotify_add_watch = 254
    inotify_rm_watch = 255
    migrate_pages = 256
    openat = 257
    mkdirat = 258
    mknodat = 259
    fchownat = 260
    futimesat = 261
    newfstatat = 262
    unlinkat = 263
    renameat = 264
    linkat = 265
    symlinkat = 266
    readlinkat = 267
    fchmodat = 268
    faccessat = 269
    pselect6 = 270
    ppoll = 271
    unshare = 272
    set_robust_list = 273
    get_robust_list = 274
    splice = 275
    tee = 276
    sync_file_range = 277
    vmsplice = 278
    move_pages = 279
    utimensat = 280
    epoll_pwait = 281
    signalfd = 282
    timerfd_create = 283
    eventfd = 284
    fallocate = 285
    timerfd_settime = 286
    timerfd_gettime = 287
    accept4 = 288
    signalfd4 = 289
    eventfd2 = 290
    epoll_create1 = 291
    dup3 = 292
    pipe2 = 293
    inotify_init1 = 294
    preadv = 295
    pwritev = 296
    rt_tgsigqueueinfo = 297
    perf_event_open = 298
    recvmmsg = 299
    fanotify_init = 300
    fanotify_mark = 301
    prlimit64 = 302
    name_to_handle_at = 303
    open_by_handle_at = 304
    clock_adjtime = 305
    syncfs = 306
    sendmmsg = 307
    setns = 308
    getcpu = 309
    process_vm_readv = 310
    process_vm_writev = 311
    kcmp = 312
    finit_module = 313
    sched_setattr = 314
    sched_getattr = 315
    renameat2 = 316
    seccomp = 317
    getrandom = 318
    memfd_create = 319
    kexec_file_load = 320
    bpf = 321
    execveat = 322
    userfaultfd = 323
    membarrier = 324
    mlock2 = 325
    copy_file_range = 326
    preadv2 = 327
    pwritev2 = 328
    pkey_mprotect = 329
    pkey_alloc = 330
    pkey_free = 331
    statx = 332
    io_pgetevents = 333
    rseq = 334
    pidfd_send_signal = 424
    io_uring_setup = 425
    io_uring_enter = 426
    io_uring_register = 427
    open_tree = 428
    move_mount = 429
    fsopen = 430
    fsconfig = 431
    fsmount = 432
    fspick = 433
    pidfd_open = 434
    clone3 = 435


def getpid() -> int:
    return int(_libc.getpid())


def getppid() -> int:
    return int(_libc.getppid())


def getpgid(pid: int) -> int:
    return int(_libc.getpgid(pid))


def getuid() -> int:
    return int(_libc.getuid())


def getgid() -> int:
    return int(_libc.getgid())


def geteuid() -> int:
    return int(_libc.geteuid())


def getegid() -> int:
    return int(_libc.getegid())


def gettid() -> int:
    return int(_libc.syscall(SYS.gettid))


def getsid(pid: int) -> int:
    return int(_libc.getsid(pid))


def kill(pid: int, sig: int) -> None:
    if int(_libc.kill(pid, sig)) == -1:
        raise _oserror(ctypes.get_errno())


def tkill(tid: int, sig: int) -> None:
    if int(_libc.syscall(SYS.tkill, tid, sig)) == -1:
        raise _oserror(ctypes.get_errno())


def tgkill(tgid: int, tid: int, sig: int) -> None:
    if int(_libc.syscall(SYS.tgkill, tgid, tid, sig)) == -1:
        raise _oserror(ctypes.get_errno())


def clock_gettime(clk_id: CLOCK) -> float:
    ts = (ctypes.c_long * 2)()
    if int(_libc.clock_gettime(clk_id, ctypes.byref(ts))) == -1:
        raise _oserror(ctypes.get_errno())
    return ts[0] + ts[1] * 1e-9


def clock_getres(clk_id: CLOCK) -> float:
    ts = (ctypes.c_long * 2)()
    if int(_libc.clock_getres(clk_id, ctypes.byref(ts))) == -1:
        raise _oserror(ctypes.get_errno())
    return ts[0] + ts[1] * 1e-9


def clock_nanosleep(clk_id: CLOCK, flag: TIMER, request: float) -> float:
    ts_req = _f1_to_ts(request)
    ts_rem = (ctypes.c_long * 2)()
    if int(_libc.clock_nanosleep(clk_id, flag, ctypes.byref(ts_req), ctypes.byref(ts_rem))) == -1:
        raise _oserror(ctypes.get_errno())
    return _ts_to_f1(ts_rem)


def nanosleep(req: float) -> float:
    ts_req = _f1_to_ts(req)
    ts_rem = (ctypes.c_long * 2)()
    if int(_libc.nanosleep(ctypes.byref(ts_req), ctypes.byref(ts_rem))) == -1:
        raise _oserror(ctypes.get_errno())
    return _ts_to_f1(ts_rem)


def timerfd_create(clockid: CLOCK, flags: TFD) -> int:
    fd = int(_libc.timerfd_create(clockid, flags))
    if fd == -1:
        raise _oserror(ctypes.get_errno())
    return fd


def timerfd_settime(fd: int, flags: TFD_TIMER, new_value: (float, float)) -> (float, float):
    """
    Args:
        fd :  file descriptor of timerfd
        flags : flag to pass `timerfd_settime`
        new_value : new_value to pass `timerfd_settime` in second by float.
            The 1st element is 'Interval for periodic timer' in second (float).
            The 2nd element is 'Initial expiration' in second (float).

    Returns:
        old_value at timerfd_settime in second by float.
    """
    it_new = _f2_to_it(new_value)
    it_old = (ctypes.c_long * 4)()
    if int(_libc.timerfd_settime(fd, flags, ctypes.byref(it_new), ctypes.byref(it_old))) == -1:
        raise _oserror(ctypes.get_errno())
    return _it_to_f2(it_old)


def timerfd_settime_ns(fd: int, flags: TFD_TIMER, new_value: (int, int)) -> (int, int):
    """
    Args:
        fd :  file descriptor of timerfd
        flags : flag to pass `timerfd_settime`
        new_value : new_value to pass `timerfd_settime` in nano-seconds
            The 1st element is 'Interval for periodic timer' in nano-second.
            The 2nd element is 'Initial expiration' in nano-second.

    Returns:
        old_value at timerfd_settime in nano-second.
    """
    it_new = _int2_to_it(new_value)
    it_old = (ctypes.c_long * 4)()
    if int(_libc.timerfd_settime(fd, flags, ctypes.byref(it_new), ctypes.byref(it_old))) == -1:
        raise _oserror(ctypes.get_errno())
    return _it_to_int2(it_old)


def timerfd_gettime(fd: int) -> (float, float):
    it_cur = (ctypes.c_long * 4)()
    if int(_libc.timerfd_gettime(fd, ctypes.byref(it_cur))) == -1:
        raise _oserror(ctypes.get_errno())
    return _it_to_f2(it_cur)


def timerfd_gettime_ns(fd: int) -> (int, int):
    it_cur = (ctypes.c_long * 4)()
    if int(_libc.timerfd_gettime(fd, ctypes.byref(it_cur))) == -1:
        raise _oserror(ctypes.get_errno())
    return _it_to_int2(it_cur)


def eventfd(initval: int, flags: EFD) -> int:
    fd = int(_libc.eventfd(initval, flags))
    if fd == -1:
        raise _oserror(ctypes.get_errno())
    return fd


def memfd_create(name: str, flags: MFD) -> int:
    fd = int(_libc.memfd_create(name.encode(), flags))
    if fd == -1:
        raise _oserror(ctypes.get_errno())
    return fd
