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
        
        print("update stock basicdata begin...")
        # 获取数据
        stockquery = StockQuery()
        # 获取并更新基础数据
        stockdata = stockquery.getStockBasicData()
        #print( stockdata.ix[0,0] )
        #stockdata.ix[0]
        icount = len(stockdata.values)
        for i in range(icount):
            ts_code = stockdata.values[i,0]
            symbol = stockdata.values[i,1]
            stkname = stockdata.values[i,2]
            stkarea = stockdata.values[i,3]
            industry = stockdata.values[i,4]
            list_status = stockdata.values[i,5]
            list_date = stockdata.values[i,6]
            # update
            sql = '''select symbol from stock_basic where ts_code = '{0}'
            '''.format( ts_code )
            try:
                cursor.execute(sql)
                if ( cursor.fetchone() != None ):
                    # update
                    sql2 = '''update stock_basic set symbol='{1}',name='{2}',
                    area='{3}',industry='{4}',list_status='{5}',
                    list_date='{6}' where ts_code='{0}'
                    '''.format(ts_code,symbol,stkname,stkarea,
                    industry,list_status,list_date)
                    #print( sql2 )
                    try:
                        cursor.execute(sql2)
                        dbcon.commit()
                    except:
                        print("update db error")
                        dbcon.rollback()
                else:
                    # add
                    sql3 = '''insert into stock_basic (ts_code,symbol,name,
                    area,industry,list_status,list_date) 
                    values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(ts_code,symbol,stkname,stkarea,industry,list_status,list_date)
                    #print( sql3 )
                    try:
                        cursor.execute(sql3)
                        dbcon.commit()
                    except:
                        print("insert db error")
                        dbcon.rollback()
                        
            except:
                print( "Error: unable to fecth data" )
            
            
        # 存储数据
        
        print("update stock basicdata ok")
        
        
        print("update stock detail data begin...")
        
        
        
        
        print("update stock detail data ok")
        
        # 关闭db
        dbcon.close()
    
    def connectdb( self ):
        dbcon = MySQLdb.connect(host=self.db_host, port=self.db_port, 
                             user=self.db_user, passwd=self.db_passwd, 
                             db=self.db_name, charset=self.db_charset )        
        return dbcon
    


