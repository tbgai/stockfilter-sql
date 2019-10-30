#!/bin/bash
nohup python stkdatatrans.py > stockfilter-sql_`date +%Y-%m-%d`.log 2>&1 &
