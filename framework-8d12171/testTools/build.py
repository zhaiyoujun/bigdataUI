#!/usr/bin/python
import glob
import os


def splitToolname(fullname):
    sections = fullname.split('-', 1)
    if len(sections) == 1:
        return sections[0], ''
    else:
        return sections[0], sections[1]


os.system('rm -rf *.tar.gz')

for tool in glob.glob('*'):
    if not os.path.isdir(tool):
        continue
    op, ver = splitToolname(tool)
    os.system('sh build-one.sh %s %s' % (tool, op))

os.system('rm -rf tmp')
