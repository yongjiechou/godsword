import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os,json
os.add_dll_directory(r'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
import datetime
result=datetime.datetime.now()

myfilename=r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\work\2022周雍傑週報.xlsx'
df = pd.read_excel(myfilename, sheet_name="7.簽核文件")
r_count,c_count=df.shape
pcn = str(df.iloc[r_count-1, 5]).strip()
##pcn='PCN-26041422TW'
cnxnlcd = ibm_db.connect("DATABASE=L7WPPT1;HOSTNAME=10.107.1.3;PORT=50301;PROTOCOL=TCPIP;UID=l7wbm1u2;PWD=l7insert;", "", "")
conn=ibm_db_dbi.Connection(cnxnlcd)
SQL_QUERY = f"""
select DISTINCT pfcd||ope_id,MES_ID from L7WPT1D.CPARAM WHERE
OPE_ID IN ('2130','2100','2200','2210','3270','3000','4100','4000','3620','2700','2800','3670')
"""
df1 = pd.read_sql(SQL_QUERY, conn)
# iloc[:, 0] 代表所有列的第一欄，iloc[:, 1] 代表第二欄
mydic = dict(zip(df1.iloc[:, 0], df1.iloc[:, 1]))

SQL_QUERY = f"""
SELECT DATA_GROUP, CHARTLAST, TOTAL_COUNT
FROM (
    SELECT
        RTRIM(DATA_GROUP) AS DATA_GROUP,
        RTRIM(SUBSTR(ONCHID, LOCATE('_', ONCHID, LOCATE('_', ONCHID) + 1) + 1)) AS CHARTLAST,
        COUNT(*) AS TOTAL_COUNT,
        -- 核心邏輯：在每個 DATA_GROUP 內按數量排序並編號
        ROW_NUMBER() OVER(PARTITION BY DATA_GROUP ORDER BY COUNT(*) DESC) AS RN
    FROM L7WPT1D.CSPC_ONLNCHART
    WHERE SUBSTR(SPECSEQ, 1, 3) = 'PCN'
      AND ACTIVE = 'Y'
      --AND DATA_GROUP IN ('H01_LC_mass_Bf_F', 'AU Shift_Y')
    GROUP BY DATA_GROUP, RTRIM(SUBSTR(ONCHID, LOCATE('_', ONCHID, LOCATE('_', ONCHID) + 1) + 1))
) AS TEMP
WHERE RN = 1  -- 只取出每個分組的第一名（數量最大者）
ORDER BY DATA_GROUP;

"""
df2 = pd.read_sql(SQL_QUERY, conn)
mydicdatagroup_chartlast = dict(zip(df2.iloc[:, 0], df2.iloc[:, 1]))
SQL_QUERY = f"""
select distinct rtrim(SUBSTR(ONCHID, LOCATE('_', ONCHID, LOCATE('_', ONCHID) + 1) + 1)) CHARTLAST
from L7WPT1D.CSPC_ONLNCHART
where substr(specseq,1,3)='PCN' and active='Y'
"""
df2 = pd.read_sql(SQL_QUERY, conn)
mychartlast_set=set(df2.iloc[:,0])

cnxnedclcd = ibm_db.connect("DATABASE=L7HEDC1;HOSTNAME=10.107.1.6;PORT=50602;PROTOCOL=TCPIP;UID=p7cimu1;PWD=p7cimu1;", "", "")
SQL_QUERY = f"""
SELECT DISTINCT
    SUBSTR(A.ONCHID, LOCATE('_', A.ONCHID, LOCATE('_', A.ONCHID) + 1) + 1) AS NEW_ONCHID
FROM L7HEC1D.HCMSPARA A, L7HEC1D.HCMSGLSINFO B
WHERE A.SEQ = B.SEQ
  AND a.data_group = 'G_CGI_L4_Dn_W'

"""
##conn=ibm_db_dbi.Connection(cnxnedclcd)
##df2 = pd.read_sql(SQL_QUERY, conn)


# 初始化 tkinter，但不顯示主視窗
root = tk.Tk()
root.withdraw()

# 彈出檔案選取視窗
# filetypes 可以限制檔案格式，例如只選取 Excel 或 TXT
file_path = filedialog.askopenfilename(
    title="請選擇檔案",
    filetypes=[("Excel files", "*.xlsx"), ("Text files", "*.txt"),  ("All files", "*.*")]
)
try:
    if file_path:
        print(f"你選擇的檔案路徑是：{file_path}")
    else:
        print("使用者取消了選取")
except OSError as e:
    print(e)
excel_file = pd.ExcelFile(file_path)
sheet_names = excel_file.sheet_names
print(sheet_names)

MyUpdateSql1=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\SQL\autouse_lcdspc.sql"

MyNewSql1=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\mTool4\data\CSPC_ONLNCHART.txt"

# 1. 定義你要處理的 Sheet 索引
target_indices = [0]
all_results = [] # 用來存放每個 Sheet 處理後的結果

for idx in target_indices:
    sheet_name = sheet_names[idx]
    print(f"正在處理：{sheet_name}")

    # 讀取該分頁
    df = pd.read_excel(file_path, dtype=str, sheet_name=sheet_name)

    # 前處理：刪除全空列、補齊合併儲存格
    df = df.dropna(how='all').reset_index(drop=True)
    df.iloc[:, 1] = df.iloc[:, 1].ffill()
    df.iloc[:, 2] = df.iloc[:, 2].ffill()
    df.iloc[:, 0] = df.iloc[:, 0].ffill()
    df.iloc[:, 3] = df.iloc[:, 3].ffill()
    df.iloc[:, 18] = df.iloc[:, 18].ffill()
    df.iloc[:, 19] = df.iloc[:, 19].ffill()
    df.iloc[:, 20] = df.iloc[:, 20].ffill()
    df.iloc[:, 21] = df.iloc[:, 21].ffill()
    df.iloc[:, 22] = df.iloc[:, 22].ffill()
    df.iloc[:, 23] = df.iloc[:, 23].ffill()
    df=df.fillna('')
    df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.replace('_X_X', '_X', regex=False)
    df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.replace('_Y_Y', '_Y', regex=False)
    df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.replace('_Y_X', '_Y', regex=False)
    df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.replace(')_X', ')', regex=False)
    df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.replace('_EDC', '', regex=False)
    df.iloc[:, 6] = df.iloc[:, 6].astype(str).str.replace('Vernier', 'vernier', regex=False)
    df.iloc[:, 10] = df.iloc[:, 10].astype(str).str.replace('1', 'A', regex=False)
    df.iloc[:, 10] = df.iloc[:, 10].astype(str).str.replace('0', 'o', regex=False)
    df.iloc[:, 10] = df.iloc[:, 10].astype(str).str.replace('O', 'o', regex=False)
    df.iloc[:, 8] = df.iloc[:, 8].astype(str).str.replace('P', 'M', regex=False)
    df['製程站點'] = df.iloc[:, 1]
    df['量測站點'] = df.iloc[:, 2]
    df['PFCD'] = df.iloc[:, 3]
    df['DATA_GROUP'] = df.iloc[:, 6]
    df['ACTIVE'] = df.iloc[:, 7]
    df['DATA_PAT'] = df.iloc[:, 8]
    df['CHARTGRADE'] = df.iloc[:, 10]
    df['SHOLDLOT'] = df.iloc[:, 11]
    df['SHOLDEQP'] = df.iloc[:, 12]
    df['SALARM'] = df.iloc[:, 13]
    df['AVGTYPE'] = df.iloc[:, 14]
    df['SIGMATYPE'] = df.iloc[:, 15]
    df['SAMPLECNT'] = df.iloc[:, 16]
    df['ONCHID'] = df.iloc[:, 17]
    df['PEQPTSUB'] = df.iloc[:, 18]
    df['PEQPTMAIN'] = df.iloc[:, 19]
    df['PEQPTMAINSUB'] = df.iloc[:, 20]
    df['EQPTSUB'] = df.iloc[:, 21]
    df['EQPTMAIN'] = df.iloc[:, 22]
    df['EQPTMAINSUB'] = df.iloc[:, 23]
    df['ONCHTYPE'] = df.iloc[:, 24]
    df['COWNER'] = df.iloc[:, 25]
    df['USPEC'] = df.iloc[:, 27]
    df['UCL1'] = df.iloc[:, 28]
    df['TARGET'] = df.iloc[:, 29]
    df['CL1'] = df.iloc[:, 30]
    df['LCL1'] = df.iloc[:, 31]
    df['LSPEC'] = df.iloc[:, 32]
    df['UCL2'] = df.iloc[:, 35]
    df['CL2'] = df.iloc[:, 36]
    df['LCL2'] = df.iloc[:, 37]
    df['UCL3'] = df.iloc[:, 38]
    df['CL3'] = df.iloc[:, 39]
    df['LCL3'] = df.iloc[:, 40]
    df = df.assign(**{f'WER{i:02d}': df.iloc[:, 40 + i] for i in range(1, 17)})
    df['OOS_ABNSHEET'] = df.iloc[:, 57]
    df['OOC_ABNSHEET'] = df.iloc[:, 58]
    df['OOR_ABNSHEET'] = df.iloc[:, 59]
    df['mykey'] = df['ONCHID'].str.split('_').str[0]
    # 針對所有字串欄位移除頭尾空格與換行符號
##    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    # 建議寫法：將檔案開啟放在迴圈外

    myrptunitdata='S'#REP_UNIT

    sql_outputs = []
    txt_outputs = []
    MYSPCCHARTLIST = []


    for row in df.itertuples(index=False):
        mykey=row.ONCHID.split('_')[0]
        mychartlast='_'.join(row.ONCHID.split('\n')[0].split('_')[2:])
        myCOWNER=row.COWNER
        myDATA_GROUP=row.DATA_GROUP
        myDATA_PAT=row.DATA_PAT
        myACTIVE=row.ACTIVE
        mySHOLDLOT=row.SHOLDLOT
        mySHOLDEQP=row.SHOLDEQP
        mySALARM=row.SALARM
        myCHARTGRADE=row.CHARTGRADE
        myUSPEC=row.USPEC
        myLSPEC=row.LSPEC
        myTARGET=row.TARGET
        myUCL1=row.UCL1
        myLCL1=row.LCL1
        myCL1=row.CL1
        myUCL2=row.UCL2
        myLCL2=row.LCL2
        myCL2=row.CL2
        myUCL3=row.UCL3
        myLCL3=row.LCL3
        myCL3=row.CL3
        myAVGTYPE=row.AVGTYPE
        mySIGMATYPE=row.SIGMATYPE
        mySAMPLECNT=row.SAMPLECNT
        mySAMPLECNT=row.SAMPLECNT
        myOOS_ABNSHEET=row.OOS_ABNSHEET
        myOOC_ABNSHEET=row.OOC_ABNSHEET
        myOOR_ABNSHEET=row.OOR_ABNSHEET
        myWER01=row.WER01
        myWER02=row.WER02
        myWER03=row.WER03
        myWER04=row.WER04
        myWER05=row.WER05
        myWER06=row.WER06
        myWER07=row.WER07
        myWER08=row.WER08
        myWER09=row.WER09
        myWER10=row.WER10
        myWER11=row.WER11
        myWER12=row.WER12
        myWER13=row.WER13
        myWER14=row.WER14
        myWER15=row.WER15
        myWER16=row.WER16
        myINSPEQ='CMO01'
        myPROD='CMO'
        myEQPTSUB='CM'
        if len(str(row.DATA_GROUP)) >16 and row.DATA_GROUP!='EDC ITEM\nDATA_GROUP':
            print(f"{row.DATA_GROUP} 測項超過系統16碼限制")


        if str(row.量測站點) in ['2130','2100','2200','3270','2210','3620','3000','4100','2700','3600','2800','4000','3670','4100\n4000','4000\n4100'] : # 你的判斷式
##        if str(row.量測站點) in ['2200'] : # 你的判斷式

            myPFCDlist=row.PFCD.split('\n')
            myPFCDlist = [item for item in myPFCDlist if item[0] in ['L','F']]
            myEQLIST=[]
            eqerrflag=True
            for myPFCD in myPFCDlist:
##                myEQLIST=[f"{row.PEQPTSUB[:4]}{k:02d}{row.PEQPTSUB[-2:].replace('XX','00')}" for k in range(int(row.PEQPTMAIN.split('~')[0]), int(row.PEQPTMAIN.split('~')[-1]) + 1)]

                myeq1234=row.PEQPTSUB[:4]
                if myeq1234 !=mykey[:4] and eqerrflag:
                    print(f"機台填寫錯誤{myeq1234}")
                    eqerrflag=False

                if '~' in row.PEQPTMAIN and '~' in row.PEQPTSUB:
                    for myeq56 in range(int(row.PEQPTMAIN.split('~')[0]), int(row.PEQPTMAIN.split('~')[-1]) + 1):
                        for myeq78 in range(int(row.PEQPTSUB.split('~')[0][-2:]), int(row.PEQPTSUB.split('~')[-1]) + 1):
                            myEQLIST.append(f"{myeq1234}{myeq56:02d}{myeq78:02d}")
                            myEQLIST = list(dict.fromkeys(myEQLIST))
                if ',' in row.PEQPTMAIN and '~' in row.PEQPTSUB:
                    for myeq56 in row.PEQPTMAIN.split(','):
                        for myeq78 in range(int(row.PEQPTSUB.split('~')[0][-2:]), int(row.PEQPTSUB.split('~')[-1]) + 1):
                            myEQLIST.append(f"{myeq1234}{int(myeq56):02d}{myeq78:02d}")
                            myEQLIST = list(dict.fromkeys(myEQLIST))
                if '~' in row.PEQPTMAIN and '~' not in row.PEQPTSUB:
                    for myeq56 in range(int(row.PEQPTMAIN.split('~')[0]), int(row.PEQPTMAIN.split('~')[-1]) + 1):
                        myeq78 = row.PEQPTSUB[-2:].replace('XX','00')
                        myEQLIST.append(f"{myeq1234}{myeq56:02d}{int(myeq78):02d}")
                        myEQLIST = list(dict.fromkeys(myEQLIST))
                if '~' not in row.PEQPTMAIN and '~' not in row.PEQPTSUB and ',' not in row.PEQPTMAIN and myeq1234!='NPLI':
                    myeq56=row.PEQPTMAIN
                    myeq78=row.PEQPTSUB[-2:]
                    myEQLIST.append(f"{myeq1234}{int(myeq56):02d}{int(myeq78):02d}")
                if '~' not in row.PEQPTMAIN and '~' not in row.PEQPTSUB and ',' not in row.PEQPTMAIN and myeq1234=='NPLI':
                    myeq56='01'
                    myeq78=row.PEQPTMAIN
                    myEQLIST.append(f"{myeq1234}{int(myeq56):02d}{int(myeq78):02d}")
                if myeq1234=='NPLI':
                    myeq56='01'
                    if ',' in row.PEQPTMAIN:
                        for myeq78 in row.PEQPTMAIN.split(','):
                            myEQLIST.append(f"{myeq1234}{int(myeq56):02d}{int(myeq78):02d}")
                    else:
                        myeq78==row.PEQPTSUB[-2:]



                for myEQPT in myEQLIST:
                    if myEQPT[-2:]=='00':
                        myEQPTSUB='CM'
                        myPROCEQ=myEQPT
                    else:
                        myEQPTSUB=myEQPT[-2:]
                        myPROCEQ=f"{myEQPT[:6]}00"

                    if row.量測站點=='2210':
                        myPFCDPID='LJ'+myPFCD.replace(' ','')[2:12]+f'{row.量測站點}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD=myPFCD
                        myPFCDTOCHART=myPFCD
                        myCTOOLID='AAPK0100'
                        myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                    elif row.量測站點=='3000':
                        myPFCDPID='LJ'+myPFCD.replace(' ','')[2:12]+f'{row.量測站點}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD='CMO'
                        myPFCDTOCHART=myPFCD[2:6]+mymes_id[-2:].replace('00','')
                        myCTOOLID=myEQPT[:6]+row.EQPTSUB[-2:]
                        if mychartlast in mychartlast_set:
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        else:
                            mychartlast=mydicdatagroup_chartlast[f'{myDATA_GROUP}']
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                    elif row.量測站點=='2130':

                        myPFCDPID=myPFCD.replace(' ','')+f'{row.量測站點}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD='CMO'
                        myPFCDTOCHART=myPFCD[2:6]
                        myCTOOLID='AOIX0100'
                        myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        if len(mykey)==6:
                            mychartlast='_'.join(row.ONCHID.split('\n')[0].split('_')[1:])
                            myonchidKEY=f'{myEQPT[:6]}_{mychartlast}'
                    elif row.量測站點=='2100':

                        myPFCDPID=myPFCD.replace(' ','')+f'{row.量測站點}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD='CMO'
                        myPFCDTOCHART=myPFCD[2:6]
                        myCTOOLID=f"{myEQPT[:6]}07"
                        myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                    elif row.量測站點=='2200':

                        myPFCDPID=myPFCD.replace(' ','')+f'{row.量測站點}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD='CMO'
                        myPFCDTOCHART=myPFCD[2:6]
                        myCTOOLID=f"{myEQPT}"
                        if myDATA_GROUP[:2]=='M0':
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        elif mychartlast in mychartlast_set and myDATA_GROUP[:2]!='M0':
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        else:
                            mychartlast=mydicdatagroup_chartlast[f'{myDATA_GROUP}']
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'

                        if row.PEQPTSUB==row.EQPTSUB:
                            myPROCEQ='CMO01'
                            myEQPTSUB='CM'
                            myINSPEQ=myEQPT

                    elif row.量測站點 in ['4100','4000','4100\n4000','4000\n4100']:
                        myPFCDPID=myPFCD.replace(' ','')+f'{row.量測站點[:4]}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD='CMO'
                        myPFCDTOCHART=myPFCD[2:6]+mymes_id[-2:].replace('00','')
                        if mykey!=row.PEQPTSUB:
                            myCTOOLID=myEQPT[:6]+mykey[-2:]
                            myEQPT=myEQPT[:6]+mykey[-2:]
                            myEQPTSUB='CM'
                        else:
                            myCTOOLID=myEQPT[:6]+row.EQPTSUB[-2:]


                        if mychartlast in mychartlast_set:
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        else:
                            mychartlast=mydicdatagroup_chartlast[f'{myDATA_GROUP}']
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        if row.PEQPTSUB==row.EQPTSUB:
                            myEQPTSUB='CM'
                    elif row.量測站點=='2700':

                        myPFCDPID=myPFCD.replace(' ','')+f'{row.量測站點}'
                        mymes_id=mydic[myPFCDPID]
                        myPROD='CMO'
                        myPFCDTOCHART=myPFCD[2:6]
                        myCTOOLID=myEQPT[:6]+row.EQPTSUB[-2:]
                        if mychartlast in mychartlast_set:
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        else:
                            mychartlast=mydicdatagroup_chartlast[f'{myDATA_GROUP}']
                            myonchidKEY=f'{myEQPT}_{myPFCDTOCHART}_{mychartlast}'
                        if row.PEQPTSUB==row.EQPTSUB:
                            myEQPTSUB='CM'

                    temp = (
                        f'"{myonchidKEY}","{row.ONCHTYPE}","{myCOWNER}","{myonchidKEY}","{myCTOOLID}","{mymes_id}",'
                        f'"{myDATA_GROUP}","{myrptunitdata}","{myDATA_PAT}","{myACTIVE}","N","{myonchidKEY}","{pcn}","CMO","{myPROCEQ}"'
                        f',"{myEQPTSUB}","CMO","CMO   ","{myINSPEQ}","CM","CMO","CMO01   ","{mySHOLDLOT}","{mySHOLDEQP}","{mySALARM}","N","N","Y","N","N","Y","P",'
                        f'"{myWER01}","{myWER02}","{myWER03}","{myWER04}","{myWER05}","{myWER06}","{myWER07}","{myWER08}","{myWER09}","{myWER10}","{myWER11}"'
                        f',"{myWER12}","{myWER13}","{myWER14}","{myWER15}","{myCHARTGRADE}","{pcn}","{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)}'
                        f' {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}:{str(result.second).zfill(2)}.000153","10005034","'
                        f'{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)}'
                        f' {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}:{str(result.second).zfill(2)}.000153","0001","0001",'
                        f'{myUSPEC},{myLSPEC},{myTARGET},{myUCL1},{myLCL1},{myCL1},{myUCL2},{myLCL2},{myCL2},{myUCL3},{myLCL3},{myCL3},'
                        f'"{myAVGTYPE}","{mySIGMATYPE}",{mySAMPLECNT},"{myPROD}","P"," ","00","N","N","X","{myWER16}","N","N","N",0,0,0,"N","N","N",0,0,0,0,0,0,"N","N",'
                        f'"{myOOS_ABNSHEET}","{myOOC_ABNSHEET}","{myOOR_ABNSHEET}","","L7","",,"",0,0,0,"",,,,,,,,,,""'
                    )
                    if myonchidKEY not in MYSPCCHARTLIST:
                        txt_outputs.append(temp)
##                    sql = (
##                        f"UPDATE L7WPT1D.CSPC_ONLNCHART SET ACTIVE='{row.ACTIVE}',SPECSEQ='{pcn}',CHARTGRADE='{row.CHARTGRADE}',"
##                        f"ONCHTYPE='{row.ONCHTYPE}', TARGET={row.TARGET},USPEC={row.USPEC},LSPEC={row.LSPEC},"
##                        f"CL1={row.CL1},UCL1={row.UCL1},LCL1={row.LCL1},CL2={row.CL2},UCL2={row.UCL2},LCL2={row.LCL2},"
##                        f"OOS_ABNSHEET='{row.OOS_ABNSHEET}',OOC_ABNSHEET='{row.OOC_ABNSHEET}',OOR_ABNSHEET='{row.OOR_ABNSHEET}',"
##                        f"SHOLDEQP='{row.SHOLDEQP}',SALARM='{row.SALARM}',CL3={row.CL3},UCL3={row.UCL3},LCL2={row.LCL3} "
##                        f"WHERE REP_UNIT='{myrptunitdata}' and ONCHTYPE='{row.ONCHTYPE}' and DATA_GROUP='{row.DATA_GROUP}' AND "
##                        f"MES_ID='{mymes_id}' and prod='{myPROD}' and PEQPT_ID='{myEQPT[:6]}00';"
##                    )
                    sql = (
                        f"UPDATE L7WPT1D.CSPC_ONLNCHART SET ACTIVE='{row.ACTIVE}',EDIT_USER='{pcn}',SPECSEQ='{pcn}',CHARTGRADE='{row.CHARTGRADE}',"
                        f"ONCHTYPE='{row.ONCHTYPE}', TARGET={row.TARGET},USPEC={row.USPEC},LSPEC={row.LSPEC},"
                        f"CL1={row.CL1},UCL1={row.UCL1},LCL1={row.LCL1},CL2={row.CL2},UCL2={row.UCL2},LCL2={row.LCL2},"
                        f"OOS_ABNSHEET='{row.OOS_ABNSHEET}',OOC_ABNSHEET='{row.OOC_ABNSHEET}',OOR_ABNSHEET='{row.OOR_ABNSHEET}',"
                        f"SHOLDEQP='{row.SHOLDEQP}',SALARM='{row.SALARM}',CL3={row.CL3},UCL3={row.UCL3},LCL3={row.LCL3} "
                        f"WHERE ONCHID='{myonchidKEY}';"
                    )
                    if myonchidKEY not in MYSPCCHARTLIST:
                        sql_outputs.append(sql)

                    MYSPCCHARTLIST.append(myonchidKEY)
    with open(MyNewSql1, 'w') as f:
        f.write('\n'.join(txt_outputs))
    with open(MyUpdateSql1, 'w') as f:
        f.write('\n'.join(sql_outputs))


SQL_QUERY1 = f"select distinct pfcd,mes_id from L7WPT1D.CPARAM where pfcd in ('{set(df.iloc[:,3])}') and ope_id in('{set(df.iloc[:,2])}')"
SQL_QUERY1=SQL_QUERY1.replace("'{'","'").replace("'}'","'").replace("\\n","','")
conn=ibm_db_dbi.Connection(cnxnlcd)
df1 = pd.read_sql(SQL_QUERY1, conn)
print(df1)
myprinter=f'''
SELECT RTRIM(MES_ID)||'&'||RTRIM(DATA_GROUP)||'&'||RTRIM(data_pat)||'&'||substr(peqpt_id,1,6)||PSUBENTITY FROM L7WPT1D.CSPC_ONLNCHART
WHERE  specseq='{pcn}'
EXCEPT
select RTRIM(MES_ID)||'&'||RTRIM(DATA_GROUP)||'&'||RTRIM(data_pat)||'&'||eqpt_id from L7WPT1D.CMLITEM
where USE_TCS_LABEL_FLG='N'
'''
print(f'add_data_group1.txt:{myprinter}')
print(f"處理完成！共生成 {len(sql_outputs)} 筆資料。")
print(f"檔案已儲存至：\n1. {MyUpdateSql1}\n2. {MyNewSql1}")
print("可以IMPORT OR UPDATE!!")