# coding: utf8

import logging
import logging.handlers

import config


def InitLogging(logfile, instanceId=None):
    fh = logging.handlers.RotatingFileHandler(
        logfile,
        maxBytes=config.LOG_FILE_MB * 1024 * 1024,
        backupCount=config.LOG_FILE_COUNT)
    ch = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter(config.LOG_FORMATTER + ('' if instanceId is None else ' ' + instanceId) + ' %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    Logger = logging.getLogger('')
    Logger.setLevel(logging.DEBUG)
    Logger.addHandler(fh)
    Logger.addHandler(ch)
