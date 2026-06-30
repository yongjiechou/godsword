import pandas as pd
import os,openpyxl

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
##pd.set_option('display.width', None) ##視情況調適欄位對應好看
pd.set_option('display.max_colwidth', None)



directory=r'D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\download'

path=max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
print(path)
wb = openpyxl.load_workbook(path)
all_sheets = wb.worksheets  # 取得所有工作表物件
names = wb.sheetnames       # 取得所有工作表名稱
##excel = pd.ExcelFile(path)
##sheets = excel.book.sheets()
filenamelist=[]
path1=r"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\data\excel_file.txt"
with open (path1,'w') as f:
    f.write('')
for i in names:
    df=pd.read_excel(path,dtype=str,sheet_name=i)
    i=i.replace('-','連接').replace('>','連接').replace('|','連接').replace(' ','')


    filename1 =fr"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\pcn\{i}.xlsx"
    df.to_excel(filename1)

for sheet in names:
##    print(sheet.name, sheet.visibility)
    print(f'{sheet}')


    with open (path1,'a') as f:

        f.write(f'{sheet}')
        f.write('\n')
    filenamelist.append(sheet)

myfilename=path.split('\\')[-1]
print(f"檔案名稱:{myfilename}")
