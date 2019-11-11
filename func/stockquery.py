# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:40:42 2019

@author: jingzl

parse stock data from tushare interface
"""
import datetime
import pandas as pd
import numpy as np
import tushare as ts

TUSHARE_TOKEN = '8af63d3d7f7ec3bc0e511a85b13d0cf01c57dd310bc1f8ed4b902ad3'

class StockQuery( object ):
    
    def __init__( self ):
        pass
    
    def getStockBasicData( self ):
        try:
            # 获取所有的股票列表信息
            pro = ts.pro_api( token=TUSHARE_TOKEN )
            # 查询当前所有正常上市交易的股票列表 , symbol, name
            data = pro.query( 'stock_basic', exchange='', list_status='L', 
                             fields='ts_code,symbol,name,area,industry,list_status,list_date')
            #print( data )
            #print( data.ix[0:3] )
            #print( data.columns )
            #print( data.ix[ 0:3, 1 ] )
            
            #dl = data.ix[ :, 0 ].values
            return data
        except:
            a = []
            df = pd.DataFrame( a, columns=['ts_code','symbol','name',
                                           'area','industry','list_status',
                                           'list_date'],
                             index=np.arange(len(a)))
            return df
        

    def getSingleStockData( self, ts_code, length ):
        
        pro = ts.pro_api( token=TUSHARE_TOKEN )
        '''
        因接口无法根据记录数返回，考虑到正常交易日是工作日，所以按照两倍长度获取数据，
        然后截取 length 数量的数据返回
        '''
        today = datetime.date.today()
        hisday = today - datetime.timedelta(days=2*length)
        start_date = hisday.strftime("%Y%m%d")
        end_date = today.strftime("%Y%m%d")
        
        #print( length )
        #print( start_date )
        #print( end_date )
        try:
            df = pro.query( 'daily', ts_code=ts_code, start_date=start_date,
                       end_date=end_date, fields='trade_date,close')
            dl = df.ix[:,1].values.tolist()
            dl.reverse()
            if len(dl) < length:
                return []
            else:
                return dl[0:length]
        except:
            return []

    def getStockDailyData( self, ts_code, start_date, end_date ):
        try:
            pro = ts.pro_api( token=TUSHARE_TOKEN )
            df = pro.query( 'daily', ts_code=ts_code, start_date=start_date,
                       end_date=end_date, fields='ts_code,trade_date,open,\
                       high,low,close,pre_close,change,pct_chg,vol,amount')
            #print( df )
            return df
        except:
            a = []
            df = pd.DataFrame( a, columns=['ts_code','trade_date','open',
                                           'high','low','close','pre_close',
                                           'change','pct_chg','vol','amount'],
                             index=np.arange(len(a)))
            return df

    def getTradeCal( self, start_date, end_date ):
        return True

    
    
    