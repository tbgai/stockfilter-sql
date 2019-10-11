# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:12:39 2019

@author: jingzl
"""
import os
import time
from func import cons as ct
from func.configparser import ConfigParser
from func.datatrans import DataTrans


if __name__ == '__main__':
    
    print( "{}".format( '-'*50 ) )
    print("[{0}]--update stockdata db begin...".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    config_file = os.path.dirname( os.path.realpath(__file__)) + ct.CONFIG_FNAME
    config = ConfigParser()
    if config.parse( config_file ):
        datatrans = DataTrans( config.db_host, config.db_port, config.db_user, 
                              config.db_passwd, config.db_name, config.db_charset )
        datatrans.trans()
    else:
        print( "解析配置文件失败，请检查配置文件！" )
    print("[{0}]--update stockdata db end".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    




