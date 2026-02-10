import os
import win32com.client as win32
import pandas as pd

def automail_send_status2(all_mail_results,ipmailto):
  # กำหนด path ไฟล์ Excel ที่ต้องการแนบ
  #file_path  = r"C:\Users\hatha\OneDrive - Chulalongkorn University\Documents\work\pyrpa2\template_config\logs\status_log_S4D.xlsx"

    # สร้างอ็อบเจกต์ Outlook
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)  # 0 = olMailItem

    today_str = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')  # วันที่ปัจจุบันในรูปแบบ YYYY-MM-DD

    # กำหนดรายละเอียดอีเมล
    mail.To = ipmailto          # อีเมลผู้รับ
    mail.Subject = 'รายงานสถานะการสร้างผู้ใช้งานในระบบ'

    # -------------------------
    # Header mail
    # -------------------------
    html_body = f"""
    <p style="font-family:'Cordia New'; font-size:16pt;">
        เรียนทีมงาน,<br>
        รายงานสถานะการสร้างผู้ใช้งานในระบบ
    </p>

    <p style="font-family:'Cordia New'; font-size:16pt;">
        <strong>วันที่:</strong> {today_str}
    </p>
    """

    # -------------------------
    # Loop แต่ละ SAP system
    # -------------------------
    for r in all_mail_results:
        ipsap_system = r["sap_system"]
        iptotal_users = r["total_users"]
        iplog_path = r["log_path"]

        html_body += f"""
        <hr>
        <p style="font-family:'Cordia New'; font-size:16pt;">
            <strong>ระบบ:</strong> {ipsap_system}<br>
            <strong>จำนวน Username ที่สร้าง:</strong> {iptotal_users} รายการ
            <br>
        </p>
        """

        # แนบไฟล์ log ของแต่ละ system
        mail.Attachments.Add(iplog_path)

    # -------------------------
    # Footer
    # -------------------------
    html_body += """
    <p style="font-family:'Cordia New'; font-size:16pt;">
        สามารถตรวจสอบรายละเอียดได้จากไฟล์ log ที่แนบมา<br><br>
        ขอบคุณค่ะ,<br>
        <em>Automation</em><br>
        <em>*This message is auto-sent by RPA*</em>
    </p>
    """

    # ใส่ HTML ทีเดียว
    mail.HTMLBody = html_body

    # แสดง draft (เปลี่ยนเป็น mail.Send() ได้)
    #mail.Display()
    mail.Send()

  #print("ส่งเมล Outlook เรียบร้อยแล้ว")

#from sendmail import automail_send
#automail_send_status(sap_system, total_users, )
#automail_send_status('s4p', 10, r'C:\Users\hatha\OneDrive - Chulalongkorn University\Documents\work\pyrpa2\template_config\logs\status_log_S4D.xlsx', 'hathaichanok.t@chula.ac.th')