# -*- coding: utf-8 -*-
# Author:       zrlyou<zrlyouwin@gmail.com>
# Date:         2018/2/1
# FileName:     unity_tool.py
# Description:  Tool for Unity

import os
import thread
from buildtools import common, log_tool


def build(method, unity_path, project_path, log_path):
    """
    调用unity命令行来构建项目
    :param method:
    :param unity_path:
    :param project_path:
    :param log_path:
    :return:
    """
    build_cmd = [unity_path,
                 '-batchmode',
                 '-projectPath', project_path,
                 '-nographics',
                 '-executeMethod', method,
                 '-logFile', log_path,
                 '-quit']
    log_tool.show_info('Start Unity...')

    if os.path.exists(log_path):
        os .remove(log_path)
        log_tool.show_info('Delete the old logfile!')

    thread.start_new_thread(common.start_thread_to_tail, (log_path,))

    log_tool.show_info('Run Unity Command: {}'.format(' '.join(build_cmd)))
    result_file = 'result.txt'
    # common.run_command(build_cmd, cwd=project_path)
    common.run_command_write_result_to_file(build_cmd, result_file, is_print=True, cwd=project_path)
    log_tool.show_info('Run Command is done!')

