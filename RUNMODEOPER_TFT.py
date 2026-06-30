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
##pcn='PCN-26050966TW'
cnxnlcd = ibm_db.connect("DATABASE=T7WPPT1;HOSTNAME=10.107.1.1;PORT=50101;PROTOCOL=TCPIP;UID=t7wbm1u2;PWD=t7insert;", "", "")
conn=ibm_db_dbi.Connection(cnxnlcd)
SQL_QUERY = f"""
select EQPT_ID||EQPT_RUN_MODE,max(SEQ_NO) from T7WPT1D.ARMOPER
where eqpt_id!=''
group by EQPT_ID||EQPT_RUN_MODE order by 2 desc
"""
df1 = pd.read_sql(SQL_QUERY, conn)
mydicMES_ID_chartlast = dict(zip(df1.iloc[:, 0],df1.iloc[:, 1]))

SQL_QUERY = f"""
select distinct EQPT_ID||EQPT_RUN_MODE||PROC_ID from T7WPT1D.ARMOPER

"""
df2 = pd.read_sql(SQL_QUERY, conn)
alreadyset = set(df2.iloc[:, 0])


# iloc[:, 0] 代表所有列的第一欄，iloc[:, 1] 代表第二欄

MyUpdateSql1=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\mTool4\data\BARMOPER.txt"
MyUpdateSql2=r"Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\mTool4\data\BARMOPER_OPER.txt"


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

sheet_name = sheet_names[2]
df = pd.read_excel(file_path,skiprows=0, dtype=str, sheet_name=sheet_name)
df = df.dropna(how='all').reset_index(drop=True)
df.iloc[:, 0] = df.iloc[:, 0].ffill()
df.iloc[:, 1] = df.iloc[:, 1].ffill()
df['EQPT'] = df.iloc[:, 0]
df['RUNMODE'] = df.iloc[:, 1]
df['PROC_ID'] = df.iloc[:, 2]
df['MYKEY'] = df.iloc[:, 0]+df.iloc[:, 1]
df['MYFULLKEY'] = df.iloc[:, 0]+df.iloc[:, 1]+df.iloc[:, 2]



df=df.fillna('')


sql_outputs = []
txt_outputs = []
mykeylist=[]

for row in df.itertuples(index=False):
    if row.MYFULLKEY not in alreadyset:
        if row.MYKEY not in mykeylist:
            try:
                mynum=int(mydicMES_ID_chartlast[row.MYKEY])+1
            except:
                mynum=1

            temp = (
                        f'" ","{row.EQPT}","{row.RUNMODE}","        ","{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)} {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}",'
                        f'"{pcn}","{result.year}-{str(result.month).zfill(2)}-{str(result.day).zfill(2)} {str(result.hour).zfill(2)}:{str(result.minute).zfill(2)}",'
                        f'"10005034            ","EditComp    ","2026/05/14 13:36","10005034            ","Save        ","2026/05/14 13:36","10005034            ","EditStart   ","2026/05/14 13:33","10005034            ","Release     ","2026/05/14 13:33","10005034            ","EditComp    ","NotInWork   ","WaitForRelease    ","Public      ","10005034            ","      ","{pcn}","                    ","2026-05-14 13:36:13.153276"'

                    )
            txt_outputs.append(temp)
        else:

            mynum+=1
        mykeylist.append(row.MYKEY)

        sql = (
                        f'" ","{row.EQPT}","{row.RUNMODE}","{str(mynum).zfill(2)}","                ","     ","{row.PROC_ID}",{mynum-1}'
                    )

        sql_outputs.append(sql)


with open(MyUpdateSql1, 'w') as f:
    f.write('\n'.join(txt_outputs))
with open(MyUpdateSql2, 'w') as f:
    f.write('\n'.join(sql_outputs))
print(f"處理完成！共生成 {len(sql_outputs)} 筆資料。")
print(f"檔案已儲存至：\n1. {MyUpdateSql1}  {len(txt_outputs)} 筆資料\n2. {MyUpdateSql2}  {len(sql_outputs)} 筆資料")
print("可以IMPORT OR UPDATE!!")



