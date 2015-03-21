# -*- coding:utf-8 -*-
'''
Created on 2013年11月19日

@author: Zouyiran
'''

import cPickle as pickle
from config.config import *

def storeip(ip,segmac,xmldict,segIP):
    filename = PROGRAM_ROOT + os.sep + 'seg_ip.txt'
    flag = ip in segIP.values()
    if not flag:
        segIP[segmac] = ip
        segIP[segmac+'_port'] = xmldict[segmac+'_port']
        ipfile = open(filename,'wb')
        pickle.dump(segIP,ipfile)
        ipfile.close()
    else:
        pass