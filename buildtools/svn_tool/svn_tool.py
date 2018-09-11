# -*- coding: utf-8 -*-
# Author:       zrlyou<zrlyouwin@gmail.com>
# Date:         2018/1/22
# FileName:     svn_tool.py
# Description:  Tool for svn

import os
import sys
import shutil
from subprocess import check_output
from buildtools import common, log_tool


def svn_checkout(svn_url, local_path):
    """
    svn checkout
    :param svn_url:
    :param local_path:
    :return:
    """
    cmd = ['svn', 'co', svn_url, local_path]
    common.run_command(cmd)


def svn_switch(svn_url, local_path, revision=None):
    """
    svn switch
    :param svn_url:
    :param local_path:
    :param revision:
    :return:
    """
    cmd = ['svn', 'switch', svn_url, local_path, '--accept', 'theirs-full', '--force']

    if revision:
        cmd.append('-r')
        cmd.append(revision)
    common.run_command(cmd)


def svn_up(local_path, version_number=None):
    """
    svn up
    :param local_path:
    :param version_number:
    :return:
    """
    if type(local_path) == str:
        paths = [local_path]
    else:
        paths = local_path

    if version_number:
        cmd = ['svn', 'up', '-r', version_number] + paths
    else:
        cmd = ['svn', 'up'] + paths

    common.run_command(cmd)


def svn_commit(local_path, message):
    if type(local_path) == str:
        paths = [local_path]
    else:
        paths = local_path

    cmd = ['svn', 'commit'] + paths + ['-m', message]
    common.run_command(cmd)


def svn_add(local_path):
    """
    svn add
    :param local_path:
    :return:
    """
    os.chdir(local_path)
    cmd = ['svn', 'add', local_path, '--force']
    common.run_command(cmd)


def svn_revert(local_path):
    """
    svn revert
    :param local_path:
    :return:
    """
    cmd = ['svn', 'revert', local_path, '--depth', 'infinity']
    result = common.run_command(cmd)
    log_tool.show_info("The local path is {}.Revert status: {}".format(local_path, result))


def svn_cleanup(local_path):
    """
    svn cleanup
    :param local_path:
    :return:
    """
    cmd = ['svn', 'cleanup', local_path]
    common.run_command(cmd)


def svn_delete(delete_path):
    cmd = ['svn', 'delete', delete_path]
    common.run_command(cmd)


def is_link(file_path):
    """
    check whether the file is link file
    :param file_path:
    :return:
    """
    if sys.platform == 'win32':
        cmd = ['stat', file_path]
        result = check_output(cmd, shell=True)
        return 'symbolic link' in result
    else:
        return os.path.islink(file_path)


def delete_link(file_path):
    if not os.path.exists(file_path):
        return True
    os.remove(file_path)


def delete_check(path, ignore_paths):
    """
    check whether the file or the directory is deleted
    :param path:
    :param ignore_paths:
    :return:
    """
    is_ignore = False
    if ignore_paths:
        for ignore_path in ignore_paths:
            if ignore_path in path:
                is_ignore = True
                break
    return is_ignore


def delete_all(path, ignore_paths):
    """
    delete file or directory
    :param path:
    :param ignore_paths:
    :return:
    """
    path = path.replace('\\', '/')

    if delete_check(path, ignore_paths):
        return False
    if not os.path.isdir(path) or is_link(path):
        log_tool.show_info('Delete file or link: {}'.format(path))
        delete_link(path)
        return True
    log_tool.show_info('Delete directory: {}'.format(path))
    shutil.rmtree(path)
    return True


def delete_unversioned(local_path, ignore_paths=None):
    """
    delete unversioned file or directory
    :param local_path:
    :param ignore_paths:
    :return:
    """
    os.chdir(local_path)

    is_match = False

    lines = os.popen('svn status --no-ignore').readlines()
    for line in lines:
        first_char = line[0]
        if first_char == 'I' or first_char == '?':
            path = line[1:].strip()
            delete_all(path, ignore_paths)
            is_match = True

    if not is_match:
        log_tool.show_warn("Ignore[0 changed] unversioned files for handle on [{}]".format(local_path))

