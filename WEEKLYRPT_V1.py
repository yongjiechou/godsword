# -*- coding: utf-8 -*-
import os

# --- 1. 優先處理 DLL 載入 ---
DLL_PATH = r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\Portable Python-3.9.9 x64\App\Python\Lib\site-packages\clidriver\bin'
if os.path.exists(DLL_PATH):
    os.environ['PATH'] = DLL_PATH + os.pathsep + os.environ['PATH']
    try:
        os.add_dll_directory(DLL_PATH)
    except AttributeError:
        pass

import pandas as pd
import datetime, ibm_db, ibm_db_dbi
from datetime import timedelta

# ==========================================
# 2. 環境與路徑設定
# ==========================================
BASE_DIR = r'Z:\Software\WebSphere MQ 6.0_Client\Licenses\Windows'
FILE_NAME_TEMPLATE = '週報.xlsx'
FILE_NAME_RECORD = '2025周雍傑週報.xlsx'
NAME_OWNER = '周雍傑'

PATH_TEMPLATE = os.path.join(BASE_DIR, 'download', FILE_NAME_TEMPLATE)
PATH_RECORD = os.path.join(BASE_DIR, 'work', FILE_NAME_RECORD)

# ==========================================
# 3. 週數與日期計算
# ==========================================
target_date = datetime.datetime.now() - timedelta(days=7)
year, week_num, _ = target_date.isocalendar()
the_week = f"W{str(week_num).zfill(2)}"

start_day = datetime.datetime.strptime(f"{year}-W{week_num}-1", "%G-W%V-%u")
end_day = start_day + timedelta(days=7)
start_str = start_day.strftime('%Y/%m/%d 00:00')
end_str = end_day.strftime('%Y/%m/%d 00:00')

# ==========================================
# 4. 資料庫查詢
# ==========================================
DB_CONFIGS = {
    'T7': {
        'dsn': "DATABASE=T7WPPT1;HOSTNAME=10.107.1.1;PORT=50101;PROTOCOL=TCPIP;UID=t7wbm1u2;PWD=t7insert;",
        'table': "T7WBM1D.BAPRDCT", 'id_col': "PRODUCT_ID"
    },
    'L7': {
        'dsn': "DATABASE=L7WPPT1;HOSTNAME=10.107.1.3;PORT=50301;PROTOCOL=TCPIP;UID=l7wbm1u2;PWD=l7insert;",
        'table': "L7WBM1D.BCPRDCT", 'id_col': "PFCD"
    }
}

def fetch_db_data(db_key):
    conf = DB_CONFIGS.get(db_key)
    if not conf: return pd.DataFrame()
    sql = f"SELECT {conf['id_col']} AS PRODUCT_ID, P_CREATE_DATE FROM {conf['table']} WHERE P_CREATE_DATE >= '{start_str}' AND P_CREATE_DATE <= '{end_str}'"
    try:
        raw_conn = ibm_db.connect(conf['dsn'], "", "")
        conn = ibm_db_dbi.Connection(raw_conn)
        df = pd.read_sql(sql, conn)
        ibm_db.close(raw_conn)
        return df
    except Exception as e:
        print(f"DB Error ({db_key}): {e}")
        return pd.DataFrame()

df_new_products = pd.concat([fetch_db_data('T7'), fetch_db_data('L7')], axis=0).sort_values(by='P_CREATE_DATE').reset_index(drop=True)

# ==========================================
# 5. 資料處理與退件分析
# ==========================================
df_sign = pd.read_excel(PATH_RECORD, sheet_name="7.簽核文件").fillna("")
mydata = df_sign[df_sign['Week'] == week_num].copy()

# 總表基本資訊填寫
df_total = pd.read_excel(PATH_TEMPLATE, sheet_name=0).fillna("")
df_total.iloc[0, 0] = the_week
df_total.iloc[0, 3] = len(mydata)
df_total.iloc[0, 4] = f'新產品{len(df_new_products)}隻'

# 過濾退件案例 (週會日期不為空)
df_returned = mydata[mydata['週會日期'].astype(str).str.strip() != ''].copy()
unique_returns = (df_returned['週會日期'].astype(str) + "(" + df_returned['PCN(MIM) No.'].astype(str) + ")").unique().tolist()
df_total.iloc[1, 3] = len(df_returned)
df_total.iloc[1, 4] = ", ".join(unique_returns)

if not mydata.empty:
    last_wip = str(mydata['ENG'].iloc[-1]).split(':')[-1].replace('張','')
    df_total.iloc[2, 3] = last_wip

# 建立「PCN退件案例」資料
# 從 df_returned 映射欄位：廠區(Site), 開單人(OWNER), PCN單號(PCN(MIM) No.), 主旨(Subject), 退件原因(空), 備註(空)
df_pcn_cases = pd.DataFrame()
if not df_returned.empty:
    df_pcn_cases['廠區'] = df_returned['廠別']
    df_pcn_cases['開單人']  = df_returned['ENG'].astype(str).str.split('PCN').str[0]
    df_pcn_cases['PCN單號'] = df_returned['PCN(MIM) No.']
    df_pcn_cases['主旨'] = df_returned['主旨']
    df_pcn_cases['退件原因'] = df_returned['週會日期']
    df_pcn_cases['備註'] = ""
else:
    df_pcn_cases = pd.DataFrame(columns=['廠區', '開單人', 'PCN單號', '主旨', '退件原因', '備註'])

# ==========================================
# 6. 寫出 Excel 並設定動態框線樣式
# ==========================================
output_file = os.path.join(BASE_DIR, 'download', f'{the_week}{FILE_NAME_TEMPLATE}')

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df_total.to_excel(writer, index=False, sheet_name='總表')
    df_new_products.to_excel(writer, index=False, sheet_name='新產品')
    df_pcn_cases.to_excel(writer, index=False, sheet_name='PCN退件案例')

    workbook = writer.book
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#C6E0B4', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    cell_fmt = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
    center_fmt = workbook.add_format({'border': 1,'align': 'center','valign': 'vcenter','text_wrap': True})

    for name, df in [('總表', df_total), ('新產品', df_new_products), ('PCN退件案例', df_pcn_cases)]:
        ws = writer.sheets[name]
        rows, cols = df.shape
        # 套用標題樣式
        for col_num, value in enumerate(df.columns.values):
            ws.write(0, col_num, value, header_fmt)
        # 僅對有資料的區域繪製框線
        for r in range(rows):
            for c in range(cols):
                ws.write(r + 1, c, df.iloc[r, c], cell_fmt)
        ws.set_column(0, cols-1, 18) # 預設欄寬

    # 總表細節調整
    ws_total = writer.sheets['總表']
    ws_total.set_column('E:E', 60)
    ws_total.merge_range(1, 0, 3, 0, the_week, cell_fmt)
    ws_total.merge_range(1, 1, 3, 1, 'FAB7', cell_fmt)
    ws_total.merge_range(1, 5, 3, 5, NAME_OWNER, cell_fmt)
    ws_pcn = writer.sheets['PCN退件案例']
    ws_pcn.set_column('A:C', 20,center_fmt)  # 廠區、開單人、PCN單號
    ws_pcn.set_column('D:E', 50)  # 主旨 (D欄) 與 退件原因 (E欄) 拉長
    ws_pcn.set_column('F:F', 20)  # 備註
print(f"任務完成：{output_file}")
