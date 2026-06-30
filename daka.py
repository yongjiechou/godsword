from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# --- 設定區域 ---
# 請將路徑改為你存放 chromedriver.exe 的實際路徑
DRIVER_PATH = r'D:\Portable Python-3.9.9 x64\FAB7\DATA\chromedriver.exe'
TARGET_URL = "http://jnpmdd04.cminl.oa/WAS/Default.aspx"

# 1. 初始化瀏覽器
service = Service(executable_path=DRIVER_PATH)
options = webdriver.ChromeOptions()
# 如果是舊版 Chrome 或環境受限，可加入以下參數
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=options)

def find_and_click_in_all_frames(driver, target_id):
    # 1. 先嘗試在當前層級找
    try:
        button = driver.find_element(By.ID, target_id)
        driver.execute_script("arguments[0].click();", button)
        print(f"✅ 成功在當前層級點擊 {target_id}")
        return True
    except:
        pass

    # 2. 遞迴進入所有子 iframe 尋找
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for i in range(len(iframes)):
        try:
            driver.switch_to.frame(i)
            if find_and_click_in_all_frames(driver, target_id):
                return True
            driver.switch_to.parent_frame() # 沒找到就回上一層
        except:
            continue
    return False

# --- 主程式執行部分 ---
try:
    print(f"正在連線至: {TARGET_URL}")
    driver.get(TARGET_URL)
    time.sleep(5) # 增加等待時間確保內網網頁加載完畢

    # 開始全網頁深度搜索點擊
    if not find_and_click_in_all_frames(driver, "btnIn"):
        print("❌ 遍歷所有層級後仍找不到 btnIn")
        # 最後手段：直接執行按鈕背後的 JavaScript 函數
        # (通常 ASP.NET 按鈕會觸發 __doPostBack)
        # driver.execute_script("__doPostBack('btnIn','')")
    if not find_and_click_in_all_frames(driver, "btnConfirm"):
        print("❌ 遍歷所有層級後仍找不到 btnConfirm")

except Exception as e:
    print(f"發生錯誤: {e}")

finally:
    time.sleep(3)
    driver.quit()