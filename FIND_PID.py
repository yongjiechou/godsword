import pandas as pd
##PI 禁止PID ((會使機台默停，導致回塞造成耳朵漏光-軟體issue))
##PI 禁止PID：501~549，605~606，704~783

path=r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\temp\find_pid.txt'
df=pd.read_fwf(path)
df=df.fillna('')
df=df.drop([0])
df=df.reset_index(drop=True)
oper_id='4800'##  option input
oper_id=input("please enter your OPER(2100,2200,3000,3270,4100,4600,4800) : ")

mydic={
'2100': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('PIPR','PIRP') and substr(recipe_id,1,1)='0' ORDER BY RECIPE_ID",
'2200': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('TPAB') and substr(recipe_id,1,1)='0' AND PFCD IN (select PFCD from L7WBM1D.BCPRDCT WHERE P_CREATE_DATE>='2010/05/28 13:24') ORDER BY RECIPE_ID",
'3000': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','CSLI','DKRP','DEPK','LCWL') and substr(recipe_id,1,1)='0' ORDER BY RECIPE_ID",
'4800': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('DEPK','BPRS','LION','OWLI') and substr(recipe_id,1,1)='0' ORDER BY RECIPE_ID",
'4100': "select distinct RECIPE_ID  from L7WPT1D.CPARAM WHERE EQPT_ID IN ('PZAT0100','RTPC0100') AND PFCD IN (select PFCD from L7WBM1D.BCPRDCT WHERE P_CREATE_DATE>='2016/05/28 13:24') and recipe_id!=''  ORDER BY RECIPE_ID",
'3270': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('GAPX')  ORDER BY RECIPE_ID",
'3650': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','OWLI')  ORDER BY RECIPE_ID",
'4600': "select distinct RECIPE_ID  from L7WPT1D.CPARAM  WHERE SUBSTR(EQPT_ID,1,4) IN ('LION','OWLI','GAPX','CSLI')  ORDER BY RECIPE_ID"

}

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
print(sorted(canusepid, reverse = False),len(canusepid),sep='\n')
print("==將SQL存成:find_pid.txt==")
print(mydic[oper_id])