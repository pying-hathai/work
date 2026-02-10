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
import re

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
start_script_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
print(current_script_path)
print('Starting script...')

#อ่านข้อมูลจากไฟล์ config_info.xlsx
time.sleep(3)
template_config = "template_config" # โฟลเดอร์ย่อยที่เก็บไฟล์ config_info.xlsx
input_config_path = os.path.join(current_script_path, template_config, "config_info.xlsx")
xls_config_path = pd.ExcelFile(input_config_path)
df_config_path = pd.read_excel(xls_config_path)

#อ่านข้อมูลจากไฟล์ config_info.xlsx
config_dict = dict(zip(df_config_path['Description'], df_config_path['Info']))
hr_folder = config_dict['hr_path']
hr_done = config_dict['hr_done']
#hr_filename = config_dict['hrinput']
input_mailto = config_dict['mailto']
#print(input_hrpath)
#print(input_hrfile)
#print(input_mailto)

#อ่านข้อมูลจากไฟล์ config_login.xlsx
input_config_login = os.path.join(current_script_path, template_config, "config_login.xlsx")
xls_config_login = pd.ExcelFile(input_config_login)
df_config_login = pd.read_excel(xls_config_login)
#print(df_config_login)

#โฟลเดอร์ย่อยที่เก็บไฟล์ logs ของงาน
statuslog_folder = "logs" 
statuslog_path = os.path.join(current_script_path, template_config, statuslog_folder)
#print(statuslog_path)

# หาไฟล์ .xlsx ล่าสุด ใน folder ของ hr
excel_files = [f for f in os.listdir(hr_folder) if f.endswith('.xlsx')]
if not excel_files:
    #print("ไม่พบไฟล์ .xlsx ในโฟลเดอร์:", hr_folder)
    sys.exit(1)  # หยุดโปรแกรมทันทีด้วย exit code 1 (แสดงว่า error)
# สร้าง path เต็ม
full_paths = [os.path.join(hr_folder, f) for f in excel_files]
# หาไฟล์ที่ใหม่ที่สุด (ตามเวลาแก้ไขล่าสุด)
latest_file = max(full_paths, key=os.path.getmtime)
# แสดงชื่อไฟล์ (เอาเฉพาะชื่อ ไม่เอา path)
hr_filename = os.path.basename(latest_file)
#print(f"ใช้ไฟล์ Excel ล่าสุด: {hr_filename}")

#อ่านข้อมูลจากไฟล์ของ hr 
time.sleep(3)
input_hrpath = os.path.join(hr_folder,hr_filename)
xls_hrfile = pd.ExcelFile(input_hrpath)
df_create = pd.read_excel(xls_hrfile, sheet_name="สร้าง") # อ่านชีทสร้าง
#print(input_hrpath)  #moveไฟล์นี้หลังจากทำเสร็จ

#parameter for role
role1 = "Z:BC_GENERAL"
role2 = "ZBC_ENDUSER"
role3 = "ZCHRSS_ESS_BE01"
role4 = "ZCHRSS_MSS_BE01"
roleFEP = "ZCHRSS_ESS_FE01"

for index, row in df_config_login.iterrows():
    sap_system = row['sap_system']
    client = row['Client']
    username = row['Username']
    #password = row['Password']
    password = password_decryp
    print(sap_system) 
    
    #parameter for log
    status_log = []
    
    #role_list
    if sap_system in ['S4D','S4P' , 'S/4 HANA - PRD'] :
        role_list = [role1, role2, role3, role4]
    else:
        role_list = [roleFEP]

    #start sapgui
    time.sleep(5)
    os.system('taskkill /f /im saplogon.exe')
    time.sleep(5)
    os.startfile("saplogon.exe")
    time.sleep(5)       
    #ควบคุมการทำงานภายในหน้าต่าง SAP GUI
    sap = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    session = sap.OpenConnection(sap_system, True).Children(0)
    
    #login 
    session.findById("wnd[0]/usr/txtRSYST-MANDT").text = client
    session.findById("wnd[0]/usr/txtRSYST-BNAME").text = username
    session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
    session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "TH"
    session.findById("wnd[0]").sendVKey(0)
    time.sleep(2)

    #case multiple login to SAP
    activate_getwin_multilogin()
    time.sleep(2)
    #case found page "ลิขสิทธิ์"
    activate_getwin_license()
    
    #goto tcode su01
    session.findById("wnd[0]/tbar[0]/okcd").text = "su01"
    session.findById("wnd[0]").sendVKey(0)
    
    #parameter for user info อ่านจาก excel
    for index, row in df_create.iterrows():
        input_UserID = row['UserID']
        input_FirstName = row['Firstname']
        input_LastName = row['Lastname']
        input_Department = row['Department']
        input_Email = row['Email']
        input_StartDate = row['วันที่เริ่ม']
        #print(input_UserID)
     
        #แทนค่าตัวแปรด้วยข้อมูลจาก Excel
        create_userid = input_UserID
        #addr
        firstname = input_FirstName
        lastname = input_LastName
        dep = input_Department
        email = input_Email
        #logon data
        usertype = "ESS"
        startdate = input_StartDate
        enddate = "31.12.9999"
        #initial
        lang = "TH"
        time.sleep(1)

        #tcode su01
        session.findById("wnd[0]/usr/ctxtSUID_ST_BNAME-BNAME").text = create_userid
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        time.sleep(1)
    
        #case of found page "การปรับปรุงที่อยู่"
        activate_getwin_userid()
        time.sleep(1)
#
#        #create user is already exist check by status bar
#        #status_text = session.findById("wnd[0]/sbar").Text
#        #if "ผู้ใช้ {input_UserID} มีอยู่แล้ว" in status_text:
#        #    print(f"User already exists. Skipping creation.")
#        #    continue
#    
        #addr
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpADDR").select()
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpADDR/ssubMAINAREA:SAPLSUID_MAINTENANCE:1900/txtSUID_ST_NODE_PERSON_NAME-NAME_LAST").text = lastname
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpADDR/ssubMAINAREA:SAPLSUID_MAINTENANCE:1900/txtSUID_ST_NODE_PERSON_NAME-NAME_FIRST").text = firstname
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpADDR/ssubMAINAREA:SAPLSUID_MAINTENANCE:1900/txtSUID_ST_NODE_WORKPLACE-DEPARTMENT").text = dep
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpADDR/ssubMAINAREA:SAPLSUID_MAINTENANCE:1900/txtSUID_ST_NODE_COMM_DATA-SMTP_ADDR").text = email
        time.sleep(1)
        #logon data
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpLOGO").select()
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpLOGO/ssubMAINAREA:SAPLSUID_MAINTENANCE:1101/btnFKT_DEL").press()
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpLOGO/ssubMAINAREA:SAPLSUID_MAINTENANCE:1101/ctxtSUID_ST_NODE_LOGONDATA-CLASS").text = usertype
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpLOGO/ssubMAINAREA:SAPLSUID_MAINTENANCE:1101/ctxtSUID_ST_NODE_LOGONDATA-GLTGV").text = startdate
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpLOGO/ssubMAINAREA:SAPLSUID_MAINTENANCE:1101/ctxtSUID_ST_NODE_LOGONDATA-GLTGB").text = enddate
        time.sleep(1)
        #initial
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpDEFA").select()
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/ctxtSUID_ST_NODE_DEFAULTS-LANGU").text = lang
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DCPFM").key = "X"
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DCPFM").setFocus()
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG").select()
        #session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpDEFA/ssubMAINAREA:SAPLSUID_MAINTENANCE:1105/cmbSUID_ST_NODE_DEFAULTS-DCPFM").setFocus()
        time.sleep(1)

        #role
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG").select()
        for i,rolei in enumerate(role_list):
            session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").modifyCell(i,"AGR_NAME",rolei)
            session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").modifyCell(i,"UPDATE_FROM_DAT",startdate)
            session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").modifyCell(i,"UPDATE_TO_DAT",enddate)
            time.sleep(1)
    
        #save
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(1)
    
        #get status หลังจากsaveแล้ว
        status_txt = get_status_text()
        time.sleep(1)
    
        #สร้าง dictionary สำหรับเก็บค่า status ของแต่ละ userid
        status_dict = {
            "user_id": create_userid,
            "status": status_txt
        }
        status_log.append(status_dict)
        time.sleep(1)

    time.sleep(3)
    #print(status_log)

    #บันทึกเวลา log
    finish_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # แถวเริ่มต้น
    start_row = pd.DataFrame([{
        "user_id": "Start Script",
        "status": start_script_time
    }])
    # แถวสิ้นสุด
    end_row = pd.DataFrame([{
        "user_id": "Finish Script",
        "status": finish_time
    }])
    #log การทำงาน
    df_log = pd.DataFrame(status_log)
    df_log2 = pd.concat([start_row, df_log, end_row], ignore_index=True)
    # แปลงชื่อให้ safe สำหรับ filename (แทนทุกตัวอักษรไม่ปลอดภัยด้วย "_")
    safe_sap_system = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', sap_system)
    statuslog_path2 = os.path.join(statuslog_path, f"status_log_{safe_sap_system}_{start_script_time}.xlsx")
    df_log2.to_excel(statuslog_path2, index=False)
    #print("บันทึกไฟล์ status_log.xlsx เรียบร้อยแล้ว")
    time.sleep(5)
    
    os.system('taskkill /f /im saplogon.exe')
    time.sleep(5)

    #ส่งเมล outlook
    #automail_send_status(ipsap_system,iptotal_users,iplog_path,iphr_filename,ipmailto)
    automail_send_status(sap_system, len(df_create), statuslog_path2, hr_filename, input_mailto, latest_file)
    time.sleep(10)


time.sleep(5)
xls_config_path.close()
xls_config_login.close()
xls_hrfile.close()

#Move to hr_done
time.sleep(5)
# เอาชื่อไฟล์มาจาก path
hrfile_name = os.path.basename(input_hrpath)
# path ปลายทางแบบเต็ม
dst_path = os.path.join(hr_done, hrfile_name)
# ย้ายไฟล์
shutil.move(input_hrpath, dst_path)
#print(f"ย้ายไฟล์ไปที่: {dst_path}")

