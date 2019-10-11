# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:28:25 2019

@author: jingzl

datatrans.py: get data from web and save to db.
"""
import MySQLdb
import time
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
        
        print("[{0}]--update stock basicdata begin...".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        start = time.perf_counter()
        # 获取数据
        stockquery = StockQuery()
        # 获取并更新基础数据
        stockdata = stockquery.getStockBasicData()
        #print( stockdata.ix[0,0] )
        #stockdata.ix[0]
        self.updateStockList( dbcon, stockdata )
        dur = time.perf_counter() - start
        print("[{}]--update stock basicdata finished.[{:.2f}s]".format(time.strftime("%Y-%m-%d %H:%M:%S"),dur))
        
        print("[{}]--update stock daily data begin...".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        start = time.perf_counter()
        self.updateStockDailyData( dbcon, stockdata )
        dur = time.perf_counter() - start
        print("[{}]--update stock daily data finished.[{:.2f}s]".format(time.strftime("%Y-%m-%d %H:%M:%S"),dur))
        
        # 关闭db
        dbcon.close()
    
    def connectdb( self ):
        dbcon = MySQLdb.connect(host=self.db_host, port=self.db_port, 
                             user=self.db_user, passwd=self.db_passwd, 
                             db=self.db_name, charset=self.db_charset )        
        return dbcon
    
    def updateStockList( self, dbcon, stockdata ):
        cursor = dbcon.cursor()
        icount = len(stockdata.values)
        print( "update stock list - {}".format(icount) )
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
        
        
    def updateStockDailyData( self, dbcon, stockdata ):
        stockquery = StockQuery()
        # 判断当前是否是交易日，如果是，则抓取更新，否则pass
        if not stockquery.getTradeCal( '20190901', '20191009' ):
            print( "today is not trade" )
            return
        cursor = dbcon.cursor()
        icount = len(stockdata.values)
        for i in range(600,icount): #range(icount)
            ts_code = stockdata.values[i,0]
            print("save {0}--{1} data".format( i, ts_code ) )
            df = stockquery.getStockDailyData( ts_code, '20190101', '20191009' )
            #print( df )
            ilen = len(df.values)
            for j in range( ilen ):
                #print( df.values[ilen-1-j, 0])
                #print( df.values[ilen-1-j, 1])
                sql = '''insert into stock_daily (ts_code,trade_date,vopen,
                       vhigh,vlow,vclose,pre_close,vchange,pct_chg,vol,amount) 
                      values ('{0}','{1}',{2},{3},{4},{5},{6},{7},{8},{9},{10})
                      '''.format(ts_code, df.values[ilen-1-j, 1], 
                      df.values[ilen-1-j, 2], df.values[ilen-1-j, 3],
                      df.values[ilen-1-j, 4], df.values[ilen-1-j, 5],
                      df.values[ilen-1-j, 6], df.values[ilen-1-j, 7],
                      df.values[ilen-1-j, 8], df.values[ilen-1-j, 9],
                      df.values[ilen-1-j, 10])
                #print( sql )
                try:
                    cursor.execute(sql)
                    dbcon.commit()
                except:
                    print("insert stock_daily error [{0}-{1}]".format(ts_code, df.values[ilen-1-j, 1]))
                    dbcon.rollback()
            





