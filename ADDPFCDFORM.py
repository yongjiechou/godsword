import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os,json
os.add_dll_directory(r'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi

cnxnlcd = ibm_db.connect("DATABASE=L7WPPT1;HOSTNAME=10.107.1.3;PORT=50301;PROTOCOL=TCPIP;UID=l7wbm1u2;PWD=l7insert;", "", "")

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
target_indices = [0]
all_results = [] # 用來存放每個 Sheet 處理後的結果
pathout=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\data\output.txt"
with open (pathout,'w') as f:
    f.write('')
#第幾隻PFCD
MYNUM=6
myTFTSOURCE=''
myCFSOURCE=''
PFCD10CODE=['1','2','3','4','5','6','7','8','9','A','B','C','D','F','G','H','I','K','L','M','O','R','S','T','U']
for idx in target_indices:
    sheet_name = sheet_names[idx]
    print(f"正在處理：{sheet_name}")

    # 讀取該分頁
    df = pd.read_excel(file_path, dtype=str, sheet_name=sheet_name, header=None)
    df = df.fillna('')
    myTFTSOURCE=str(df.iloc[5,MYNUM]).replace('\n','/')
    myCFSOURCE=str(df.iloc[4,MYNUM]).replace('\n','/')
    myPOL=df.iloc[12,MYNUM]
    myPOLCF=df.iloc[13,MYNUM].replace('\n',' ')
    myPOLTFT=df.iloc[14,MYNUM].replace('\n',' ')

    myPOLCFSQL=myPOLCF.split('-')[1][:4]
    myPOLTFTSQL=myPOLTFT.split('-')[1][:4]
    SQL_QUERY = f"""
select distinct substr(a.pfcd,3,4)||substr(a.pfcd,8,1)||substr(a.pfcd,10,3) PFCD from L7WPT1D.CPRDCTPP A,L7WPT1D.CPARAM B
where A.PFCD=B.PFCD AND
TFPOL_PRODUCT_ID='{myPOLTFTSQL}' AND CFPOL_PRODUCT_ID='{myPOLCFSQL}' AND B.OPE_ID IN ('4000','4100')
"""
    conn=ibm_db_dbi.Connection(cnxnlcd)
    df1 = pd.read_sql(SQL_QUERY, conn)
    PFCDPOLLIST=df1['PFCD'].values.tolist()
##    with open (pathout,'a') as f:
##        f.write(f'{df1}\n')
    SQL_QUERY = f"""
select distinct substr(pfcd,3,4)||substr(pfcd,8,1)||substr(pfcd,10,3) PFCD from L7WBM1D.BCPRDCT_MTRLPRD
where MTRL_PRODUCT_ID in (select MTRL_PRODUCT_ID from L7WBM1D.BCMTRLPRD_SRC
where SRC_PRODUCT_ID in ('{myTFTSOURCE.split('/')[0]}')) and OPE_ID=''
"""
    conn=ibm_db_dbi.Connection(cnxnlcd)
    df1 = pd.read_sql(SQL_QUERY, conn)
    PFCDSOURCELIST=df1['PFCD'].values.tolist()
##    with open (pathout,'a') as f:
##        f.write(f'{df1}\n')
    result = list(set(PFCDPOLLIST) & set(PFCDSOURCELIST))
    result.sort(reverse=True)
##    with open (pathout,'a') as f:
##        f.write(f'{result}\n')
    for PFCD in result:
        SQL_QUERY = f"""
select pfcd from L7WPT1D.CPRDCT
where substr(pfcd,3,4)='{PFCD[:4]}' AND SUBSTR(PFCD,8,1)='{PFCD[4]}' AND SUBSTR(PFCD,10,3)='{PFCD[-3:]}'
except
select distinct pfcd from L7WBM1D.BCPRDCT_AFTCUT
"""
        conn=ibm_db_dbi.Connection(cnxnlcd)
        df1 = pd.read_sql(SQL_QUERY, conn)
        if len(df1)==4:
##            with open (pathout,'a') as f:
##                f.write(f'{PFCD}\n')
            PFCD=df1['PFCD'][1]
            break
    for k in PFCD10CODE:

        SQL_QUERY = f"""
select pfcd from L7WPT1D.CPRDCT
where substr(pfcd,3,4)='{PFCD[2:6]}' AND SUBSTR(PFCD,8,1)='{PFCD[7]}' AND (SUBSTR(PFCD,10,3)='{k}{PFCD[-2:]}' or SUBSTR(PFCD,10,3)='{k}X{PFCD[-1]}')
except
select distinct pfcd from L7WBM1D.BCPRDCT_AFTCUT
"""
        conn=ibm_db_dbi.Connection(cnxnlcd)
        df1 = pd.read_sql(SQL_QUERY, conn)

        if len(df1)==0:
            NEWPFCD=PFCD[:9]+k+PFCD[-2:]
##            with open (pathout,'a') as f:
##                f.write(f'{df1}\n')
            break

    myprinter=f'''
from_cell='L7{PFCD[2:]}'##change
new_cell= 'L7{NEWPFCD[2:]}'##change
real_from_cell=''##change新建不同偏貼 PFCD來源PFCD右邊或者是跨廠-->3
new_cell_unpzat=''##change第11碼X
new_cell_merge=''##change切割後 merge
tft_source='{myTFTSOURCE}'##change
cf_source='{myCFSOURCE}'##change
tft_source_merge=''##change
cf_source_merge=''##change
if new_cell_unpzat!='':    mytype=1 #主線產生未偏貼出貨,有SOURCE TFT CF
elif new_cell_merge!='':    mytype=2 #新玻璃切割後併入
elif tft_source!='':    mytype=0
elif real_from_cell!='':    mytype=3#新建不同偏貼 PFCD,新包材導入
print("select PFCD,ROUTE_ID from L7WPT1D.CPRDCT")
myfrom=['* Start Stage： Before PI','* Start Stage： Before Polarizer','* Start Stage： Before PI','* Start Stage： Before Polarizer']
myto=['* Finish Stage：After LOT2','* Finish Stage：Before Polarizer','* Finish Stage：Before Polarizer','* Finish Stage：After LOT2']
mypzat=["偏光板 {myPOL}","未偏貼出貨","切割後 merge 回原 PFCD","偏光板	{myPOL}"]
mycfpzat=["{myPOLCF}","","","{myPOLCF}"]
mytftpzat=["{myPOLTFT}","","","{myPOLTFT}"]
mycfpzatrwk=["","","",""]
mytftpzatrwk=["","","",""]
my_desc='{df.iloc[0,MYNUM]}{df.iloc[1,MYNUM]}'
'''
    with open (pathout,'a') as f:
        f.write(f'{myprinter}')
