#pip install pyperclip
#pying.hathai@g hint:cool@
#pying.hathai2@g hint:cool@
#singup to n8n : https://community.n8n.io/signup
#ai key : https://aistudio.google.com/
#Gen openai , api key : https://platform.openai.com/settings/organization/general

import os
import pandas as pd
import time
import sys
from openpyxl import load_workbook
import pyperclip # อย่าลืม import นี้ที่ส่วนบนสุดของสคริปต์ของคุณ
from datetime import datetime

from opensapgui import active_opensapgui
from your_password_module import load_password  # import ฟังก์ชันจากไฟล์ที่บันทึกรหัสไว้


# กำหนดค่าตัวแปรสำหรับการเชื่อมต่อ SAP
sap_system = "S4D"
client = "300"
login_username = "hathaich"  # เปลี่ยนเป็นชื่อผู้ใช้ของคุณ
password = load_password()  # เรียกใช้ฟังก์ชันเพื่อโหลดร
tcode = "su01"
# กำหนด path ของไฟล์ Excel
excel_path = 'G:\My Drive\Automation_SAP\projn8n\output'
saplocation = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"

for file in os.listdir(excel_path):
    if file.endswith('.xlsx') or file.endswith('.xls'):
        dataname = file
        #print(dataname)
        #print(f"Found Excel file: {file}")
        #break

df = pd.read_excel(os.path.join(excel_path, dataname), sheet_name='Sheet')    
df_duplicates = df[df.duplicated(subset=["Username", "Role", "StartDate", "EndDate"], keep=False)]

df2 = df.copy()
df2["Remark"] = ""
df2.loc[df2.duplicated(subset=["Username", "Role", "StartDate", "EndDate"], keep=False), "Remark"] = "Duplicate"

df_no_dup = df.drop_duplicates(subset=["Username", "Role", "StartDate", "EndDate"], keep='first')

grouped = df_no_dup.groupby(["System", "Action", "Username"])   
group_dict = {}
key_list = []

# --- เตรียม Log DataFrame ---
log_columns = ["System", "Action", "Username", "Role", "Message_Type", "Status_Message"]
process_log_df = pd.DataFrame(columns=log_columns)


for (systemi, actioni, usernamei), df_group in grouped:
    group_dict[(systemi, actioni, usernamei)] = df_group
    key_list.append((systemi, actioni, usernamei))
    #print(f"Group: System={systemi}, Action={actioni}, Username={usernamei}")
    #print(df_group)

#print("Keys and Group Dictionary:")
#print(key_list)
#print(group_dict)


for (systemi, actioni, usernamei) in key_list:
    df_process = group_dict[(systemi, actioni, usernamei)]
    print(f"Processing Group: System={systemi}, Action={actioni}, Username={usernamei}")
    print(df_process)

    if systemi == "S4P":
        session = active_opensapgui(sap_system, client, login_username, password, tcode, saplocation)
        time.sleep(5)

        # go to user
        session.findById("wnd[0]/usr/ctxtSUID_ST_BNAME-BNAME").text = usernamei
        session.findById("wnd[0]/tbar[1]/btn[18]").press()
        time.sleep(3)

        # go to tab roles
        session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG").select()
        time.sleep(2)

        if actioni == "assign":
            # find empty row
            rolei = 0  
            while True:
                cell_value = session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").getCellValue(rolei, "AGR_NAME")
                if cell_value in [None, "", " "]:
                    print(f"Row {rolei} is empty, ready to add role.")
                    break
                else:
                    rolei += 1

            # add role
            for index, row in df_process.iterrows():
                rolei_value = row["Role"]
                start_datei = row["StartDate"]
                end_datei = row["EndDate"]

                session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").modifyCell(rolei, "AGR_NAME", rolei_value)
                session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").modifyCell(rolei, "UPDATE_FROM_DAT", start_datei)
                session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell").modifyCell(rolei, "UPDATE_TO_DAT", end_datei)

                rolei += 1
                time.sleep(1)
            

            # save once at the end
            time.sleep(2)
            session.findById("wnd[0]/tbar[0]/btn[11]").press()
            time.sleep(2)

            # read status message
            try:
                # attempt to read message from alv grid and check for errors
                session.findById("wnd[0]/shellcont/shell").currentCellColumn = "T_MSG"
                session.findById("wnd[0]/shellcont/shell").selectedRows = "0"
                message = session.findById("wnd[0]/shellcont/shell").getCellValue(0, "T_MSG")
                print(f"Status message: {message}")

                # Log the result
                # error message showing
                if message != "":
                    for index, row in df_process.iterrows():
                        rolei_value = row["Role"]
                        log_entry = {
                            "System": systemi,
                            "Action": actioni,
                            "Username": usernamei,
                            "Role": rolei_value,
                            "Message_Type": "E",
                            "Status_Message": message
                        }
                        process_log_df = pd.concat([process_log_df, pd.DataFrame([log_entry])], ignore_index=True)
                        print(f"Logged error for role {rolei_value}")

                    #back out if error
                    session.findById("wnd[0]/tbar[0]/btn[3]").press()  # press back button if error
                    session.findById("wnd[1]/usr/btnBUTTON_2").press()  # no recording

            except:
                # if not fails, try to read from status bar
                message = session.findById("wnd[0]/sbar").text
                print(f"Status message from status bar: {message}")

                # Log the result
                for index, row in df_process.iterrows():
                    rolei_value = row["Role"]
                    log_entry = {
                        "System": systemi,
                        "Action": actioni,
                        "Username": usernamei,
                        "Role": rolei_value,
                        "Message_Type": "S",
                        "Status_Message": "Role assigned successfully"
                    }
                    process_log_df = pd.concat([process_log_df, pd.DataFrame([log_entry])], ignore_index=True)
                    print(f"Logged success for role {rolei_value}")
            

            #write log to excel
            with pd.ExcelWriter(os.path.join(excel_path, dataname), mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                process_log_df.to_excel(writer, sheet_name='process_log_assign', index=False)
                #print("Written process log to 'process_log' sheet.")
           


        elif actioni == "close":

            #sort dates to close last date first
            grid = session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell")
            grid.selectColumn("UPDATE_TO_DAT")
            grid.pressToolbarButton("&SORT_DSC")
            time.sleep(2)

            #how many roles in grid
            #rows_count = grid.RowCount
            #print(f"Total roles in grid: {rows_count}")

            if len(df_process) > 0:
                for index, row in df_process.iterrows():
                    role_valuei = row["Role"]
                    end_date_i = row["EndDate"]
                    end_date_dt = datetime.strptime(end_date_i, "%d.%m.%Y").date()
                    print(f"Processing role to close: {role_valuei} with end date {end_date_i}")

                    j = 0
                    while True:
                        grid_AGR_NAME = grid.GetCellValue(j, "AGR_NAME")
                        # ถ้า cell ว่าง ให้หยุด loop
                        if not grid_AGR_NAME:
                            break
                        
                        
                        grid_UPDATE_TO_DAT = grid.GetCellValue(j, "UPDATE_TO_DAT")
                        grid_date_dt = datetime.strptime(grid_UPDATE_TO_DAT, "%d.%m.%Y").date() 
                        

                        if grid_AGR_NAME == role_valuei:
                            is_more_recent = grid_date_dt > end_date_dt
                            if is_more_recent:
                                print(f"index {j}, role name= {grid_AGR_NAME} current end date {grid_UPDATE_TO_DAT} is more recent than {end_date_i}, updating...    ")
                                grid.modifyCell(j, "UPDATE_TO_DAT", end_date_i)  # ตั้งค่าวันที่ปิดเป็นวันที่กำหนด
                                grid.pressEnter()
                                time.sleep(1)                                

                            else:
                                print(f"Skipping: current date is less or equal")
                                break
                            break
                        else:
                            print(f"Not match role: Role name={grid_AGR_NAME}, continue searching...")

                        j += 1


            # read status message
            try:
                # attempt to read message from alv grid and check for errors
                session.findById("wnd[0]/shellcont/shell").currentCellColumn = "T_MSG"
                session.findById("wnd[0]/shellcont/shell").selectedRows = "0"
                message = session.findById("wnd[0]/shellcont/shell").getCellValue(0, "T_MSG")
                print(f"Status message: {message}")
                # Log the result
                # error message showing
                if message != "":
                    for index, row in df_process.iterrows():
                        rolei_value = row["Role"]
                        log_entry = {
                            "System": systemi,
                            "Action": actioni,
                            "Username": usernamei,
                            "Role": rolei_value,
                            "Message_Type": "E",
                            "Status_Message": message
                        }
                        process_log_df = pd.concat([process_log_df, pd.DataFrame([log_entry])], ignore_index=True)
                        print(f"Logged error for role {rolei_value}")
                    #back out if error
                    session.findById("wnd[0]/tbar[0]/btn[3]").press()  # press back button if error
                    session.findById("wnd[1]/usr/btnBUTTON_2").press()  # no recording
            except:
                # if not fails, try to read from status bar
                # save 
                time.sleep(2)
                session.findById("wnd[0]/tbar[0]/btn[11]").press()
                time.sleep(2)
                
                message = session.findById("wnd[0]/sbar").text
                print(f"Status message from status bar: {message}")
                # Log the result
                for index, row in df_process.iterrows():
                    rolei_value = row["Role"]
                    log_entry = {
                        "System": systemi,
                        "Action": actioni,
                        "Username": usernamei,
                        "Role": rolei_value,
                        "Message_Type": "S",
                        "Status_Message": "Role assigned successfully"
                    }
                    process_log_df = pd.concat([process_log_df, pd.DataFrame([log_entry])], ignore_index=True)
                    print(f"Logged success for role {rolei_value}")
            
            #write log to excel
            with pd.ExcelWriter(os.path.join(excel_path, dataname), mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                process_log_df.to_excel(writer, sheet_name='process_log_close', index=False)
                #print("Written process log to 'process_log' sheet.")

