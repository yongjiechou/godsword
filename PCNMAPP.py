import os, time, re, datetime, sys, clipboard, pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# --- 設定區域 ---
DRIVER_PATH = r'D:\Portable Python-3.9.9 x64\FAB7\DATA\chromedriver.exe'

# PCN 登入資訊
PCN_USER = "yongjie.chou"
PCN_PWD = "@S122765079c"

# MAPP 登入資訊
MAPP_URL = "https://mapp.innolux.com/teamplus_innolux/EIM/Messenger/MessengerLogin.aspx?lang=zh-TW"
MAPP_USER = "yongjie.chou"
MAPP_PWD = "@S122765079c"

class PCNToMapp:
    def __init__(self):
        self.log("🚀 啟動監測系統...")
        service = Service(executable_path=DRIVER_PATH)
        options = webdriver.ChromeOptions()
        # 注意：因為要使用 pyautogui 座標點擊，不可開啟 headless 模式
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
        # 固定視窗大小以確保座標 (153, 276) 盡可能準確
        self.driver.set_window_size(1000, 800)

    def log(self, message):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_pcn_count(self):
        """登入 PCN 並獲取單號總數"""
        target_ips = ['10.55.7.91', '10.55.7.92']
        current_ip = ""

        for ip in target_ips:
            try:
                self.driver.get(f"http://{ip}/PCN/WorklistAction.do?method=dispInitPage")
                current_ip = ip
                self.log(f"✅ 連線至 {ip}")
                break
            except:
                self.log(f"⚠️ {ip} 無法連線")

        if not current_ip:
            return None

        # 登入步驟
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "tbUserId"))).send_keys(PCN_USER)
            self.driver.find_element(By.ID, "tbPassword").send_keys(PCN_PWD)
            self.driver.find_element(By.ID, "btnLogin").click()

            # 等待頁面載入並分析 HTML
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*")))
            time.sleep(2) # 確保內容加載完全
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # 抓取所有以 TW 結尾的單號連結
            all_links = soup.find_all(href=re.compile("TW$"))
            return len(all_links)
        except Exception as e:
            self.log(f"❌ PCN 抓取失敗: {e}")
            return None

    def send_mapp_notification(self, count):
        """發送 MAPP 訊息"""
        try:
            self.log(f"📣 正在開啟 MAPP...")
            self.driver.get(MAPP_URL)

            # 登入 MAPP
            try:
                account_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".listItem.account input")))
                account_field.send_keys(MAPP_USER)
                self.driver.find_element(By.CSS_SELECTOR, ".listItem.password input").send_keys(MAPP_PWD)
                self.driver.find_element(By.CLASS_NAME, "keepLogin").click()

                login_btn = self.driver.find_element(By.XPATH, "//div[contains(text(), '登入')]")
                self.driver.execute_script("arguments[0].click();", login_btn)
            except:
                self.log("ℹ️ 偵測到已登入狀態")
                pyautogui.press('enter')

            # 傳送訊息
            time.sleep(5) # 等待畫面跳轉完成

            # 使用您原本指定的座標點擊對話框
            pyautogui.click(x=153, y=276)

            message = f"【PCN 自動通知】偵測到目前 WIP 總計有：{count} 張單據。"
            clipboard.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            self.log(f"✅ 訊息已送出: {count} 張")

        except Exception as e:
            self.log(f"❌ MAPP 發送出錯: {e}")

    def run(self):
        try:
            pcn_count = self.get_pcn_count()
            if pcn_count >0:
                self.send_mapp_notification(pcn_count)
            elif pcn_count ==0:
                self.log("沒事")

            else:
                self.log("⚠️ 無法獲取單據張數，取消發送通知。")
        finally:
            time.sleep(5)
            self.driver.quit()
            self.log("🏁 作業結束")

if __name__ == "__main__":
    app = PCNToMapp()
    app.run()
