import pandas as pd
import os,json
os.add_dll_directory(r'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin')
import ibm_db
import ibm_db_dbi

cnxnlcd = ibm_db.connect("DATABASE=L7WPPT1;HOSTNAME=10.107.1.3;PORT=50301;PROTOCOL=TCPIP;UID=l7wbm1u2;PWD=l7insert;", "", "")
SQL_QUERY = f"""
select substr(PFCD,3,4)||substr(PFCD,8,1)||substr(PFCD,10,3) PFCD from L7WPT1D.CPRDCT
"""
conn=ibm_db_dbi.Connection(cnxnlcd)
df = pd.read_sql(SQL_QUERY, conn)
existing_pfcds = set(df["PFCD"].dropna())

try:
    while True:
        user_input = input("請輸入 12 碼 PFCD：").upper()

        # 基本格式檢查
        if len(user_input) != 12 or not user_input.startswith("L7"):
            print("格式錯誤：必須為 L7 開頭且共 12 碼。")
            continue

        # 檢查是否重複 (使用 set 進行 O(1) 高速比對)
        if user_input[2:6]+user_input[7]+user_input[9:] in existing_pfcds:
            print(f"錯誤：*{user_input[2:6]}*{user_input[7]}*{user_input[9:]}* 已經被使用過了！")
        else:
            print(f"驗證通過：{user_input} 可以使用。")
            # 如果需要，這裡可以執行 SQL INSERT 將新資料存入資料庫
            break
except KeyboardInterrupt:
    print("\n已取消輸入，程式結束。")