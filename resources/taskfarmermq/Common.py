#! /usr/bin/env python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Written (W) 2012-2013 Seung-Jin Sul (ssul@lbl.gov)
# Copyright (C) NERSC, LBL

import uuid
import cPickle
import zlib
import sys
import os
import argparse
import getpass
import shutil
import fileinput

import multiprocessing
import time
import signal

import datetime
import socket
import subprocess
#import atexit

try:
    import pika
    print "Python pika version: ", pika.__version__
except ImportError:
    print >> sys.stderr,"Exception: Error importing pika. Please check your installation."
    sys.exit(1)

from Utils.MsgCompress import zdumps, zloads
from Utils.Run import makeDir

import logging
logger = logging.getLogger(__name__)

## To hide "No handlers could be found for logger "pika.adapters.base_connection"" warning
logging.getLogger('pika').setLevel(logging.INFO)

#-------------------------------------------------------------------------------
def setup_custom_logger(level, bFileLogging=False):
#-------------------------------------------------------------------------------
    """
    Setting up logging

    @param level: logger level
    """    
    ## Set custom loglevel name for printing resource usage
    ## CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10, NOTSET = 0.
    DEBUG_LEVELV_NUM = 60 
    logging.addLevelName(DEBUG_LEVELV_NUM, "RESOURCE")
    
    def resource(self, message, *args, **kws):
        self._log(DEBUG_LEVELV_NUM, message, args, **kws) 
    logging.Logger.resource = resource

    numericLevel = getattr(logging, level.upper(), None)
    if not isinstance(numericLevel, int):
        raise ValueError('Invalid log level: %s' % level)
    
    formatter = logging.Formatter('%(asctime)s | %(module)s | %(funcName)s | %(levelname)s : %(message)s')
    logger.setLevel(numericLevel)
    
    ## StreamLogger
    streamLogger = logging.StreamHandler()
    streamLogger.setLevel(numericLevel)
    streamLogger.setFormatter(formatter)
    logger.addHandler(streamLogger)

    ## FileLogger
    if bFileLogging:
        dateStr = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        logDir = '%s/logs' % (os.getcwd())
        makeDir(logDir)
        logFileName = '%s/tfmq_worker_%s.log' % (logDir, dateStr)
        fileLogger = logging.FileHandler(logFileName)
        fileLogger.setFormatter(formatter)
        fileLogger.setLevel(numericLevel)
        logger.addHandler(fileLogger)
        logger.info("Log file name: %s" % (logFileName))
        
class ConnWrapper(object):
    _conn = None
    def __init__(self, conn):
        self._conn = conn
    
## EOF