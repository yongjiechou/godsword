# -*- coding: big5 -*-
import pandas as pd
import os,json
os.add_dll_directory(r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi
cnxnlcd = ibm_db.connect("DATABASE=L7WPPT1;HOSTNAME=10.107.1.3;PORT=50301;PROTOCOL=TCPIP;UID=l7wbm1u2;PWD=l7insert;", "", "")
conn=ibm_db_dbi.Connection(cnxnlcd)
pathout=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\data\output.txt"


SQL_QUERY = '''
select distinct substr(pfcd,3,4),count(PFCD) from L7WPT1D.CSHEETB
where substr(pfcd,1,1) in ('L','F')
group by substr(pfcd,3,4)
order by 2 desc
'''
df = pd.read_sql(SQL_QUERY, conn)
CSHEETB_L7_list = list(df['1'])
print(CSHEETB_L7_list)
SQL_QUERY = '''
select distinct substr(pfcd,3,4),count(PFCD) from L7WPT1D.CSHEETF
where substr(pfcd,1,1) in ('L','F')
group by substr(pfcd,3,4)
order by 2 desc
'''
df = pd.read_sql(SQL_QUERY, conn)
CSHEETF_LJ_list = list(df['1'])
print(CSHEETF_LJ_list)
SQL_QUERY = '''
select distinct substr(PFCD,3,4) from L7WBM1D.BCPRDCT WHERE P_CREATE_DATE>='2020/01/01 00:00'
'''
df = pd.read_sql(SQL_QUERY, conn)
NEWCREAT_list = list(df['1'])
print(NEWCREAT_list)
result = list(set(CSHEETB_L7_list) | set(CSHEETF_LJ_list)| set(NEWCREAT_list))
print(result)
SQL_QUERY = f"""
select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('PIPR','PIRP') and substr(recipe_id,1,1)='0' AND substr(pfcd,3,4) IN ('{result}') ORDER BY RECIPE_ID
"""
SQL_QUERY=SQL_QUERY.replace("'['","'").replace("']'","'")
print(SQL_QUERY)





mydicPID={
'2100': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('PIPR','PIRP') and substr(recipe_id,1,1)='0' AND substr(pfcd,3,4) IN ('{result}') ORDER BY RECIPE_ID",
'2200': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('TPAB') and substr(recipe_id,1,1)='0' AND substr(pfcd,3,4) IN ('{result}') ORDER BY RECIPE_ID",
'3000': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','CSLI','DKRP','DEPK','LCWL') and substr(recipe_id,1,1)='0' AND substr(pfcd,3,4) IN ('{result}') ORDER BY RECIPE_ID",
'4800': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('DEPK','BPRS','LION','OWLI') and substr(recipe_id,1,1)='0' AND substr(pfcd,3,4) IN ('{result}') ORDER BY RECIPE_ID",
'4100': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM WHERE EQPT_ID IN ('PZAT0100','RTPC0100') AND substr(pfcd,3,4) IN ('{result}')  and recipe_id!=''  ORDER BY RECIPE_ID",
'3270': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('GAPX')  ORDER BY RECIPE_ID",
'3650': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','OWLI')  ORDER BY RECIPE_ID",
'4600': f"select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','OWLI','GAPX','CSLI')  ORDER BY RECIPE_ID"

}
oper_list=['2100','2200','3000','3270','4100','4600','4800']

for oper_id in oper_list:
    SQL_QUERY=mydicPID[oper_id]
    SQL_QUERY=SQL_QUERY.replace("'['","'").replace("']'","'")
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