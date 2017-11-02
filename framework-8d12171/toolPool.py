# coding: utf8

import glob
import logging
import os

import config
from const import RequestField, TaskError

Logger = logging.getLogger('')


def splitToolname(fullname):
    sections = fullname.split('-')
    if len(sections) == 1:
        return sections[0], ''
    else:
        return '-'.join(sections[:-1]), sections[-1]


class ToolPool(object):
    # TODO 支持非本地文件系统的存储介质

    @classmethod
    def details(cls):
        tools = {}
        for path in glob.glob(config.TOOLS_DIR + '/*.tar.gz'):
            file = os.path.basename(path)
            name, version = splitToolname(file[:-7])
            if name not in tools:
                tools[name] = []
            tools[name].append({
                RequestField.TOOL_NAME: name,
                RequestField.TOOL_VERSION: version,
                RequestField.TOOL_PATH: path
            })

        def trimVersion(version):
            v = version.split('.', 2)
            for i in xrange(len(v)):
                try:
                    v[i] = int(v[i])
                except:
                    v[i] = 0
            while len(v) < 3:
                v.append(0)
            return v

        def compareTool(t1, t2):
            v1 = trimVersion(t1[RequestField.TOOL_VERSION])
            v2 = trimVersion(t2[RequestField.TOOL_VERSION])
            for i in xrange(3):
                if v1[i] != v2[i]:
                    return v1[i] - v2[i]
            return 0

        for name, versions in tools.items():
            versions.sort(cmp=compareTool, reverse=True)

        return tools

    @classmethod
    def prepare(cls, operation, version, workDir):
        tools = cls.details()

        if operation not in tools:
            return TaskError.MISS_TOOL, None

        tool = None
        if version is None or version == '':
            tool = tools[operation][0]
        else:
            for t in tools[operation]:
                if t[RequestField.TOOL_VERSION] == version:
                    tool = t
                    break
        if tool is None:
            return TaskError.MISS_TOOL, None

        sourceTarFile = tool[RequestField.TOOL_PATH]
        if not os.path.exists(sourceTarFile):
            return TaskError.MISS_TOOL, tool[RequestField.TOOL_VERSION]

        os.system('tar -xzf %s -C %s' % (sourceTarFile, workDir))
        if not os.path.exists(workDir + '/' + operation):
            return TaskError.TOOL_ERROR, tool[RequestField.TOOL_VERSION]

        return 0, tool[RequestField.TOOL_VERSION]
