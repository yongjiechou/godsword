import tkinter as tk
from tkinter import filedialog
import pandas as pd

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


# 1. 定義你要處理的 Sheet 索引
target_indices = [0]
all_results = [] # 用來存放每個 Sheet 處理後的結果

for idx in target_indices:
    sheet_name = sheet_names[idx]
    print(f"正在處理：{sheet_name}")

    # 讀取該分頁
    df = pd.read_excel(file_path, dtype=str, sheet_name=sheet_name)

    # 前處理：刪除全空列、補齊合併儲存格 (第二欄)
    df = df.dropna(how='all').reset_index(drop=True)
    df.iloc[:, 1] = df.iloc[:, 1].where(df.iloc[:, 1].str.len() == 4, None)
    df.iloc[:, 1] = df.iloc[:, 1].ffill()

    # 提取需要的欄位
    temp_df = pd.DataFrame({
        'TEMPLATE_ID': df.apply(lambda x: f"A{x.iloc[1]}X1" if x.iloc[6] != x.iloc[7] else f"A{x.iloc[1]}X", axis=1),
        'PRODUCT_CATE': 'PROD',
        'PRODUCT_ID': '自行替換PRODUCT_ID',
        'EC_CODE':  '自行替換EC_CODE',
        'ROUTE_ID':  '自行替換ROUTE_ID',
        'ROUTE_VER':  '00000',
        'SMP_ROUTE_ID':  df.apply(lambda x: "" if x.iloc[6] != x.iloc[7] else f"{x.iloc[1]}", axis=1),
        'SMP_ROUTE_VER':  df.apply(lambda x: "" if x.iloc[6] != x.iloc[7] else "00000", axis=1),
        'AEI_OPER_NO':  df.apply(lambda x: f"{x.iloc[6]}" if x.iloc[6] != x.iloc[7] else "", axis=1),
        'AEI_OPER_ID':  df.apply(lambda x: f"{x.iloc[6]}" if x.iloc[6] != x.iloc[7] else "", axis=1),
        'AEI_SAMP_ROUTE_ID':  df.apply(lambda x: f"{x.iloc[1]}" if x.iloc[6] != x.iloc[7] else "", axis=1),
        'AEI_SAMP_VER':  df.apply(lambda x: "00000" if x.iloc[6] != x.iloc[7] else "", axis=1),

    })


    # 將結果加入清單
    all_results.append(temp_df)

# 2. 合併所有 Sheet 的結果
result_final = pd.concat(all_results, ignore_index=True)

# 3. 匯出 Excel
with pd.ExcelWriter('展開格式.xlsx', engine='openpyxl', mode='w') as writer:
    result_final.to_excel(writer, sheet_name="展開格式", index=False)

print(f"全部處理完成！總共筆數：{len(result_final)}")



