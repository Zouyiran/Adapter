# -*- coding:utf-8 -*-
'''
# Created on 2013年10月17日
# 
# @author: Echo
# '''

import signal
import sys
import os
from edgemanager.edge_manager import *
from config.config import *
from config.globals import *
import cPickle as pickle

def main():
    #初始化时从文件读入设备状态表
    try:
        filename = PROGRAM_ROOT + os.sep + 'temps' + os.sep + 'devicemap'
        f = open(filename, 'r')
        globals.deviceMap = pickle.load(f)
        logger.info(globals.deviceMap)
    except:
        pass
    edgemanager = EdgeManager(SERVER_PORT, CMSG_PORT)
    edgemanager.run()
    app.run()

def exit_handler(signal, frame):
    #捕获SIGTERM信号，将设备状态表存入磁盘配置文件
    filename = PROGRAM_ROOT + os.sep + 'temps' + os.sep + 'devicemap'
    f = open(filename, 'w')
    pickle.dump(globals.deviceMap, f)
    #随后无条件杀死
    f = open(PROGRAM_ROOT + os.sep + "sys.pid", "r")
    pid = int(f.readline())
    cmd = "kill -9 %d" % pid
    os.system(cmd)

def daemonize(stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null'): 
    try: 
        pid = os.fork() 
        if pid > 0: 
            sys.exit(0) 
    except OSError, e: 
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errorno, e.strerror)) 
        sys.exit(1) 
    
    os.chdir('/') 
    os.umask(0) 
    os.setsid() 
     
    try: 
        pid = os.fork() 
        if pid > 0: 
            sys.exit(0) 
    except OSError, e: 
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errorno, e.strerror)) 
        sys.exit(1) 
         
    for f in sys.stdout, sys.stderr: 
        f.flush() 
     
    si = file(stdin, 'r') 
    so = file(stdout, 'a+') 
    se = file(stderr, 'a+', 0) 
    os.dup2(si.fileno(), sys.stdin.fileno()) 
    os.dup2(so.fileno(), sys.stdout.fileno()) 
    os.dup2(se.fileno(), sys.stderr.fileno())

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, exit_handler)
    daemonize(stdout = PROGRAM_ROOT + os.sep + 'sys.log', stderr = PROGRAM_ROOT + os.sep + 'sys.err') 
    pidfile = open(PROGRAM_ROOT + os.sep + "sys.pid", "w")
    pidfile.write(str(os.getpid()))
    pidfile.close()
    main()