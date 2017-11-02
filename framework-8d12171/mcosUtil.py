# coding: utf8

import json
import logging
import os
import urllib2

import config
from fsutil import FSUtil

Logger = logging.getLogger('')
fs = FSUtil()


class MCOSAPI(object):
    @classmethod
    def ListMount(cls, visitorName, token):
        req = urllib2.Request(
            url=config.MCOS_SERVER_HOST + '/datacell/mount/list',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "visitor": {
                    "name": visitorName,
                    "token": token
                }
            })
        )

        try:
            res = urllib2.urlopen(req, timeout=config.MCOS_TIMEOUT)
            result = json.loads(res.read())
            res.close()
        except Exception, e:
            Logger.exception("list mount for visitor '%s' failed", visitorName)
            raise e

        if result['code'] != 0:
            raise Exception("list mount for visitor '%s' failed: code=%s" % str(result['code']))

        return result['data']


class MCOSUtil(object):
    @classmethod
    def Mount(cls, visitorName, token, dir):
        mounts = MCOSAPI.ListMount(visitorName, token)
        fs.makedirs(dir)
        for mount in mounts:
            dcRoot = config.MCOS_DFS_DATA_CELL_RO_ROOT if mount['readOnly'] else config.MCOS_DFS_DATA_CELL_RW_ROOT
            dcPath = os.path.join(dcRoot, mount['dataCellName'])
            fs.symlink(dcPath, os.path.join(dir, mount['point']))
