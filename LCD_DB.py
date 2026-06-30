# -*- coding: big5 -*-

import pandas as pd
import os
os.add_dll_directory(r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
##pd.set_option('display.width', None) ##視情況調適欄位對應好看
pd.set_option('display.max_colwidth', None)

cnxnlcd = ibm_db.connect("DATABASE=L7WPPT1;HOSTNAME=10.107.1.3;PORT=50301;PROTOCOL=TCPIP;UID=l7wbm1u2;PWD=l7insert;", "", "")
SQL_QUERY = f"""
select PFCD,ROUTE_ID from L7WPT1D.CPRDCT
"""
conn=ibm_db_dbi.Connection(cnxnlcd)
df1 = pd.read_sql(SQL_QUERY, conn)
pathb=r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\temp\pfcd_route.csv'
df1.to_csv(pathb, index=False)
