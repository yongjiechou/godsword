# -*- coding: big5 -*-
import pandas as pd
import os,json
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
mydic=dict(zip(df1['PFCD'],df1['ROUTE_ID']))
path=r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\temp\pfcd_route.json'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(mydic, f, ensure_ascii=False, indent=4)

pathout=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\data\output.txt"
with open(pathout, 'r', encoding='utf-8') as f:
    SQL_QUERY = f.read()  # 全部讀取成一個大字串
df2 = pd.read_sql(SQL_QUERY, conn)
mydic2=dict(zip(df2['OPE_ID'],df2['RECIPE_ID']))
path2=r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\temp\pfcd_pid.json'
with open(path2, 'w', encoding='utf-8') as f:
    json.dump(mydic2, f, ensure_ascii=False, indent=4)


mydicPID={
'2100': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('PIPR','PIRP') and substr(recipe_id,1,1)='0' ORDER BY RECIPE_ID",
'2200': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('TPAB') and substr(recipe_id,1,1)='0' AND PFCD IN (select PFCD from L7WBM1D.BCPRDCT WHERE P_CREATE_DATE>='2010/05/28 13:24') ORDER BY RECIPE_ID",
'3000': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','CSLI','DKRP','DEPK','LCWL') and substr(recipe_id,1,1)='0' ORDER BY RECIPE_ID",
'4800': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('DEPK','BPRS','LION','OWLI') and substr(recipe_id,1,1)='0' ORDER BY RECIPE_ID",
'4100': "select distinct RECIPE_ID  from L7WPT1D.CPARAM WHERE EQPT_ID IN ('PZAT0100','RTPC0100') AND PFCD IN (select PFCD from L7WBM1D.BCPRDCT WHERE P_CREATE_DATE>='2016/05/28 13:24') and recipe_id!=''  ORDER BY RECIPE_ID",
'3270': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('GAPX')  ORDER BY RECIPE_ID",
'3650': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','OWLI')  ORDER BY RECIPE_ID",
'4600': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','OWLI','GAPX','CSLI')  ORDER BY RECIPE_ID"

}
oper_list=['2100','2200','3000','3270','4100','4600','4800']

for oper_id in oper_list:
    SQL_QUERY=mydicPID[oper_id]
    df = pd.read_sql(SQL_QUERY, conn)

    mylist=[]
    pidlist=[]
    canusepid=[]

    if oper_id=='4100':
        for i in range(1,400):
            mylist.append(str(i).zfill(4))

    elif oper_id=='2100':
        for i in range(100,1000):
            if i%2==0 and i<500 :
                mylist.append(str(i).zfill(4))
    elif oper_id=='3000':
        for i in range(100,1000):
            if i%2==0  :
                mylist.append(str(i).zfill(4))
    elif oper_id=='2200':
        for i in range(100,800):
            if i not in range(320,326):
                mylist.append(str(i).zfill(4))
    elif oper_id=='4800':
        for i in range(100,800):
            mylist.append(str(i).zfill(4))
    elif oper_id=='3270':
        for i in range(100,300):
            mylist.append(str(i).zfill(4))
    elif oper_id=='3650':
        for i in range(400,600):
            mylist.append(str(i).zfill(4))
    elif oper_id=='4600':
        for i in range(100,900):
            mylist.append(str(i).zfill(4))


    if oper_id=='3000':
        for i in df.index:
            if i>=df.index[0] and int(df.iloc[i,0])%2==0:
                pidlist.append(df.iloc[i,0])
            elif i>=df.index[0] and int(df.iloc[i,0])%2==1:
                pidlist.append(str(int(df.iloc[i,0])+1).zfill(4))
    else:
        for i in df.index:
            if i>=df.index[0] and i<=df.index[-1]:
                pidlist.append(df.iloc[i,0])
    canusepid=list(set(mylist)-set(pidlist))
    with open (pathout,'a', encoding='utf-8') as f:
        print(f'{oper_id}可用PID:{len(canusepid)}個',file=f)
        print(sorted(canusepid, reverse = False),sep='\n',file=f)

