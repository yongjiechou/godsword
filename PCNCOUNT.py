import os, time, re, datetime, sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

# --- 設定資料 ---
path=r'D:\#User\yongjie\H\autoit.ini'
df=pd.read_fwf(path, sep=" ",header=None)
USER_PASS=df.iloc[2,0].split("=")[-1]
USER_ID = "yongjie.chou"
TARGET_IPS = ['10.55.7.91', '10.55.7.92']

# 路徑設定
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_CHROMEDRIVER = r'D:\#User\yongjie\project-x\chromedriver.exe'

def count_pcn():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 無頭模式
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = None
    try:
        service = Service(PATH_CHROMEDRIVER)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 15)

        # 1. 登入伺服器
        current_ip = ""
        for ip in TARGET_IPS:
            try:
                print(f"嘗試連線至伺服器: {ip}...")
                driver.get(f"http://{ip}/PCN/WorklistAction.do?method=dispInitPage")
                current_ip = ip
                break
            except WebDriverException:
                print(f"⚠ {ip} 無回應，嘗試下一個...")

        if not current_ip:
            print("❌ 錯誤：所有伺服器 IP 皆無法連線。")
            return

        # 執行登入
        wait.until(EC.presence_of_element_located((By.ID, "tbUserId"))).send_keys(USER_ID)
        driver.find_element(By.ID, "tbPassword").send_keys(USER_PASS)
        driver.find_element(By.ID, "btnLogin").click()

        # 檢查登入錯誤彈窗
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"❌ 登入失敗：{alert.text}")
            alert.accept()
            return
        except TimeoutException:
            pass

        # 2. 獲取單據清單並統計數量
        print("✅ 登入成功，正在讀取單據清單...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 尋找所有符合 PCN 編號格式的連結 (以 TW 結尾)
        all_links = soup.find_all(href=re.compile("TW$"))

        pcn_count = len(all_links)

        print("\n" + "="*30)
        print(f"📊 統計結果")
        print(f"目前 WIP 中的 PCN 總數為：{pcn_count} 張")
        print("="*30)

    except Exception as e:
        print(f"❌ 執行時發生錯誤：{e}")
    finally:
        if driver:
            driver.quit()
            print("\n瀏覽器已關閉，作業結束。")

if __name__ == "__main__":
    count_pcn()
