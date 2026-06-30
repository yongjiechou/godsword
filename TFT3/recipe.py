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
df=pd.read_excel(file_path,dtype=str,sheet_name='Recipe release')
print(df)
r_count,c_count=df.shape

data_list = []

df = df.dropna(how='all')
# 刪除空白後，重排索引
df = df.reset_index(drop=True)

for i in df.index:

    myeqgroup=df.iloc[i,2].split(',')
    myeqgroup = [item.strip() for item in myeqgroup]
    for eqhead in myeqgroup:
        myeqhead=eqhead[:4]
        myeqlist=eqhead.split('.')
        myeqlist = [item.strip() for item in myeqlist]

        for myeq in myeqlist:
            myeq=f'{myeqhead}{myeq[-2:]}'
            new_row ={f'{df.columns[0]}': df.iloc[i,0],
f'{df.columns[1]}': df.iloc[i,1],
f'{df.columns[2]}': f'{myeq[:6]}00',
f'{df.columns[3]}': df.iloc[i,3],
f'{df.columns[4]}': df.iloc[i,4],
f'{df.columns[5]}': df.iloc[i,5],
f'{df.columns[6]}': df.iloc[i,6]}
            data_list.append(new_row)

dftemp = pd.DataFrame(data_list)
print(dftemp)
with pd.ExcelWriter('展開格式.xlsx', engine='openpyxl', mode='w') as writer:
    dftemp.to_excel(writer, sheet_name="展開格式",index=False)