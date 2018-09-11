# -*- coding: utf-8 -*-
# Author:       zrlyou<zrlyouwin@gmail.com>
# Date:         2018/1/22
# FileName:     common.py
# Description:  Common function

import os
import sys
import time
import tail
import platform
import subprocess
import shutil
from shutil import *
from buildtools import log_tool


def run_command(cmd, cwd=None, is_print=True):
    if is_print:
        print '================================================='
        print "========== [Run Command]: {} ==========".format(' '.join(cmd))
        print '================================================='
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)

    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() is not None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    exit_code = process.poll()
    if exit_code != 0:
        log_tool.show_error('Run Command Error for {}, Error code: {}'.format(' '.join(cmd), exit_code))
        exit(exit_code)
    log_tool.show_info('Done!')


def run_command_write_result_to_file(cmd, result_file, is_print=True, cwd=None):
    if is_print:
        print '================================================='
        print "========== [Run Command]: {} ==========".format(' '.join(cmd))
        print '================================================='
        print "========== [Result file]: {} ==========".format(result_file)
        print '================================================='

    with open(result_file, 'w') as outfile:
        process = subprocess.Popen(cmd, stdout=outfile, stderr=outfile, cwd=cwd)
        process.wait()

    exit_code = process.poll()
    if exit_code != 0:
        time.sleep(2)
        log_tool.show_error('[ERROR]: Run Command Error for {}, Error code: {}'.format(' '.join(cmd), exit_code))
        exit(exit_code)
    log_tool.show_info('Run Command is done!')


def log_tail(content):
    """
    show content
    :param content:
    :return:
    """
    print content


def start_thread_to_tail(tail_file):
    """
    start a thread to tail a file
    :param tail_file:
    :return:
    """
    print 'Wait for tail file... {}'.format(tail_file)

    while True:
        if os.path.exists(tail_file):
            print 'Start tail file... {}'.format(tail_file)
            break
    t = tail.Tail(tail_file)
    t.register_callback(log_tail)
    t.follow(s=1)


def full_path(relative_path):
    return os.path.abspath(os.path.expanduser(relative_path))


def is_macos():
    return 'Darwin' in platform.platform()


def is_windows():
    return 'Windows' in platform.platform()


def is_linux():
    return 'Linux' in platform.platform()


def copytree(src, dst, symlinks=False, ignore=None):
    """
    auto overwrite tree
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    # This one line does the trick
    if not os.path.isdir(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Exception, errors
