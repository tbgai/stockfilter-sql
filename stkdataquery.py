# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 22:12:39 2019

@author: jingzl
"""

import MySQLdb

def connectdb():
    db = MySQLdb.connect(host="47.104.252.239", port=33060, user="root", passwd="mysql.1q2", db="stkdata", charset='utf8' )
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : ", data)
    db.close()

def querydata():
    pass

def savedata():
    pass


if __name__ == '__main__':
    connectdb()
    querydata()
    savedata()
    







