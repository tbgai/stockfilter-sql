# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:28:25 2019

@author: jingzl

datatrans.py: get data from web and save to db.
"""
import MySQLdb
from func.stockquery import StockQuery


class DataTrans( object ):
    
    db_host = ""
    db_port = 0
    db_user = ""
    db_passwd = ""
    db_name = ""
    db_charset = ""
    
    def __init__( self, dbhost, dbport, dbuser, dbpasswd, dbname, dbcharset ):
        self.db_host = dbhost
        self.db_port = dbport
        self.db_user = dbuser
        self.db_passwd = dbpasswd
        self.db_name = dbname
        self.db_charset = dbcharset

    def trans( self ):
        # 连接db
        dbcon = self.connectdb()
        cursor = dbcon.cursor()
        #cursor.execute("SELECT VERSION()")
        
        # 获取数据
        stockquery = StockQuery()
        stockdata = stockquery.getStockBasicData()
        print( stockdata )
        
        # 存储数据
        
        
        
        # 关闭db
        dbcon.close()
    
    def connectdb( self ):
        dbcon = MySQLdb.connect(host=self.db_host, port=self.db_port, 
                             user=self.db_user, passwd=self.db_passwd, 
                             db=self.db_name, charset=self.db_charset )        
        return dbcon
    


