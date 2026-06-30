import shutil
import os


def mkdir(path):
    #判斷目錄是否存在
    #存在：True
    #不存在：False
    folder = os.path.exists(path)

    #判斷結果
    if not folder:
        #如果不存在，則建立新目錄
        os.makedirs(path)
        print('-----建立成功-----')

    else:
        #如果目錄已存在，則不建立，提示目錄已存在
        print(path+'目錄已存在')

def deltree(path):


    try:
        shutil.rmtree(path)
    except OSError as e:
        print(e)
    else:
        print("The directory is deleted successfully")

path = r"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\mTool4\mTool4\data"
path1 = r"D:\Software\WebSphere MQ 6.0_Client\Licenses\Windows\pcn"
deltree(path)
deltree(path1)
mkdir(path)
mkdir(path1)