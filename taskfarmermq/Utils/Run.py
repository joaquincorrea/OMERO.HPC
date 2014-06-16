#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Apr 3, 2013

Convenience methods to make it easier to run external programs
and other os-related tools

@author: Seung-Jin
""" 

from subprocess import Popen, call, PIPE
import os, glob, sys
import shlex
import unittest

defineCalledProcessError = False
try:
    from subprocess import CalledProcessError
except ImportError:
    defineCalledProcessError = True

if defineCalledProcessError:
    class CalledProcessError(OSError):
        def __init__(self, returncode, cmd, *l, **kw):
            OSError.__init__(self, *l, **kw)
            self.cmd = cmd
            self.returncode = returncode

"""
Run user command using subprocess.call
@param: popenargs: command and options to run
@param: kwargs: additional parameters
"""
#-------------------------------------------------------------------------------
def run(*popenargs, **kwargs):
#-------------------------------------------------------------------------------
    kw = {}
    kw.update(kwargs)
    dryRun = kw.pop('dryRun', False)
    
    if dryRun:
        print popenargs
    else:
        ## convert something like run("ls -l") into run("ls -l", shell=True)
        if isinstance(popenargs[0], str) and len(shlex.split(popenargs[0])) > 1:
            kw.setdefault("shell", True)

        ## > /dev/null 2>&1
        if kw.pop("supressAllOutput", False):
            stdnull = open(os.devnull, "w") ## incompat with close_fds on Windows
            kw.setdefault("stdout", stdnull)
            kw.setdefault("stderr", stdnull)
        else:
            stdnull = None
            
        returncode = call(*popenargs, **kw)
        if stdnull:
            stdnull.close()
        if returncode != 0:
            raise CalledProcessError(returncode=returncode, cmd=str(popenargs))

"""
Similar to shell backticks, e.g. a = `ls -1` <=> a = backticks(['ls','-1']).
If 'dryRun=True' is given as keyword argument, then 'dryRet' keyword must
provide a value to return from this function.
@param: popenargs: command and options to run
@param: kwargs: additional parameters
@return: command result (stdout)
"""
#-------------------------------------------------------------------------------
def backTicks(*popenargs, **kwargs):
#-------------------------------------------------------------------------------
    kw = {}
    kw.update(kwargs)
    dryRun = kw.pop('dryRun', False)
    dryRet = kw.pop('dryRet', None)
    
    if dryRun:
        print popenargs
        return dryRet
    else:
        kw['stdout'] = PIPE
        p = Popen(*popenargs, **kw)
        retOut = p.communicate()[0]
        if p.returncode != 0:
            raise CalledProcessError(returncode=p.returncode, cmd=str(popenargs))
        return retOut

"""
Create one dir with pathname path or do nothing if it already exists.
Same as Linux 'mkdir -p'.
@param: path: path to delete
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def makeDir(path, dryRun=False):
#-------------------------------------------------------------------------------
    if not dryRun:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        print "makeDir %s" % (path, )

"""
Create muiltiple dirs with the same semantics as makeDir
@param: path: path to delete
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def makeDirs(paths, dryRun=False):
#-------------------------------------------------------------------------------
    for path in paths:
        makeDir(path=path, dryRun=dryRun)

"""
Assume that the argument is a file name and make all directories that are
part of it
@param: fileName: create dir to the file
"""
#-------------------------------------------------------------------------------
def makeFilePath(fileName):
#-------------------------------------------------------------------------------
    dirName = os.path.dirname(fileName)
    if dirName not in ("", "."):
        makeDir(dirName)

"""
Remove dir
@param: path: path to delete
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def rmDir(path, dryRun=False):
#-------------------------------------------------------------------------------
    ## To do: perhaps use shutil.rmtree instead?    
    run(["rm", "-rf", path], dryRun=dryRun)

## make alias
rmrf = rmDir

"""
Remove file.
@param: path: path to delete
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def rmf(path, dryRun=False):
#-------------------------------------------------------------------------------
    for f in glob.iglob(path):
        try:
            if os.path.exists(f):
                os.remove(f)
        except OSError:
            pass

"""
Remove multiple files.
@param: path: path to delete
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def rmfMany(paths, dryRun=False):
#-------------------------------------------------------------------------------
    for f in paths:
        try:
            os.remove(f)
        except OSError:
            pass

"""
Create an empty dir with a given path.
If path already exists,  it will be removed first.
@param: path: path to delete
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def remakeDir(path, dryRun=False):
#-------------------------------------------------------------------------------
    rmrf(path, dryRun=dryRun)
    makeDir(path, dryRun=dryRun)

"""
Change mode.
@param: path: path to chmod
@param: mode: the form `[ugoa]*([-+=]([rwxXst]*|[ugo]))+'. 
@param: opts: additional chmod options
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def chmod(path, mode, opts='', dryRun=False):
#-------------------------------------------------------------------------------
    if isinstance(path, basestring):
        path = [path]
    else:
        path = list(path)
    run(["chmod"]+opts.split()+[mode]+path, dryRun=dryRun)

"""
Check file existence
@param: path: path to check
@param: dryRun: dryrun directive
"""
#-------------------------------------------------------------------------------
def fExist(path, dryRun=False):
#-------------------------------------------------------------------------------
    return os.path.exists(path)


#-------------------------------------------------------------------------------
class TestOsUtility(unittest.TestCase):
#-------------------------------------------------------------------------------
    def testRun(self):
        try:
            run(["rm","-rf","./unittest"], dryRun=False)    
        except CalledProcessError, msg:
            self.assertNotEqual(msg.returncode, 0)   
        try:
            makeDir("./unittest", dryRun=False)
        except CalledProcessError, msg:
            self.assertEqual(msg.returncode, 0)
        try:
            rmDir("./unittest", dryRun=False)
        except CalledProcessError, msg:
            self.assertEqual(msg.returncode, 0)
        
    def testBackTicks(self):
        cmd = "free"
        try:
            freeOut = backTicks(cmd, shell=True)
        except CalledProcessError, msg:
            print >>sys.stderr, "Failed to call %s. Exit code=%s" % (msg.cmd, msg.returncode)
            sys.exit(1)
        
        ret = -1
        ret = float(freeOut.split('\n')[1].split()[2]) / \
              float(freeOut.split('\n')[1].split()[1]) * 100.0
        assert ret > -1


#
# Use this for testing purpose
if __name__ == "__main__":
    unittest.main()


## EOF


