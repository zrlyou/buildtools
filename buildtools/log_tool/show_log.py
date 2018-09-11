# -*- coding: utf-8 -*-
# Author:       zrlyou<zrlyouwin@gmail.com>
# Date:         2018/3/13
# FileName:     show_log.py
# Description:  show level log


def show_info(msg):
    """
    show info level log
    :param msg:
    :return:
    """
    print "[INFO]: {}".format(msg)


def show_warn(msg):
    """
    show warn level log
    :param msg:
    :return:
    """
    print "[WARN]: {}".format(msg)


def show_error(msg):
    """
    show error level log
    :param msg:
    :return:
    """
    print "[ERROR]: {}".format(msg)
