import os
import pandas as pd
import time
import sys
from openpyxl import load_workbook

from opensapgui import active_opensapgui
from your_password_module import load_password  # import ฟังก์ชันจากไฟล์ที่บันทึกรหัสไว้


# กำหนดค่าตัวแปรสำหรับการเชื่อมต่อ SAP
sap_system = "S4D"
client = "300"
username = "hathaich"  # เปลี่ยนเป็นชื่อผู้ใช้ของคุณ
password = load_password()  # เรียกใช้ฟังก์ชันเพื่อโหลดร
tcode = "su01"
# กำหนด path ของไฟล์ Excel
excel_path = 'G:\My Drive\projn8n\output'
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

#with pd.ExcelWriter(os.path.join(excel_path, dataname), mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
#    df2.to_excel(writer, sheet_name='dup', index=False)
#    print("Written duplicates to 'dup' sheet.")

df_no_dup = df.drop_duplicates(subset=["Username", "Role", "StartDate", "EndDate"], keep='first')


grouped = df_no_dup.groupby(["System", "Action", "Username"])   
group_dict = {}
key_list = []


for (systemi, actioni, usernamei), df_group in grouped:
    group_dict[(systemi, actioni, usernamei)] = df_group
    key_list.append((systemi, actioni, usernamei))
    print(f"Group: System={systemi}, Action={actioni}, Username={usernamei}")
    print(df_group)

print("Keys and Group Dictionary:")
print(key_list)
print(group_dict)


for (systemi, actioni, usernamei) in key_list:
    df_process = group_dict[(systemi, actioni, usernamei)]
    print(df_process)

    if systemi == "S4P":
        session = active_opensapgui(sap_system, client, username, password, tcode, saplocation)
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

        elif actioni == "close":
            for _, row in df_process.iterrows():
                rolei_value = row["Role"]
                end_datei = row["EndDate"]
            
                grid = session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpACTG/ssubMAINAREA:SAPLSUID_MAINTENANCE:1106/cntlG_ROLES_CONTAINER/shellcont/shell")

                i = 0
                while True:
                    value = grid.GetCellValue(i, "AGR_NAME")

                    # ถ้า cell ว่าง ให้หยุด loop
                    if not value:  
                        break
                    
                    print(f"Row {i}: {value}")

                    # ทำอย่างอื่นกับ row นี้ได้ เช่น modifyCell
                    #if value in df_process["Role"].values:
                    if value == rolei_value:
                        print(f"Closing role: {value} at row {i} with end date {end_datei}")
                        grid.modifyCell(i, "UPDATE_TO_DAT", end_datei)  # ตั้งค่าวันที่ปิดเป็นวันนี้

                    i += 1
            # save once at the end
            time.sleep(2)
            session.findById("wnd[0]/tbar[0]/btn[11]").press()
            time.sleep(2)




