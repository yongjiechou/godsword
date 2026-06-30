import os, time, re, datetime, clipboard, threading, sys
import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# --- 路徑設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "DATA")
PATH_CHROMEDRIVER = os.path.join(DATA_DIR, "chromedriver.exe")
PATH_EXCEL = os.path.join(DATA_DIR, "公版格式.xlsx")
PATH_WAIT_TXT = os.path.join(DATA_DIR, "waitnotdopcn.txt")
PATH_OUTPUT_TXT = os.path.join(DATA_DIR, "output.txt")

class PCNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PCN 自動化系統 v3.2")
        self.root.geometry("500x550")

        tk.Label(root, text="PCN 系統登入", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="使用者帳號:").pack()
        self.entry_user = tk.Entry(root, width=30)
        self.entry_user.insert(0, "yongjie.chou")
        self.entry_user.pack(pady=5)

        tk.Label(root, text="使用者密碼:").pack()
        self.entry_pass = tk.Entry(root, width=30, show="*")
        self.entry_pass.pack(pady=5)

        self.btn_run = tk.Button(root, text="開始執行", command=self.start_thread, bg="#4CAF50", fg="white", width=20, height=2)
        self.btn_run.pack(pady=20)

        tk.Label(root, text="執行狀態:").pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled')
        self.log_area.pack(padx=20, pady=5)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update()

    def start_thread(self):
        if not self.entry_user.get() or not self.entry_pass.get():
            messagebox.showwarning("提示", "請輸入帳號與密碼")
            return
        self.btn_run.config(state='disabled')
        threading.Thread(target=self.run_automation, daemon=True).start()

    def run_automation(self):
        user_id = self.entry_user.get().strip()
        user_pass = self.entry_pass.get()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if not os.path.exists(PATH_CHROMEDRIVER):
            self.log("❌ 錯誤: DATA 內找不到 chromedriver.exe")
            self.btn_run.config(state='normal'); return

        self.log("🚀 正在啟動 Chrome...")
        driver = webdriver.Chrome(service=Service(PATH_CHROMEDRIVER), options=chrome_options)

        try:
            mytime = datetime.datetime.now()
            ip = '10.55.7.91'
            driver.get(f"http://{ip}/PCN/WorklistAction.do?method=dispInitPage&FUNCTION_ID=F_WORKLIST")
            wait = WebDriverWait(driver, 20)

            wait.until(EC.presence_of_element_located((By.ID, "tbUserId"))).send_keys(user_id)
            driver.find_element(By.ID, "tbPassword").send_keys(user_pass)
            driver.find_element(By.ID, "btnLogin").click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                self.log(f"❌ 登入失敗: {driver.switch_to.alert.text}")
                driver.switch_to.alert.accept(); driver.quit(); self.btn_run.config(state='normal'); return
            except: pass

            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PCN')]")))
            links = BeautifulSoup(driver.page_source, 'html.parser').find_all(href=re.compile("TW$"))

            if not links:
                self.log("📭 目前無 WIP。"); driver.quit(); self.btn_run.config(state='normal'); return

            # 尋找目標 (排除 waitnotdopcn.txt)
            notyet = []
            if os.path.exists(PATH_WAIT_TXT):
                with open(PATH_WAIT_TXT, 'r', encoding='utf-8') as f:
                    notyet = [line.strip().replace('PCN-', '') for line in f.readlines() if line.strip()]

            target_pcn = next((l.text.strip() for l in reversed(links) if l.text.strip()[-10:] not in notyet), "")

            if not target_pcn:
                self.log("💡 案件皆在排除名單中。")
            else:
                self.log(f"🔍 進入詳細頁面: {target_pcn}")
                driver.get(f'http://{ip}/PCN/IssueApplyAction.do?method=dispInitPagesSign&FUNCTION_ID=F_ISSUE&PCN_ID={target_pcn}')
                wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PCN No')]")))

                # --- 資料抓取邏輯 ---
                status = driver.find_element(By.XPATH, "//strong/font").text.strip()
                pcn_no = driver.find_element(By.XPATH, "//strong[contains(text(), 'PCN No')]").text.split(':')[-1].strip()

                # 抓取 廠別 (對應截圖: *廠區(Fab))
                try:
                    fab = driver.find_element(By.XPATH, "//*[@id='mainFabSpan']").text.strip()
                except:
                    fab = "Unknown"

                # 抓取 主旨
                try:
                    subject = driver.find_element(By.XPATH, "//*[contains(text(), '主旨')]/following::pre").text.strip()
                except:
                    subject = "N/A"

                # 抓取 先行要求人員
                try:
                    owner = driver.find_element(By.XPATH, "//*[contains(text(), '先行要求人員')]/following::td").text.strip()
                except:
                    owner = ""

                # --- 寫入 Excel (A-I 欄位精確對應) ---
                if any(k in status for k in ['Signing', 'Approving', 'Applying', '簽核中']):
                    df = pd.read_excel(PATH_EXCEL, sheet_name="7.簽核文件")
                    pcn_last = str(df.iloc[-1, 5]) if len(df) > 0 else ""

                    if target_pcn != pcn_last:
                        new_row_dict = {
                            'Week': str(mytime.isocalendar()[1]),           # A: 週數數字
                            '週會日期': '',                                   # B: 空白
                            'Modeling Owner': '*' if 'Emergency' in status else '', # C
                            '簽核日期': mytime.strftime('%Y-%m-%d %H:%M'),    # D
                            '廠別': fab,                                      # E: CF7
                            'PCN(MIM) No.': target_pcn,                       # F
                            'ENG': f'PCN的WIP:{len(links)}張',                # G
                            '主旨': subject,                                  # H
                            'Comment': status                                 # I
                        }

                        # 依照 Excel 現有標題順序對齊
                        new_df = pd.DataFrame([new_row_dict]).reindex(columns=df.columns)
                        df = pd.concat([df, new_df], ignore_index=True)

                        with pd.ExcelWriter(PATH_EXCEL, engine='openpyxl', mode='w') as writer:
                            df.to_excel(writer, sheet_name="7.簽核文件", index=False)
                        self.log(f"✅ 更新成功: {target_pcn} ({fab})")
                    else:
                        self.log(f"⏭️ 案件 {target_pcn} 已存在，跳過寫入。")

                    # 複製網址
                    final_url = f"http://{ip}/PCN/IssueApplyAction.do?method=dispInitPagesSign&FUNCTION_ID=F_ISSUE&PCN_ID={pcn_no}"
                    clipboard.copy(final_url)
                    with open(PATH_OUTPUT_TXT, 'w', encoding='utf-8') as f: f.write(final_url)
                    self.log("📋 網址已複製至剪貼簿。")

        except Exception as e: self.log(f"⚠️ 錯誤: {e}")
        finally:
            driver.quit(); self.log("🏁 執行結束。"); self.btn_run.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk(); app = PCNApp(root); root.mainloop()
