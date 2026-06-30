import pandas as pd
##myfilename=r'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\work\2022周雍傑週報.xlsx'
##df = pd.read_excel(myfilename, sheet_name="7.簽核文件")
##r_count,c_count=df.shape
##pcn=df.iloc[r_count-1,5]
pcn='PCN-26022535TW'

##print("RTRIM(PFCD)||SUBSTR(EQPT_ID,1,6) IN (select RTRIM(PFCD)||SUBSTR(EQPT_ID,1,6) from L7WBM1D.BCODFPRM WHERE HEADER='')")
path1=r"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\data\excel_file.txt"
with open (path1,'r') as f:
    myfile=f.readlines()

path=fr'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\pcn\{myfile[0][:-1]}.xlsx'

df=pd.read_excel(path)
r_count,c_count=df.shape
df=df.fillna('')
myfrom=myparama=myparamb=myparamc=myparamd=mypshighmin=mypshighmax=mygapa=mygapb=mygapid=myeqpt=mypfcd=mycalid=9999
##print(df)
for i in df.index:
    for j in range(c_count):
        if df.iloc[i,j] in ['變更後','PFCD']:
            myfrom=i+1
        if df.iloc[i,j] in ['PARAM_A']:
            myparama=j
        if df.iloc[i,j]=='EQPT_ID':
            myeqpt=j
        if df.iloc[i,j] in ['PARAM_B']:
            myparamb=j
        if df.iloc[i,j] in ['PARAM_C']:
            myparamc=j
        if df.iloc[i,j] in ['PARAM_D']:
            myparamd=j
        if df.iloc[i,j] in ['MIN_LC','MIN_CF_PS_HEIGHT']:
            mypshighmin=j
        if df.iloc[i,j] in ['MAX_LC','MAX_CF_PS_HEIGHT']:
            mypshighmax=j
        if df.iloc[i,j] in ['GAP Param A']:
            mygapa=j
        if df.iloc[i,j] in ['GAP Param B']:
            mygapb=j
        if df.iloc[i,j] in ['GAP Logic ID']:
            mygapid=j
        if df.iloc[i,j] in ['PFCD']:
            mypfcd=j
        if df.iloc[i,j] in ['CALC_LOGIC_ID']:
            mycalid=j
print(myfrom,myeqpt,mypfcd,myparama,myparamb,myparamc,mypshighmin,mypshighmax,mycalid,myparamd,mygapa,mygapb,mygapid)
df[mypfcd] = df[mypfcd].apply(lambda x: str(x).replace(' ',''))
MyUpdateSql1=r"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\SQL\autouse_aff.sql"
with open (MyUpdateSql1,'w') as f:
    f.write('')
for i in df.index:
    if i >= myfrom and df.iloc[i,myeqpt][:4]=='TPAB':
        df.iloc[i,0]=f"UPDATE L7WBM1D.BCODFPRM SET P_COMMENT='{pcn}',\
PARAM_A='{df.iloc[i,myparama]}',PARAM_B='{df.iloc[i,myparamb]}',PARAM_C='{df.iloc[i,myparamc]}',PARAM_D='{round(float(df.iloc[i,myparamd]),15)}',MIN_CF_PS_HEIGHT='{df.iloc[i,mypshighmin]}',\
MAX_CF_PS_HEIGHT='{df.iloc[i,mypshighmax]}',P_SETUP_STATE='WaitForRelease    ',HEADER='',GAP_PARM_A='{df.iloc[i,mygapa]}',GAP_PARM_B='{df.iloc[i,mygapb]}',GAP_LOGIC_ID='{df.iloc[i,mygapid]}',CALC_LOGIC_ID='{df.iloc[i,mycalid]}'\
 WHERE SUBSTR(EQPT_ID,1,6)='{df.iloc[i,myeqpt][0:6]}' AND PFCD='{df.iloc[i,mypfcd]}';"

        with open (MyUpdateSql1,'a') as f:
            f.write(df.iloc[i,0])
            f.write('\n')
MyNewSql1=r"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\mTool4\data\BCODFPRM.txt"
with open (MyNewSql1,'w') as f:
    f.write('')
for i in df.index:
    if i >= myfrom and df.iloc[i,myeqpt][:4]=='TPAB':
        df.iloc[i,0]=f'"R","{df.iloc[i,myeqpt][:6]}00","{df.iloc[i,mypfcd]}","{df.iloc[i,myparama]}","{df.iloc[i,myparamb]}","{df.iloc[i,myparamc]}","{round(float(df.iloc[i,myparamd]),15)}","{df.iloc[i,mypshighmin]}","{df.iloc[i,mypshighmax]}",\
"{df.iloc[i,mycalid]}","        ","2007/07/26 09:52","139199              ","2020/05/05 14:13","10005034            ","Release     ","2020/04/30 16:20","10005034            ","Release     ","2019/11/08 11:54","10005034            ","Release     ","2017/10/25 15:41","10005034            ","Release     ","2017/10/25 15:40","10005034            ","EditComp    ","NotInWork   ","Released          ","Public      \
","139199              ","      ","{pcn}","                    ","2017-10-25 15:39:41.321752",\
"{df.iloc[i,mygapa]}","{df.iloc[i,mygapb]}","{df.iloc[i,mygapid]}"'

        with open (MyNewSql1,'a') as f:
            f.write(df.iloc[i,0])
            f.write('\n')
path=fr'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\pcn\{myfile[1][:-1]}.xlsx'

df=pd.read_excel(path,skiprows=0,usecols='a:z',dtype=str,header=None)
r_count,c_count=df.shape
df=df.fillna('')
print(df[2])
toprint=f'''*****************
直接IMPORT UPDATE
再update
再DEL RTABLE 後在BRM RELEASE
RTRIM(PFCD)||SUBSTR(EQPT_ID,1,6) IN (select RTRIM(PFCD)||SUBSTR(EQPT_ID,1,6) from L7WBM1D.BCODFPRM WHERE HEADER='')
{pcn}
'''
print(toprint)