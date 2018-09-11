# -*- coding: utf-8 -*-
# Author:       zrlyou<zrlyouwin@gmail.com>
# Date:         2018/3/13
# FileName:     workspace.py
# Description:  workspace class

import os
from buildtools import svn_tool, common, log_tool


class WorkSpace:
    def __init__(self, workspace, svnbranch='trunk'):
        # 工程目录相关
        self.workspace = workspace

    @staticmethod
    def set_file_permission(file_path):
        """
        设置文件权限
        :param file_path:
        :return:
        """
        cmd = ['chmod', '755', file_path]
        common.run_command(cmd)







