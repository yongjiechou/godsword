import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os,json
os.add_dll_directory(r'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
import datetime,itertools
result=datetime.datetime.now()

myfilename=r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\work\2022周雍傑週報.xlsx'
df = pd.read_excel(myfilename, sheet_name="7.簽核文件")
r_count,c_count=df.shape
pcn = str(df.iloc[r_count-1, 5]).strip()
##pcn='PCN-26042732TW'
cnxnlcd = ibm_db.connect("DATABASE=F7WPPT1;HOSTNAME=10.107.1.2;PORT=50201;PROTOCOL=TCPIP;UID=f7wbm1u2;PWD=f7insert;", "", "")
conn=ibm_db_dbi.Connection(cnxnlcd)
SQL_QUERY = f"""
SELECT    DISTINCT
    CASE
        WHEN LOCATE('XJ', ONCHID) > 0
             THEN SUBSTR(rtrim(ONCHID), LOCATE('_', ONCHID, LOCATE('XJ', ONCHID)) + 1)
        ELSE ONCHID
    END AS LAST_PART,mes_id
FROM F7WPT1D.BSPC_ONLNCHART
where RUN_MODE='X' and prod in ('XJXXXXXXXX') and data_pat='M'

"""
df1 = pd.read_sql(SQL_QUERY, conn)
mydicMES_ID_chartlast = dict(zip(df1.iloc[:, 0], df1.iloc[:, 1]))

# iloc[:, 0] 代表所有列的第一欄，iloc[:, 1] 代表第二欄
MyUpdateSql2=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\SQL\autouse_cfspcall.sql"
MyUpdateSql3=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\mTool4\data\BSPC_ONLNCHART.txt"


##file_path = r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\download\20260506_E350+SPC+CHART+定義.xlsx'

# 初始化 tkinter，但不顯示主視窗
root = tk.Tk()
root.withdraw()

# 彈出檔案選取視窗
# filetypes 可以限制檔案格式，例如只選取 Excel 或 TXT
file_path = filedialog.askopenfilename(
    title="請選擇檔案",
    filetypes=[("Excel files", "*.xls*"), ("Text files", "*.txt"),  ("All files", "*.*")]
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

sheet_name = sheet_names[4]
df = pd.read_excel(file_path,skiprows=2, dtype=str, sheet_name=sheet_name)
df = df.dropna(how='all').reset_index(drop=True)
df.iloc[:, 1] = df.iloc[:, 1].ffill()
df.iloc[:, 2] = df.iloc[:, 2].ffill()
df['PROCID'] = df.iloc[:, 2]
df['ONCHID'] = df.iloc[:, 6]
df['DATA_GROUP'] = df.iloc[:, 5]
##df['MES_ID'] = df.iloc[:, 8]
df['PEQPTID'] = df.iloc[:, 9]
df['CHARTTYPE'] = df.iloc[:, 19]
df['COWNER'] = df.iloc[:, 20]
df['CHARTGRADE'] = df.iloc[:, 16]
df['ACTIVE'] = df.iloc[:, 36]

RUN_MODE={'':'X','ABN':'A'}
df=df.fillna('')
myoper=list(df.iloc[:, 2].unique())

sql_outputs = []
txt_outputs = []
MYSPCCHARTLIST = []


MYPEQPTLIST=[]

for row in df.itertuples(index=False):
    mychartid=row.ONCHID

    myWER12=row.WER12
    myWER14=row.WER14
    mychartgrade=row.CHARTGRADE
    myPROD = next((p for p in row.ONCHID.split('_') if p.startswith(('FJ', 'TJ','CMO'))), None)

    parts = mychartid.split("_")
    if myPROD and myPROD[:2]=='FJ':
        myLAST = "_".join(parts[[i for i, s in enumerate(parts) if "FJ" in s][0] + 1:]) if any("FJ" in s for s in parts) else "NOT_FOUND"
    elif myPROD and myPROD[:2]=='TJ':
        myLAST = "_".join(parts[[i for i, s in enumerate(parts) if "TJ" in s][0] + 1:]) if any("TJ" in s for s in parts) else "NOT_FOUND"
    elif myPROD and myPROD[:3]=='CMO':
        myLAST = "_".join(parts[[i for i, s in enumerate(parts) if "CMO" in s][0] + 1:]) if any("CMO" in s for s in parts) else "NOT_FOUND"
    try:
        myMES_ID=mydicMES_ID_chartlast[myLAST]
    except:
        myMES_ID=row.MES_ID
        print(f'{myLAST}沒有MES_ID')

    myEQLIST=[]

    mykey=row.ONCHID.split('_')[0]
    peqpt1234=row.PEQPTID[:4]
    if peqpt1234!='':

        for peqpt56 in list(itertools.chain.from_iterable(range(int(p.split('~')[0]), int(p.split('~')[-1]) + 1) for p in row._10.replace('\n',',').split(','))):
            peqpt78=row.PEQPTID.replace('\n',',').split(',')[0][-2:]

            myEQLIST.append(f"{peqpt1234}{int(peqpt56):02d}{int(peqpt78):02d}")
            myEQLIST = list(dict.fromkeys(myEQLIST))
    else:
        myEQLIST=['GLASS_SIZE']
    for myEQPT in myEQLIST:
        mychartid=f'{myEQPT}_{myPROD}_{myLAST}'
        for myrunmode in RUN_MODE:
            if myrunmode!='':
                mychartid=f'ABN_{mychartid}'
                mychartgrade='o'
                myWER12='N'
                myWER14='N'

            if myLAST!='NOT_FOUND' and myPROD :#and row.PROCID=='P620':
                if row.CHARTTYPE not in ['AG','AGMXMN','AGRG','AGRGLG','AGRGMX','AGSD','AGSDLG','AGSDMX','AGSDU1','AGU1','AGU1LG','CX','XX','XXRM','AGMRRG','AGMRSD','AGRGSD','ARGRSD','XXRMMA']:
                    print(f"注意CHART TYPE有誤{row.PROCID}")
                temp = (
                    f'"{mychartid}{"" if (mychartid or "").startswith("ABN") else "    "}","{row.CHARTTYPE}","{row.COWNER}","{row.ONCHID}","CMO01","{myMES_ID}",'
                    f'"{row.DATA_GROUP}","S","M","{row.ACTIVE}","N","{row.ONCHID}","{pcn}","CMO   ",'
                    f'"{"CMO01" if (row.ONCHID or "").startswith("GLASS") or "CMO" in (row.ONCHID or "") else f"{myEQPT[:6]}00"}",'
                    f'"{"CM" if (row.ONCHID or "").startswith("GLASS") or "CMO" in (row.ONCHID or "") else f"{myEQPT[-2:]}"}"'
                    f',"CMO","{row.PROCID if "CMO" in (row.ONCHID or "") else "CMO"}",'
                    f'"{myEQPT if "CMO" in (row.ONCHID or "") else "CMO01"}","CM","CMO","CMO01   ",'
                    f'"{row.SHOLDLOT}","{row.SHOLDEQP}","{"Y" if row.OOS_ABNSHEET else "N"}","N","N","{"Y" if row.OOC_ABNSHEET else "N"}",'
                    f'"N","N","N","P","{row.WER01}","{row.WER02}","{row.WER03}","{row.WER04}","{row.WER05}","{row.WER06}",'
                    f'"{row.WER07}","{row.WER08}","{row.WER09}","{row.WER10}","{row.WER11}","{myWER12}","{row.WER13}","{myWER14}","N","{mychartgrade}"'
                    f',"{pcn}","{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)}'
                    f' {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}:{str(result.second).zfill(2)}.000153","10005034",'
                    f'"{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)}'
                    f' {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}:{str(result.second).zfill(2)}.000276","0001","0001",'
                    f'{row.SPEC上限},{row.SPEC下限},{row._24},{row._28},{row._26},'
                    f'{row._27},{row._31},{row._29},{row._30},{row._34},'
                    f'{row._32},{row._33},"1","2",3,"{myPROD}","P","00","N","N","{RUN_MODE[f"{myrunmode}"]}",'
                    f'"{row.WER16}","N","N","N",0,0,0,"N","N","N",'
                    f'0,0,0,0,0,0,'
                    f'"N","N","{row.OOS_ABNSHEET}","{row.OOC_ABNSHEET}","{row.OOR_ABNSHEET}","","F7","",,"","",0,0,0,"",,,,,,,,,,""'
                )
                sql = (
                    f"UPDATE F7WPT1D.BSPC_ONLNCHART SET ACTIVE='{row.ACTIVE}',SPECSEQ='{pcn}'"
                    f",EDIT_TIME='{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)}"
                    f" {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}:{str(result.second).zfill(2)}.000153'"
                    f",USPEC={row.SPEC上限},LSPEC={row.SPEC下限},TARGET={row._24},UCL1={row._28},LCL1={row._26},CL1={row._27},UCL2={row._31},LCL2={row._29},"
                    f"CL2={row._30},UCL3={row._34},LCL3={row._32},CL3={row._33},ONCHTYPE='{row.CHARTTYPE}',CHARTGRADE='{mychartgrade}' "
                    f"WHERE ONCHID = '{mychartid}' ;"
                )
                txt_outputs.append(temp)
                sql_outputs.append(sql)


with open(MyUpdateSql3, 'w') as f:
    f.write('\n'.join(txt_outputs))
with open(MyUpdateSql2, 'w') as f:
    f.write('\n'.join(sql_outputs))
print(f"處理完成！共生成 {len(sql_outputs)} 筆資料。")
print(f"檔案已儲存至：\n1. {MyUpdateSql3}\n2. {MyUpdateSql2}")
print("可以IMPORT OR UPDATE!!")



