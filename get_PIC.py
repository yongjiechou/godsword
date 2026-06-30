import pyautogui
import cv2
import numpy as np
import time
from PIL import Image

def auto_scroll_capture():
    # --- 設定區 ---
    # 根據你的 team+ 視窗大小調整 (寬, 高)
    capture_width = 800
    capture_height = 600
    scroll_steps = 5      # 要滾動幾次
    scroll_distance = -400 # 每次滾動量 (負數向下)
    output_name = "team_plus_long_chat.png"

    print("【準備開始】請在 5 秒內將滑鼠移至 team+ 訊息區的正中央...")
    time.sleep(5)

    # 以滑鼠目前位置為中心計算截取區域
    mx, my = pyautogui.position()
    region = (int(mx - capture_width/2), int(my - capture_height/2), capture_width, capture_height)

    screenshots = []

    print(f"開始截取區域: {region}")

    for i in range(scroll_steps):
        # 1. 截圖
        img = pyautogui.screenshot(region=region)
        # 轉為 OpenCV 格式 (BGR)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        screenshots.append(frame)

        print(f"已完成第 {i+1}/{scroll_steps} 張截圖")

        # 2. 滾動
        pyautogui.scroll(scroll_distance)
        time.sleep(1.2) # 等待讀取與動畫結束

    # 3. 影像縫合
    print("正在嘗試自動縫合圖片，請稍候...")
    stitcher = cv2.Stitcher_create(mode=cv2.Stitcher_SCANS)
    (status, result) = stitcher.stitch(screenshots)

    if status == cv2.Stitcher_OK:
        cv2.imwrite(output_name, result)
        print(f"✅ 成功！長圖已儲存為: {output_name}")
    else:
        print(f"❌ 縫合失敗 (錯誤代碼: {status})。")
        print("原因可能是：滾動距離太長導致圖片沒重疊，或是畫面有固定不動的邊欄干擾。")

if __name__ == "__main__":
    auto_scroll_capture()
