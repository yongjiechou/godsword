import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime
today_str = datetime.now().strftime("%m-%d") # 格式化為 "01-05" 形式





# 2026 一年讀經計劃 - 一月份數據
january_reading_plan = {
    "01-01": {"old_testament": ["創世記 1-2"], "new_testament": ["馬太福音 1"]},
    "01-02": {"old_testament": ["創世記 3-4"], "new_testament": ["馬太福音 2"]},
    "01-03": {"old_testament": ["創世記 5-6"], "new_testament": ["馬太福音 3"]},
    "01-04": {"old_testament": ["創世記 7-8"], "new_testament": ["馬太福音 4"]},
    "01-05": {"old_testament": ["創世記 9-10"], "new_testament": ["馬太福音 5:1-16"]},
    "01-06": {"old_testament": ["創世記 11-12"], "new_testament": ["馬太福音 5:17-26"]},
    "01-07": {"old_testament": ["創世記 13-14"], "new_testament": ["馬太福音 5:27-48"]},
    "01-08": {"old_testament": ["創世記 15-16"], "new_testament": ["馬太福音 6:1-15"]},
    "01-09": {"old_testament": ["創世記 17-18"], "new_testament": ["馬太福音 6:16-34"]},
    "01-10": {"old_testament": ["創世記 19-20"], "new_testament": ["馬太福音 7"]},
    "01-11": {"old_testament": ["創世記 21-22"], "new_testament": ["馬太福音 8"]},
    "01-12": {"old_testament": ["約伯記 1-3"], "new_testament": ["馬太福音 9"]},
    "01-13": {"old_testament": ["約伯記 4-6"], "new_testament": ["馬太福音 10"]},
    "01-14": {"old_testament": ["約伯記 7-9"], "new_testament": ["馬太福音 11"]},
    "01-15": {"old_testament": ["約伯記 10-12"], "new_testament": ["馬太福音 12"]},
    "01-16": {"old_testament": ["約伯記 13-15"], "new_testament": ["馬太福音 13:1-23"]},
    "01-17": {"old_testament": ["約伯記 16-18"], "new_testament": ["馬太福音 13:24-58"]},
    "01-18": {"old_testament": ["約伯記 19-21"], "new_testament": ["馬太福音 14"]},
    "01-19": {"old_testament": ["約伯記 22-24"], "new_testament": ["馬太福音 15"]},
    "01-20": {"old_testament": ["約伯記 25-27"], "new_testament": ["馬太福音 16"]},
    "01-21": {"old_testament": ["約伯記 28-30"], "new_testament": ["馬太福音 17"]},
    "01-22": {"old_testament": ["約伯記 31-33"], "new_testament": ["馬太福音 18"]},
    "01-23": {"old_testament": ["約伯記 34-36"], "new_testament": ["馬太福音 19"]},
    "01-24": {"old_testament": ["約伯記 37-39"], "new_testament": ["馬太福音 20"]},
    "01-25": {"old_testament": ["約伯記 40-42"], "new_testament": ["馬太福音 21:1-27"]},
    "01-26": {"old_testament": ["創世記 23-24"], "new_testament": ["馬太福音 21:28-46"]},
    "01-27": {"old_testament": ["創世記 25-26"], "new_testament": ["馬太福音 22:1-22"]},
    "01-28": {"old_testament": ["創世記 27-28"], "new_testament": ["馬太福音 22:23-46"]},
    "01-29": {"old_testament": ["創世記 29-31"], "new_testament": ["馬太福音 23"]},
    "01-30": {"old_testament": ["創世記 32-34"], "new_testament": ["馬太福音 24:1-35"]},
    "01-31": {"old_testament": ["創世記 35-37"], "new_testament": ["馬太福音 24:36-51"]}
}
# 2026 一年讀經計劃 - 二月份數據
february_reading_plan = {
    "02-01": {"old_testament": ["創世記 38-40"], "new_testament": ["馬太福音 25"]},
    "02-02": {"old_testament": ["創世記 41-43"], "new_testament": ["馬太福音 26:1-35"]},
    "02-03": {"old_testament": ["創世記 44-46"], "new_testament": ["馬太福音 26:36-75"]},
    "02-04": {"old_testament": ["創世記 47-48"], "new_testament": ["馬太福音 27:1-31"]},
    "02-05": {"old_testament": ["創世記 49-50"], "new_testament": ["馬太福音 27:32-66"]},
    "02-06": {"old_testament": ["出埃及記 1-3"], "new_testament": ["馬太福音 28"]},
    "02-07": {"old_testament": ["出埃及記 4-6"], "new_testament": ["使徒行傳 1"]},
    "02-08": {"old_testament": ["出埃及記 7-9"], "new_testament": ["使徒行傳 2"]},
    "02-09": {"old_testament": ["出埃及記 10-12"], "new_testament": ["使徒行傳 3"]},
    "02-10": {"old_testament": ["出埃及記 13-15"], "new_testament": ["使徒行傳 4"]},
    "02-11": {"old_testament": ["出埃及記 16-18"], "new_testament": ["使徒行傳 5"]},
    "02-12": {"old_testament": ["出埃及記 19-20"], "new_testament": ["使徒行傳 6"]},
    "02-13": {"old_testament": ["出埃及記 21-23"], "new_testament": ["使徒行傳 7"]},
    "02-14": {"old_testament": ["出埃及記 24-26"], "new_testament": ["使徒行傳 8"]},
    "02-15": {"old_testament": ["出埃及記 27-29"], "new_testament": ["使徒行傳 9"]},
    "02-16": {"old_testament": ["出埃及記 30-32"], "new_testament": ["使徒行傳 10"]},
    "02-17": {"old_testament": ["出埃及記 33-35"], "new_testament": ["使徒行傳 11"]},
    "02-18": {"old_testament": ["出埃及記 36-38"], "new_testament": ["使徒行傳 12"]},
    "02-19": {"old_testament": ["出埃及記 39-40"], "new_testament": ["使徒行傳 13"]},
    "02-20": {"old_testament": ["詩篇 90"], "new_testament": ["使徒行傳 14"]},
    "02-21": {"old_testament": ["利未記 1-3"], "new_testament": ["使徒行傳 15:1-22"]},
    "02-22": {"old_testament": ["利未記 4-6"], "new_testament": ["雅各書 1"]},
    "02-23": {"old_testament": ["利未記 7-9"], "new_testament": ["雅各書 2"]},
    "02-24": {"old_testament": ["利未記 10-12"], "new_testament": ["雅各書 3"]},
    "02-25": {"old_testament": ["利未記 13-15"], "new_testament": ["雅各書 4"]},
    "02-26": {"old_testament": ["利未記 16-18"], "new_testament": ["雅各書 5"]},
    "02-27": {"old_testament": ["利未記 19-21"], "new_testament": ["使徒行傳 15:23-41"]},
    "02-28": {"old_testament": ["利未記 22-24"], "new_testament": ["加拉太書 1:1-10"]}
}
# 2026 一年讀經計劃 - 三月份數據
march_reading_plan = {
    "03-01": {"old_testament": ["利未記 25-27"], "new_testament": ["加拉太書 1:1-11"]},
    "03-02": {"old_testament": ["民數記 1-3"], "new_testament": ["加拉太書 2:1-10"]},
    "03-03": {"old_testament": ["民數記 4-6"], "new_testament": ["加拉太書 2:11-21"]},
    "03-04": {"old_testament": ["民數記 7-9"], "new_testament": ["加拉太書 3:1-14"]},
    "03-05": {"old_testament": ["民數記 10-12"], "new_testament": ["加拉太書 3:15-29"]},
    "03-06": {"old_testament": ["民數記 13-15"], "new_testament": ["加拉太書 4:1-20"]},
    "03-07": {"old_testament": ["民數記 16-18"], "new_testament": ["加拉太書 4:21-31"]},
    "03-08": {"old_testament": ["民數記 19-21"], "new_testament": ["加拉太書 5:1-15"]},
    "03-09": {"old_testament": ["民數記 22-24"], "new_testament": ["加拉太書 5:16-26"]},
    "03-10": {"old_testament": ["民數記 25-27"], "new_testament": ["加拉太書 6"]},
    "03-11": {"old_testament": ["民數記 28-30"], "new_testament": ["使徒行傳 16"]},
    "03-12": {"old_testament": ["民數記 31-33"], "new_testament": ["腓立比書 1:1-11"]},
    "03-13": {"old_testament": ["民數記 34-36"], "new_testament": ["腓立比書 1:12-30"]},
    "03-14": {"old_testament": ["申命記 1-3"], "new_testament": ["腓立比書 2:1-11"]},
    "03-15": {"old_testament": ["申命記 4-6"], "new_testament": ["腓立比書 2:12-30"]},
    "03-16": {"old_testament": ["申命記 7-9"], "new_testament": ["腓立比書 3"]},
    "03-17": {"old_testament": ["申命記 10-12"], "new_testament": ["腓立比書 4"]},
    "03-18": {"old_testament": ["申命記 13-15"], "new_testament": ["使徒行傳 17:1-10", "帖撒羅尼迦前書 1"]},
    "03-19": {"old_testament": ["申命記 16-18"], "new_testament": ["帖撒羅尼迦前書 2"]},
    "03-20": {"old_testament": ["申命記 19-21"], "new_testament": ["帖撒羅尼迦前書 3"]},
    "03-21": {"old_testament": ["申命記 22-24"], "new_testament": ["帖撒羅尼迦前書 4"]},
    "03-22": {"old_testament": ["申命記 25-27"], "new_testament": ["帖撒羅尼迦前書 5"]},
    "03-23": {"old_testament": ["申命記 28-30"], "new_testament": ["帖撒羅尼迦後書 1"]},
    "03-24": {"old_testament": ["申命記 31-33"], "new_testament": ["帖撒羅尼迦後書 2"]},
    "03-25": {"old_testament": ["申命記 34", "詩篇 91"], "new_testament": ["帖撒羅尼迦後書 3"]},
    "03-26": {"old_testament": ["約書亞記 1-3"], "new_testament": ["使徒行傳 17:11-18:11"]},
    "03-27": {"old_testament": ["約書亞記 4-6"], "new_testament": ["哥林多前書 1"]},
    "03-28": {"old_testament": ["約書亞記 7-8"], "new_testament": ["哥林多前書 2"]},
    "03-29": {"old_testament": ["約書亞記 9-10"], "new_testament": ["哥林多前書 3"]},
    "03-30": {"old_testament": ["約書亞記 11-13"], "new_testament": ["哥林多前書 4"]},
    "03-31": {"old_testament": ["約書亞記 14-16"], "new_testament": ["哥林多前書 5"]}
}
# 2026 一年讀經計劃 - 四月份數據
april_reading_plan = {
    "04-01": {"old_testament": ["約書亞記 17-19"], "new_testament": ["哥林多前書 6"]},
    "04-02": {"old_testament": ["約書亞記 20-21"], "new_testament": ["哥林多前書 7"]},
    "04-03": {"old_testament": ["約書亞記 22-24"], "new_testament": ["哥林多前書 8"]},
    "04-04": {"old_testament": ["士師記 1-3"], "new_testament": ["哥林多前書 9"]},
    "04-05": {"old_testament": ["士師記 4-6"], "new_testament": ["哥林多前書 10"]},
    "04-06": {"old_testament": ["士師記 7-9"], "new_testament": ["哥林多前書 11"]},
    "04-07": {"old_testament": ["士師記 10-12"], "new_testament": ["哥林多前書 12"]},
    "04-08": {"old_testament": ["士師記 13-15"], "new_testament": ["哥林多前書 13"]},
    "04-09": {"old_testament": ["士師記 16-18"], "new_testament": ["哥林多前書 14"]},
    "04-10": {"old_testament": ["士師記 19-21"], "new_testament": ["哥林高前書 15"]},
    "04-11": {"old_testament": ["路得記 1-4"], "new_testament": ["哥林多前書 16"]},
    "04-12": {"old_testament": ["撒母耳記上 1-3"], "new_testament": ["馬可福音 1:1-28"]},
    "04-13": {"old_testament": ["撒母耳記上 4-6"], "new_testament": ["馬可福音 1:29-45"]},
    "04-14": {"old_testament": ["撒母耳記上 7-9"], "new_testament": ["馬可福音 2"]},
    "04-15": {"old_testament": ["撒母耳記上 10-12"], "new_testament": ["馬可福音 3"]},
    "04-16": {"old_testament": ["撒母耳記上 13-14"], "new_testament": ["馬可福音 4"]},
    "04-17": {"old_testament": ["撒母耳記上 15-16"], "new_testament": ["詩篇 23", "馬可福音 5"]},
    "04-18": {"old_testament": ["撒母耳記上 17-19"], "new_testament": ["詩篇 59", "馬可福音 6:1-29"]},
    "04-19": {"old_testament": ["撒母耳記上 20-21"], "new_testament": ["詩篇 34", "詩篇 56", "馬可福音 6:30-56"]},
    "04-20": {"old_testament": ["撒母耳記上 22:1-2"], "new_testament": ["詩篇 57", "詩篇 142"]},
    "04-21": {"old_testament": ["撒母耳記上 22:3-23"], "new_testament": ["詩篇 52", "馬可福音 7", "馬可福音 8"]},
    "04-22": {"old_testament": ["撒母耳記上 23"], "new_testament": ["詩篇 54", "詩篇 63", "馬可福音 9:1-32"]},
    "04-23": {"old_testament": ["撒母耳記上 24-27"], "new_testament": ["馬可福音 9:33-50"]},
    "04-24": {"old_testament": ["撒母耳記上 28-31"], "new_testament": ["馬可福音 10:1-31"]},
    "04-25": {"old_testament": ["撒母耳記下 1-2"], "new_testament": ["馬可福音 10:32-52"]},
    "04-26": {"old_testament": ["撒母耳記下 3-4"], "new_testament": ["馬可福音 11"]},
    "04-27": {"old_testament": ["撒母耳記下 5-7"], "new_testament": ["詩篇 30", "馬可福音 12:1-27"]},
    "04-28": {"old_testament": ["撒母耳記下 8:1-14"], "new_testament": ["詩篇 60", "馬可福音 12:28-44"]},
    "04-29": {"old_testament": ["撒母耳記下 8:15-10"], "new_testament": ["馬可福音 13"]},
    "04-30": {"old_testament": ["撒母耳記下 11-12:14"], "new_testament": ["詩篇 51", "詩篇 32", "馬可福音 14:1-26"]}
}
# 2026 一年讀經計劃 - 五月份數據
may_reading_plan = {
    "05-01": {"old_testament": ["撒母耳記下 12:15-13"], "new_testament": ["馬可福音 14:27-72"]},
    "05-02": {"old_testament": ["詩篇 3", "詩篇 69"], "new_testament": ["馬可福音 15:1-32"]},
    "05-03": {"old_testament": ["撒母耳記下 16-18"], "new_testament": ["詩篇 64", "馬可福音 15:33-47"]},
    "05-04": {"old_testament": ["撒母耳記下 19-20"], "new_testament": ["詩篇 70", "馬可福音 16"]},
    "05-05": {"old_testament": ["撒母耳記下 21-22"], "new_testament": ["詩篇 18"]},
    "05-06": {"old_testament": ["撒母耳記下 23-24"], "new_testament": ["哥林多後書 1"]},
    "05-07": {"old_testament": ["詩篇 4-6"], "new_testament": ["哥林多後書 2"]},
    "05-08": {"old_testament": ["詩篇 7-9"], "new_testament": ["哥林多後書 3"]},
    "05-09": {"old_testament": ["詩篇 11-13"], "new_testament": ["哥林多後書 4"]},
    "05-10": {"old_testament": ["詩篇 14-16"], "new_testament": ["哥林多後書 5"]},
    "05-11": {"old_testament": ["詩篇 17", "詩篇 19"], "new_testament": ["哥林多後書 6"]},
    "05-12": {"old_testament": ["詩篇 20-22"], "new_testament": ["哥林多後書 7"]},
    "05-13": {"old_testament": ["詩篇 24-26"], "new_testament": ["哥林多後書 8"]},
    "05-14": {"old_testament": ["詩篇 27-28"], "new_testament": ["哥林多後書 9"]},
    "05-15": {"old_testament": ["詩篇 29", "詩篇 31"], "new_testament": ["哥林多後書 10"]},
    "05-16": {"old_testament": ["詩篇 35-36"], "new_testament": ["哥林多後書 11"]},
    "05-17": {"old_testament": ["詩篇 37-38"], "new_testament": ["哥林多後書 12"]},
    "05-18": {"old_testament": ["詩篇 39-40"], "new_testament": ["哥林多後書 13"]},
    "05-19": {"old_testament": ["詩篇 41", "詩篇 53"], "new_testament": ["使徒行傳 18:12-20:1"]},
    "05-20": {"old_testament": ["詩篇 55", "詩篇 58"], "new_testament": ["以弗所書 1:1-14"]},
    "05-21": {"old_testament": ["詩篇 61-62"], "new_testament": ["以弗所書 1:15-23"]},
    "05-22": {"old_testament": ["詩篇 65", "詩篇 68"], "new_testament": ["以弗所書 2:1-10"]},
    "05-23": {"old_testament": ["詩篇 72", "詩篇 86"], "new_testament": ["以弗所書 2:11-22"]},
    "05-24": {"old_testament": ["詩篇 101", "詩篇 103"], "new_testament": ["以弗所書 3:1-13"]},
    "05-25": {"old_testament": ["詩篇 108-110"], "new_testament": ["以弗所書 3:14-21"]},
    "05-26": {"old_testament": ["詩篇 138-141"], "new_testament": ["以弗所書 4:1-16"]},
    "05-27": {"old_testament": ["詩篇 143-145"], "new_testament": ["以弗所書 4:17-32"]},
    "05-28": {"old_testament": ["列王記上 1-2"], "new_testament": ["以弗所書 5:1-20"]},
    "05-29": {"old_testament": ["列王記上 3-4"], "new_testament": ["箴言 1", "以弗所書 5:21-33"]},
    "05-30": {"old_testament": ["雅歌 1-2"], "new_testament": ["箴言 2", "以弗所書 6:1-9"]},
    "05-31": {"old_testament": ["雅歌 3-4"], "new_testament": ["箴言 3", "以弗所書 6:10-24"]}
}
# 2026 一年讀經計劃 - 六月份數據
june_reading_plan = {
    "06-01": {"old_testament": ["雅歌 5-6", "箴言 4"], "new_testament": ["路加福音 1:1-38"]},
    "06-02": {"old_testament": ["雅歌 7-8", "箴言 5"], "new_testament": ["路加福音 1:39-80"]},
    "06-03": {"old_testament": ["列王記上 5-6", "箴言 6"], "new_testament": ["路加福音 2:1-40"]},
    "06-04": {"old_testament": ["列王記上 7-8", "箴言 7"], "new_testament": ["路加福音 2:41-52"]},
    "06-05": {"old_testament": ["列王記上 9-10", "箴言 8"], "new_testament": ["路加福音 3"]},
    "06-06": {"old_testament": ["列王記上 11", "箴言 9"], "new_testament": ["路加福音 4:1-30"]},
    "06-07": {"old_testament": ["傳道書 1-2", "箴言 10"], "new_testament": ["路加福音 4:31-44"]},
    "06-08": {"old_testament": ["傳道書 3-4", "箴言 11"], "new_testament": ["路加福音 5"]},
    "06-09": {"old_testament": ["傳道書 5-6", "箴言 12"], "new_testament": ["路加福音 6:1-36"]},
    "06-10": {"old_testament": ["傳道書 7-8", "箴言 13"], "new_testament": ["路加福音 6:37-49"]},
    "06-11": {"old_testament": ["傳道書 9-10", "箴言 14"], "new_testament": ["路加福音 7"]},
    "06-12": {"old_testament": ["傳道書 11-12", "箴言 15"], "new_testament": ["路加福音 8:1-25"]},
    "06-13": {"old_testament": ["箴言 16"], "new_testament": ["路加福音 8:26-56"]},
    "06-14": {"old_testament": ["列王記上 12-13", "箴言 17"], "new_testament": ["路加福音 9:1-36"]},
    "06-15": {"old_testament": ["列王記上 14-15", "箴言 18"], "new_testament": ["路加福音 9:37-62"]},
    "06-16": {"old_testament": ["列王記上 16-17", "箴言 19"], "new_testament": ["路加福音 10"]},
    "06-17": {"old_testament": ["列王記上 18-19", "箴言 20"], "new_testament": ["路加福音 11"]},
    "06-18": {"old_testament": ["列王記上 20", "箴言 21"], "new_testament": ["路加福音 12"]},
    "06-19": {"old_testament": ["列王記上 21", "箴言 22"], "new_testament": ["路加福音 13"]},
    "06-20": {"old_testament": ["列王記上 22", "箴言 23"], "new_testament": ["路加福音 14"]},
    "06-21": {"old_testament": ["列王記下 1-2", "箴言 24"], "new_testament": ["路加福音 15"]},
    "06-22": {"old_testament": ["列王記下 3", "箴言 25"], "new_testament": ["路加福音 16"]},
    "06-23": {"old_testament": ["列王記下 4", "箴言 26"], "new_testament": ["路加福音 17"]},
    "06-24": {"old_testament": ["列王記下 5", "箴言 27"], "new_testament": ["路加福音 18"]},
    "06-25": {"old_testament": ["列王記下 6", "箴言 28"], "new_testament": ["路加福音 19"]},
    "06-26": {"old_testament": ["列王記下 7", "箴言 29"], "new_testament": ["路加福音 20"]},
    "06-27": {"old_testament": ["列王記下 8", "箴言 30"], "new_testament": ["路加福音 21"]},
    "06-28": {"old_testament": ["列王記下 9", "箴言 31"], "new_testament": ["路加福音 22:1-38"]},
    "06-29": {"old_testament": ["列王記下 10-11"], "new_testament": ["路加福音 22:39-71"]},
    "06-30": {"old_testament": ["列王記下 12-13"], "new_testament": ["路加福音 23:1-25"]}
}
# 2026 一年讀經計劃 - 七月份數據
july_reading_plan = {
    "07-01": {"old_testament": ["列王記下 14:1-22"], "new_testament": ["約拿書 1-2", "路加福音 23:26-56"]},
    "07-02": {"old_testament": ["約拿書 3-4"], "new_testament": ["路加福音 24:1-35"]},
    "07-03": {"old_testament": ["列王記下 14:23-29"], "new_testament": ["阿摩司書 1-2", "路加福音 24:36-53"]},
    "07-04": {"old_testament": ["阿摩司書 3-4"], "new_testament": ["羅馬書 1:1-17"]},
    "07-05": {"old_testament": ["阿摩司書 5-6"], "new_testament": ["羅馬書 1:18-32"]},
    "07-06": {"old_testament": ["阿摩司書 7-9"], "new_testament": ["羅馬書 2:1-16"]},
    "07-07": {"old_testament": ["列王記下 15-16"], "new_testament": ["羅馬書 2:17-29"]},
    "07-08": {"old_testament": ["列王記下 17-18"], "new_testament": ["羅馬書 3:1-20"]},
    "07-09": {"old_testament": ["列王記下 19-20"], "new_testament": ["羅馬書 3:21-31"]},
    "07-10": {"old_testament": ["列王記下 21-23"], "new_testament": ["羅馬書 4"]},
    "07-11": {"old_testament": ["列王記下 24-25"], "new_testament": ["羅馬書 5:1-11"]},
    "07-12": {"old_testament": ["詩篇 1-2"], "new_testament": ["羅馬書 5:12-21"]},
    "07-13": {"old_testament": ["詩篇 10", "詩篇 33"], "new_testament": ["羅馬書 6:1-14"]},
    "07-14": {"old_testament": ["詩篇 43", "詩篇 66"], "new_testament": ["羅馬書 6:15-23"]},
    "07-15": {"old_testament": ["詩篇 67", "詩篇 71"], "new_testament": ["羅馬書 7:1-6"]},
    "07-16": {"old_testament": ["詩篇 89", "詩篇 92"], "new_testament": ["羅馬書 7:7-25"]},
    "07-17": {"old_testament": ["詩篇 93-95"], "new_testament": ["羅馬書 8:1-17"]},
    "07-18": {"old_testament": ["詩篇 96-97"], "new_testament": ["羅馬書 8:18-27"]},
    "07-19": {"old_testament": ["詩篇 98-99"], "new_testament": ["羅馬書 8:28-39"]},
    "07-20": {"old_testament": ["詩篇 100", "詩篇 102"], "new_testament": ["羅馬書 9:1-29"]},
    "07-21": {"old_testament": ["詩篇 104-105"], "new_testament": ["羅馬書 9:30-10:21"]},
    "07-22": {"old_testament": ["詩篇 106", "詩篇 111"], "new_testament": ["羅馬書 11:1-10"]},
    "07-23": {"old_testament": ["詩篇 112-113"], "new_testament": ["羅馬書 11:11-24"]},
    "07-24": {"old_testament": ["詩篇 114-115"], "new_testament": ["羅馬書 11:25-36"]},
    "07-25": {"old_testament": ["詩篇 116-118"], "new_testament": ["羅馬書 12:1-8"]},
    "07-26": {"old_testament": ["詩篇 119:1-32"], "new_testament": ["羅馬書 12:9-21"]},
    "07-27": {"old_testament": ["詩篇 119:33-64"], "new_testament": ["羅馬書 13"]},
    "07-28": {"old_testament": ["詩篇 119:65-88"], "new_testament": ["羅馬書 14"]},
    "07-29": {"old_testament": ["詩篇 119:89-120"], "new_testament": ["羅馬書 15:1-22"]},
    "07-30": {"old_testament": ["詩篇 119:121-152"], "new_testament": ["羅馬書 15:23-16:27"]},
    "07-31": {"old_testament": ["詩篇 119:153-176"], "new_testament": ["使徒行傳 20:2-21:16"]}
}
# 2026 一年讀經計劃 - 八月份數據
august_reading_plan = {
    "08-01": {"old_testament": ["詩篇 120-121"], "new_testament": ["使徒行傳 21:17-23:35"]},
    "08-02": {"old_testament": ["詩篇 122-123"], "new_testament": ["使徒行傳 24"]},
    "08-03": {"old_testament": ["詩篇 124-125"], "new_testament": ["使徒行傳 25"]},
    "08-04": {"old_testament": ["詩篇 127-128"], "new_testament": ["使徒行傳 26"]},
    "08-05": {"old_testament": ["詩篇 129-130"], "new_testament": ["使徒行傳 27"]},
    "08-06": {"old_testament": ["詩篇 131-132"], "new_testament": ["使徒行傳 28"]},
    "08-07": {"old_testament": ["詩篇 133-134"], "new_testament": ["歌羅西書 1:1-14"]},
    "08-08": {"old_testament": ["詩篇 135-136"], "new_testament": ["歌羅西書 1:15-2:5"]},
    "08-09": {"old_testament": ["詩篇 146-147"], "new_testament": ["歌羅西書 2:6-23"]},
    "08-10": {"old_testament": ["詩篇 148-149"], "new_testament": ["歌羅西書 3:1-17"]},
    "08-11": {"old_testament": ["歷代志上 1-2"], "new_testament": ["歌羅西書 3:18-4:1"]},
    "08-12": {"old_testament": ["歷代志上 3-4"], "new_testament": ["歌羅西書 4:2-18"]},
    "08-13": {"old_testament": ["歷代志上 5-6"], "new_testament": ["詩篇 150", "希伯來書 1"]},
    "08-14": {"old_testament": ["歷代志上 7-8"], "new_testament": ["希伯來書 2"]},
    "08-15": {"old_testament": ["歷代志上 9-10"], "new_testament": ["希伯來書 3"]},
    "08-16": {"old_testament": ["歷代志上 11-12"], "new_testament": ["希伯來書 4:1-13"]},
    "08-17": {"old_testament": ["歷代志上 13-14"], "new_testament": ["希伯來書 4:14-5:10"]},
    "08-18": {"old_testament": ["歷代志上 15-16"], "new_testament": ["希伯來書 5:11-6:12"]},
    "08-19": {"old_testament": ["詩篇 42", "詩篇 44"], "new_testament": ["希伯來書 6:13-7:10"]},
    "08-20": {"old_testament": ["詩篇 45-46"], "new_testament": ["希伯來書 7:11-28"]},
    "08-21": {"old_testament": ["詩篇 47-48"], "new_testament": ["希伯來書 8"]},
    "08-22": {"old_testament": ["詩篇 49-50"], "new_testament": ["希伯來書 9:1-10"]},
    "08-23": {"old_testament": ["詩篇 73-74"], "new_testament": ["希伯來書 9:11-28"]},
    "08-24": {"old_testament": ["詩篇 75-76"], "new_testament": ["希伯來書 10:1-18"]},
    "08-25": {"old_testament": ["詩篇 77-78"], "new_testament": ["希伯來書 10:19-39"]},
    "08-26": {"old_testament": ["詩篇 79-80"], "new_testament": ["希伯來書 11:1-16"]},
    "08-27": {"old_testament": ["詩篇 81-82"], "new_testament": ["希伯來書 11:17-40"]},
    "08-28": {"old_testament": ["詩篇 83-84"], "new_testament": ["希伯來書 12:1-13"]},
    "08-29": {"old_testament": ["詩篇 85", "詩篇 87"], "new_testament": ["希伯來書 12:14-29"]},
    "08-30": {"old_testament": ["詩篇 88", "歷代志上 17"], "new_testament": ["希伯來書 13"]},
    "08-31": {"old_testament": ["歷代志上 18-19"], "new_testament": ["約翰福音 1:1-18"]}
}
# 2026 一年讀經計劃 - 九月份數據
september_reading_plan = {
    "09-01": {"old_testament": ["歷代志上 20-21"], "new_testament": ["約翰福音 1:19-28"]},
    "09-02": {"old_testament": ["歷代志上 22-23"], "new_testament": ["約翰福音 1:29-34"]},
    "09-03": {"old_testament": ["歷代志上 24-25"], "new_testament": ["約翰福音 1:35-42"]},
    "09-04": {"old_testament": ["歷代志上 26-27"], "new_testament": ["約翰福音 1:43-51"]},
    "09-05": {"old_testament": ["歷代志上 28-29"], "new_testament": ["約翰福音 2:1-11"]},
    "09-06": {"old_testament": ["歷代志下 1-2"], "new_testament": ["約翰福音 2:12-25"]},
    "09-07": {"old_testament": ["歷代志下 3-4"], "new_testament": ["約翰福音 3:1-21"]},
    "09-08": {"old_testament": ["歷代志下 5-6"], "new_testament": ["約翰福音 3:22-36"]},
    "09-09": {"old_testament": ["歷代志下 7-8"], "new_testament": ["約翰福音 4:1-38"]},
    "09-10": {"old_testament": ["歷代志下 9-10"], "new_testament": ["約翰福音 4:39-42"]},
    "09-11": {"old_testament": ["歷代志下 11-12"], "new_testament": ["約翰福音 4:43-54"]},
    "09-12": {"old_testament": ["歷代志下 13-14"], "new_testament": ["約翰福音 5:1-15"]},
    "09-13": {"old_testament": ["歷代志下 15-16"], "new_testament": ["約翰福音 5:16-30"]},
    "09-14": {"old_testament": ["歷代志下 17-18"], "new_testament": ["約翰福音 5:31-47"]},
    "09-15": {"old_testament": ["歷代志下 19-21"], "new_testament": ["約翰福音 6:1-15"]},
    "09-16": {"old_testament": ["俄巴底亞書"], "new_testament": ["約翰福音 6:16-24"]},
    "09-17": {"old_testament": ["歷代志下 22", "約珥書 1"], "new_testament": ["約翰福音 6:25-59"]},
    "09-18": {"old_testament": ["約珥書 2-3"], "new_testament": ["約翰福音 6:60-71"]},
    "09-19": {"old_testament": ["歷代志下 23-24"], "new_testament": ["約翰福音 7:1-13"]},
    "09-20": {"old_testament": ["歷代志下 25-26:8"], "new_testament": ["以賽亞書 1-2", "約翰福音 7:14-24"]},
    "09-21": {"old_testament": ["以賽亞書 3-5"], "new_testament": ["約翰福音 7:25-44"]},
    "09-22": {"old_testament": ["歷代志下 26:9-23"], "new_testament": ["以賽亞書 6", "約翰福音 7:45-52"]},
    "09-23": {"old_testament": ["歷代志下 27-29"], "new_testament": ["約翰福音 8:1-11"]},
    "09-24": {"old_testament": ["歷代志下 30-32"], "new_testament": ["約翰福音 8:12-30"]},
    "09-25": {"old_testament": ["以賽亞書 7-9"], "new_testament": ["約翰福音 8:31-41"]},
    "09-26": {"old_testament": ["以賽亞書 10-12"], "new_testament": ["約翰福音 8:42-47"]},
    "09-27": {"old_testament": ["以賽亞書 13-15"], "new_testament": ["約翰福音 8:48-59"]},
    "09-28": {"old_testament": ["以賽亞書 16-18"], "new_testament": ["約翰福音 9:1-12"]},
    "09-29": {"old_testament": ["以賽亞書 19-21"], "new_testament": ["約翰福音 9:13-34"]},
    "09-30": {"old_testament": ["以賽亞書 22-24"], "new_testament": ["約翰福音 9:35-41"]}
}
# 2026 一年讀經計劃 - 十月份數據
october_reading_plan = {
    "10-01": {"old_testament": ["以賽亞書 25-27"], "new_testament": ["約翰福音 10:1-21"]},
    "10-02": {"old_testament": ["以賽亞書 28-30"], "new_testament": ["約翰福音 10:22-42"]},
    "10-03": {"old_testament": ["以賽亞書 31-33"], "new_testament": ["約翰福音 11:1-16"]},
    "10-04": {"old_testament": ["以賽亞書 34-37"], "new_testament": ["約翰福音 11:17-37"]},
    "10-05": {"old_testament": ["以賽亞書 38-41"], "new_testament": ["約翰福音 11:38-44"]},
    "10-06": {"old_testament": ["以賽亞書 42-44"], "new_testament": ["約翰福音 11:45-57"]},
    "10-07": {"old_testament": ["以賽亞書 45-47"], "new_testament": ["約翰福音 12:1-11"]},
    "10-08": {"old_testament": ["以賽亞書 48-50"], "new_testament": ["約翰福音 12:12-19"]},
    "10-09": {"old_testament": ["以賽亞書 51-54"], "new_testament": ["約翰福音 12:20-36"]},
    "10-10": {"old_testament": ["以賽亞書 55-58"], "new_testament": ["約翰福音 12:37-50"]},
    "10-11": {"old_testament": ["以賽亞書 59-62"], "new_testament": ["約翰福音 13:1-17"]},
    "10-12": {"old_testament": ["以賽亞書 63-66"], "new_testament": ["約翰福音 13:18-30"]},
    "10-13": {"old_testament": ["何西阿書 1-3"], "new_testament": ["約翰福音 13:31-38"]},
    "10-14": {"old_testament": ["何西阿書 4-6"], "new_testament": ["約翰福音 14:1-14"]},
    "10-15": {"old_testament": ["何西阿書 7-9"], "new_testament": ["約翰福音 14:15-31"]},
    "10-16": {"old_testament": ["何西阿書 10-12"], "new_testament": ["約翰福音 15:1-17"]},
    "10-17": {"old_testament": ["何西阿書 13-14"], "new_testament": ["約翰福音 15:18-16:4"]},
    "10-18": {"old_testament": ["彌迦書 1-3"], "new_testament": ["約翰福音 16:5-16"]},
    "10-19": {"old_testament": ["彌迦書 4-5"], "new_testament": ["約翰福音 16:17-33"]},
    "10-20": {"old_testament": ["彌迦書 6-7"], "new_testament": ["約翰福音 17:1-5"]},
    "10-21": {"old_testament": ["那鴻書 1-3"], "new_testament": ["約翰福音 17:6-19"]},
    "10-22": {"old_testament": ["歷代志下 33-34"], "new_testament": ["約翰福音 17:20-26"]},
    "10-23": {"old_testament": ["西番雅書 1-3"], "new_testament": ["約翰福音 18:1-11"]},
    "10-24": {"old_testament": ["歷代志下 35"], "new_testament": ["約翰福音 18:12-24"]},
    "10-25": {"old_testament": ["哈巴谷書 1-3"], "new_testament": ["約翰福音 18:25-40"]},
    "10-26": {"old_testament": ["耶利米書 1-3"], "new_testament": ["約翰福音 19:1-16"]},
    "10-27": {"old_testament": ["耶利米書 4-6"], "new_testament": ["約翰福音 19:17-27"]},
    "10-28": {"old_testament": ["耶利米書 11-12"], "new_testament": ["約翰福音 19:28-42"]},
    "10-29": {"old_testament": ["耶利米書 7-8"], "new_testament": ["約翰福音 20:1-9"]},
    "10-30": {"old_testament": ["耶利米書 9-10"], "new_testament": ["約翰福音 20:10-18"]},
    "10-31": {"old_testament": ["耶利米書 14-15"], "new_testament": ["約翰福音 20:19-31"]}
}
# 2026 一年讀經計劃 - 十一月份數據
november_reading_plan = {
    "11-01": {"old_testament": ["耶利米書 16-17"], "new_testament": ["約翰福音 21:1-14"]},
    "11-02": {"old_testament": ["耶利米書 18-20"], "new_testament": ["約翰福音 21:15-25"]},
    "11-03": {"old_testament": ["耶利米書 35-36"], "new_testament": ["提多書 1"]},
    "11-04": {"old_testament": ["耶利米書 45", "耶利米書 25"], "new_testament": ["提多書 2:1-8"]},
    "11-05": {"old_testament": ["耶利米書 46-47"], "new_testament": ["提多書 2:9-15"]},
    "11-06": {"old_testament": ["耶利米書 48-49"], "new_testament": ["提多書 3"]},
    "11-07": {"old_testament": ["耶利米書 13", "耶利米書 22"], "new_testament": ["腓利門書"]},
    "11-08": {"old_testament": ["耶利米書 23-24"], "new_testament": ["提摩太前書 1:1-11"]},
    "11-09": {"old_testament": ["耶利米書 26-29"], "new_testament": ["提摩太前書 1:12-20"]},
    "11-10": {"old_testament": ["耶利米書 50-51"], "new_testament": ["提摩太前書 2"]},
    "11-11": {"old_testament": ["耶利米書 30-31"], "new_testament": ["提摩太前書 3:1-7"]},
    "11-12": {"old_testament": ["耶利米書 32-33"], "new_testament": ["提摩太前書 3:8-16"]},
    "11-13": {"old_testament": ["耶利米書 21", "耶利米書 34"], "new_testament": ["提摩太前書 4"]},
    "11-14": {"old_testament": ["耶利米書 37-38"], "new_testament": ["提摩太前書 5:1-16"]},
    "11-15": {"old_testament": ["耶利米書 39", "耶利米書 52"], "new_testament": ["提摩太前書 5:17-25"]},
    "11-16": {"old_testament": ["耶利米書 40-41"], "new_testament": ["提摩太前書 6:1-10"]},
    "11-17": {"old_testament": ["耶利米書 42-44"], "new_testament": ["提摩太前書 6:11-21"]},
    "11-18": {"old_testament": ["耶利米哀歌 1-2"], "new_testament": ["提摩太後書 1"]},
    "11-19": {"old_testament": ["耶利米哀歌 3-5"], "new_testament": ["提摩太後書 2:1-13"]},
    "11-20": {"old_testament": ["歷代志下 36:1-8"], "new_testament": ["但以理書 1-3", "提摩太後書 2:14-26"]},
    "11-21": {"old_testament": ["但以理書 4-6"], "new_testament": ["提摩太後書 3:1-9"]},
    "11-22": {"old_testament": ["但以理書 7-9"], "new_testament": ["提摩太後書 3:10-4:8"]},
    "11-23": {"old_testament": ["但以理書 10-12"], "new_testament": ["提摩太後書 4:9-22"]},
    "11-24": {"old_testament": ["歷代志下 36:9-21"], "new_testament": ["詩篇 137", "彼得前書 1"]},
    "11-25": {"old_testament": ["以西結書 1-3"], "new_testament": ["彼得前書 2"]},
    "11-26": {"old_testament": ["以西結書 4-6"], "new_testament": ["彼得前書 3"]},
    "11-27": {"old_testament": ["以西結書 7-9"], "new_testament": ["彼得前書 4"]},
    "11-28": {"old_testament": ["以西結書 10-12"], "new_testament": ["彼得前書 5"]},
    "11-29": {"old_testament": ["以西結書 13-15"], "new_testament": ["彼得後書 1"]},
    "11-30": {"old_testament": ["以西結書 16-18"], "new_testament": ["彼得後書 2"]}
}
# 2026 一年讀經計劃 - 十二月份數據
december_reading_plan = {
    "12-01": {"old_testament": ["以西結書 19-21"], "new_testament": ["彼得後書 3"]},
    "12-02": {"old_testament": ["以西結書 22-24"], "new_testament": ["約翰壹書 1"]},
    "12-03": {"old_testament": ["以西結書 25-27"], "new_testament": ["約翰壹書 2"]},
    "12-04": {"old_testament": ["以西結書 28-30"], "new_testament": ["約翰壹書 3"]},
    "12-05": {"old_testament": ["以西結書 31-33"], "new_testament": ["約翰壹書 4"]},
    "12-06": {"old_testament": ["以西結書 34-36"], "new_testament": ["約翰壹書 5"]},
    "12-07": {"old_testament": ["以西結書 37-39"], "new_testament": ["約翰貳書"]},
    "12-08": {"old_testament": ["以西結書 40-42"], "new_testament": ["約翰參書"]},
    "12-09": {"old_testament": ["以西結書 43-45"], "new_testament": ["猶大書"]},
    "12-10": {"old_testament": ["以西結書 46-48"], "new_testament": ["啟示錄 1"]},
    "12-11": {"old_testament": ["歷代志下 36:22-23", "以斯拉記 1-2"], "new_testament": ["啟示錄 2"]},
    "12-12": {"old_testament": ["以斯拉記 3-5:1"], "new_testament": ["啟示錄 3"]},
    "12-13": {"old_testament": ["哈該書 1-2"], "new_testament": ["啟示錄 4"]},
    "12-14": {"old_testament": ["撒迦利亞書 1-3"], "new_testament": ["啟示錄 5"]},
    "12-15": {"old_testament": ["撒迦利亞書 4-6"], "new_testament": ["啟示錄 6"]},
    "12-16": {"old_testament": ["撒迦利亞書 7-9"], "new_testament": ["啟示錄 7"]},
    "12-17": {"old_testament": ["撒迦利亞書 10-12"], "new_testament": ["啟示錄 8"]},
    "12-18": {"old_testament": ["撒迦利亞書 13-14"], "new_testament": ["啟示錄 9"]},
    "12-19": {"old_testament": ["詩篇 107", "詩篇 126"], "new_testament": ["啟示錄 10"]},
    "12-20": {"old_testament": ["以斯拉記 5:2-6"], "new_testament": ["啟示錄 11"]},
    "12-21": {"old_testament": ["以斯帖記 1-3"], "new_testament": ["啟示錄 12"]},
    "12-22": {"old_testament": ["以斯帖記 4-7"], "new_testament": ["啟示錄 13"]},
    "12-23": {"old_testament": ["以斯帖記 8-10"], "new_testament": ["啟示錄 14"]},
    "12-24": {"old_testament": ["以斯拉記 7-10"], "new_testament": ["啟示錄 15"]},
    "12-25": {"old_testament": ["尼希米記 1-3"], "new_testament": ["啟示錄 16"]},
    "12-26": {"old_testament": ["尼希米記 4-5"], "new_testament": ["啟示錄 17"]},
    "12-27": {"old_testament": ["尼希米記 6-7"], "new_testament": ["啟示錄 18"]},
    "12-28": {"old_testament": ["尼希米記 8-10"], "new_testament": ["啟示錄 19"]},
    "12-29": {"old_testament": ["尼希米記 11-13"], "new_testament": ["啟示錄 20"]},
    "12-30": {"old_testament": ["瑪拉基書 1-2"], "new_testament": ["啟示錄 21"]},
    "12-31": {"old_testament": ["瑪拉基書 3-4"], "new_testament": ["啟示錄 22"]}
}
# 全年讀經計劃總字典合併
full_year_reading_plan = {}

# 依序將各個月份的 dict 合併進來
full_year_reading_plan.update(january_reading_plan)
full_year_reading_plan.update(february_reading_plan)
full_year_reading_plan.update(march_reading_plan)
full_year_reading_plan.update(april_reading_plan)
full_year_reading_plan.update(may_reading_plan)
full_year_reading_plan.update(june_reading_plan)
full_year_reading_plan.update(july_reading_plan)
full_year_reading_plan.update(august_reading_plan)
full_year_reading_plan.update(september_reading_plan)
full_year_reading_plan.update(october_reading_plan)
full_year_reading_plan.update(november_reading_plan)
full_year_reading_plan.update(december_reading_plan)

# 如此一來,您就能在整年任何一天透過 'MM-DD' 獲取經文進度了!
# 測試調用示例:獲取今日進度
today_reading = full_year_reading_plan.get(today_str, "查無進度")

# 格式化日期輸出，例如將 "06-11" 轉換為 "6 月 11 日"
month_str, day_str_split = today_str.split("-")
formatted_date = f"{int(month_str)} 月 {int(day_str_split)} 日"

# 修改後的完整自訂輸出
print(f"今日讀經進度：{formatted_date}")
if isinstance(today_reading, dict):
    print(f"舊約: {today_reading['old_testament']}")
    print(f"新約: {today_reading['new_testament']}")
else:
    print(today_reading)

# 1. 設定郵件基本資料
sender = "yongjiechou@gmail.com"
receiver = "yongjiechou@gmail.com"
password = "nzicqlzhxranoqbv"  # 貼上剛剛申請的密碼，不要留空格

# 2. 建立郵件物件
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "這是 Python 自動寄出的測試信"

# 3. 填寫信件內文 (可使用 'plain' 純文字或 'html' 網頁格式)
body = f"{formatted_date}讀經進度：\n舊約: {today_reading['old_testament']}\n新約: {today_reading['new_testament']}"
msg.attach(MIMEText(body, "plain", "utf-8"))

try:
    # 4. 連線到 Gmail SMTP 伺服器 (TLS 加密連接埠為 587)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # 啟動加密傳輸
        server.login(sender, password)  # 登入驗證
        server.send_message(msg)  # 發送郵件
    print("郵件發送成功！")

except Exception as e:
    print(f"發送失敗，錯誤訊息：{e}")
