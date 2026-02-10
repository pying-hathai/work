#pip install pandas
#pip install openpyxl
#pip install pywin32
#pip install pygetwindow
#pip install pyautogui
#pip install cryptography
import win32com.client
import os
import time
import pandas as pd
import sys  # ใช้สำหรับหยุดโปรแกรมแบบสมบูรณ์
from datetime import datetime
import shutil

#additional function
from getwin_multilogin import activate_getwin_multilogin
from getwin_userid import activate_getwin_userid
from getwin_status import get_status_text
from getwin_license import activate_getwin_license
from sendmail import automail_send_status
from your_password_module import load_password  # import ฟังก์ชันจากไฟล์ที่บันทึกรหัสไว้

# โหลดรหัสผ่านจากไฟล์ที่เข้ารหัสไว้
password_decryp = load_password()
#print("รหัสผ่านที่ถอดรหัสได้:", password)

current_script_path = os.getcwd()
start_script_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(current_script_path)
print('Starting script...')

#อ่านข้อมูลจากไฟล์ config_info.xlsx
time.sleep(3)
template_config = "template_config" # โฟลเดอร์ย่อยที่เก็บไฟล์ config_info.xlsx
input_config_path = os.path.join(current_script_path, template_config, "config_info.xlsx")
xls_config_path = pd.ExcelFile(input_config_path)
df_config_path = pd.read_excel(xls_config_path)