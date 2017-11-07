# coding: utf8

import logging
import os
import shutil
import tarfile

Logger = logging.getLogger('')


class FSUtil(object):
    def __init__(self, silent=False):
        self.silent = silent

    def remove(self, path):
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception, e:
            Logger.exception("remove '%s' failed", path)
            if self.silent:
                return False
            raise e
        return True

    def makedirs(self, path):
        try:
            if os.path.exists(path) and os.path.isdir(path):
                return True
            os.makedirs(path)
        except Exception, e:
            Logger.exception("makedirs '%s' failed", path)
            if self.silent:
                return False
            raise e
        return True

    def symlink(self, src, path):
        try:
            os.symlink(src, path)
        except Exception, e:
            Logger.exception("symlink '%s' => '%s' failed", src, path)
            if self.silent:
                return False
            raise e
        return True

    def readlink(self, path):
        try:
            return os.readlink(path)
        except Exception, e:
            Logger.exception("makedirs '%s' failed", path)
            if self.silent:
                return None
            raise e

    def copyfile(self, src, dst):
        try:
            if shutil._samefile(src, dst):
                return True
            shutil.copyfile(src, dst)
        except Exception, e:
            Logger.exception("copy '%s' to '%s' failed", src, dst)
            if self.silent:
                return False
            raise e
        return True

    def extract(self, src, dst):
        try:
            tar = tarfile.open(src, "r:gz")
            for filename in tar.getnames():
                tar.extract(filename, dst)
            tar.close()
        except Exception, e:
            Logger.exception("extract '%s' to '%s' failed", src, dst)
            if self.silent:
                return False
            raise e
        return True
