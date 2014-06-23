#! /usr/bin/env python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Written (W) 2012-2013 Seung-Jin Sul (ssul@lbl.gov)
# Copyright (C) NERSC, LBL

"""
Get resource usage for the process.
Adapted from http://code.activestate.com/recipes/286222/
"""

import os
import sys
import time
import subprocess

from Common import *
from Run import *

g_scale_inv = ( (1024.*1024.,"MB"),(1024.,"KB") )

"""
return cpu usage of process

@param pid
"""
#-------------------------------------------------------------------------------
def get_cpu_load(pid):
#-------------------------------------------------------------------------------
    psCmd = "ps h -o pcpu -p %d" % (pid)
    cpuLoad = 0
    
    try:
        psOut = backTicks(psCmd, shell=True)
        cpuLoad = psOut.strip()
    except CalledProcessError, msg:
        #logger.exception("Failed to call %s. Exit code=%s" % (msg.cmd, msg.returncode))
        pass

    return cpuLoad

"""
get the total runtime in sec with pid.

@param pid
"""
#-------------------------------------------------------------------------------
def get_runtime(pid):
#-------------------------------------------------------------------------------
    procStatFile = '/proc/%d/stat' % pid
    grepCmd = 'grep btime /proc/stat | cut -d " " -f 2'
    catCmd = 'cat /proc/%d/stat | cut -d " " -f 22' % pid
    procRunTime = 0

    try:
        bootTime = backTicks(grepCmd, shell=True)
        bootTime = int(bootTime.strip())

        if os.path.exists(procStatFile):
            msecSinceBoot = backTicks(catCmd, shell=True)
        else:
            return procRunTime
        msecSinceBoot = int(msecSinceBoot.strip())
        secSinceBoot = msecSinceBoot / 100

        pStartTime = bootTime + secSinceBoot
        now = time.time()
        procRunTime = int(now - pStartTime) # unit in seconds will be enough
    except CalledProcessError, msg:
        #logger.exception("Failed to call %s. Exit code=%s" % (msg.cmd, msg.returncode))
        pass
    
    return procRunTime


##-------------------------------------------------------------------------------
#def get_memory_usage(pid):
##-------------------------------------------------------------------------------
#    """
#    return memory usage in Mb.
#
#    @param pid
#    """
#    return _VmB('VmSize:', pid)


"""
get various mem usage properties of process with id pid in MB

@param VmKey
@param pid
"""
#-------------------------------------------------------------------------------
def _VmB(VmKey, pid):
#-------------------------------------------------------------------------------
    procStatus = '/proc/%d/status' % pid
    unitScale = {'kB': 1.0/1024.0, 'mB': 1.0,
                 'KB': 1.0/1024.0, 'MB': 1.0}

    ## get pseudo file /proc/<pid>/status
    try:
        if os.path.exists(procStatus):
            t = open(procStatus)
            v = t.read()
            t.close()
        else:
            return 0.0
    except OSError:
        logger.exception("Failed to open /proc files.")
        return 0.0 # non-Linux?

    ## get VmKey line e.g. 'VmRSS: 9999 kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3) # by whitespace
    if len(v) < 3:
        return 0.0 # invalid format?

    ## convert Vm value to bytes
    return float(v[1]) * unitScale[v[2]]
 
"""
convert scale
"""
#-------------------------------------------------------------------------------
def toScale(x):
#-------------------------------------------------------------------------------
    for sc in g_scale_inv:
        y = x/sc[0]
        if y >= 1:
            return "%.3f%s" % (y,sc[1])
    return "%.3f%s" % (y,"B")


"""
Return memory usage in bytes or as formatted string.

@param pid
@param since
@param asStr
"""
#-------------------------------------------------------------------------------
def get_virtual_memory_usage(pid, since=0.0, asStr=True):
#-------------------------------------------------------------------------------
    b = _VmB('VmSize:', pid) - since
    if asStr:
        return "VirtMem: " + toScale(b)
    else:
        return b

"""
Return resident memory usage in bytes.

@param pid
@param since
@param asStr
"""  
#-------------------------------------------------------------------------------
def get_resident_memory_usage(pid, since=0.0, asStr=True):
#-------------------------------------------------------------------------------
    b = _VmB('VmRSS:', pid) - since
    if asStr:
        return "ResMem: " + toScale(b)
    else:
        return b
   
"""
Return stack size in bytes.
@param pid
@param since
@param asStr
""" 
#-------------------------------------------------------------------------------
def get_stacksize(pid, since=0.0, asStr=True):
#-------------------------------------------------------------------------------
    b = _VmB('VmStk:', pid) - since
    if asStr:
        return "StackMem: " + toScale(b)
    else:
        return b

"""
get the process id tree from parentPid = root to leaf processes

@param pid: root process id
"""
#-------------------------------------------------------------------------------
def get_pid_tree(pid):
#-------------------------------------------------------------------------------    
    cmd = "ps -o pid --ppid %d --noheaders" % pid
    cpids = []
    cpids.append(pid)
    
    try:
        psOut = backTicks(cmd, shell=True)
        cpids.extend([int(pidStr) for pidStr in psOut.split("\n")[:-1]]) 
    except CalledProcessError, msg:
        #logger.exception("Failed to call %s. Exit code=%s" % (msg.cmd, msg.returncode))
        pass

    ## To do
    #import psutil
    #cpids.extend([p.pid for p in psutil.Process(pid).get_children(recursive=True)])

    return cpids

"""
get % mem used per node
"""
#-------------------------------------------------------------------------------
def get_total_mem_usage_per_node():
#-------------------------------------------------------------------------------
    cmd = "free"
    
    try:
        freeOut = backTicks(cmd, shell=True)
    except CalledProcessError, msg:
        logger.exception("Failed to call %s. Exit code=%s" % (msg.cmd, msg.returncode))
        return -1

    return float(freeOut.split('\n')[1].split()[2]) / \
           float(freeOut.split('\n')[1].split()[1]) * 100.0

"""
get total number of workers on a given node
"""
#-------------------------------------------------------------------------------
def get_num_tfmqworkers_on_node():
#-------------------------------------------------------------------------------    
    cmd = "ps ax | grep -v grep | grep tfmq-worker | wc -l"
    psOut = 0
    
    try:
        psOut = backTicks(cmd, shell=True)
    except CalledProcessError, msg:
        logger.exception("Failed to call %s. Exit code=%s" % (msg.cmd, msg.returncode))
        return -1

    return int(psOut) / 3 ## we have three processes per a worker
    
## EOF