import os
import win32com.client as win32
import pandas as pd

def automail_send_status(ipsap_system,iptotal_users,iplog_path,iphr_filename,ipmailto,iphr_path):
  # กำหนด path ไฟล์ Excel ที่ต้องการแนบ
  #file_path  = r"C:\Users\hatha\OneDrive - Chulalongkorn University\Documents\work\pyrpa2\template_config\logs\status_log_S4D.xlsx"

  # สร้างอ็อบเจกต์ Outlook
  outlook = win32.Dispatch('outlook.application')
  mail = outlook.CreateItem(0)  # 0 = olMailItem

  sap_system = ipsap_system  # ชื่อระบบที่ต้องการระบุในอีเมล
  today_str = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')  # วันที่ปัจจุบันในรูปแบบ YYYY-MM-DD
  total_users = iptotal_users  # จำนวนผู้ใช้ที่สร้าง (ปรับตามความเหมาะสม)


  # กำหนดรายละเอียดอีเมล
  mail.To = ipmailto          # อีเมลผู้รับ
  mail.Subject = 'รายงานสถานะการสร้างผู้ใช้งานในระบบ ' + sap_system
  #mail.Body = 'ส่งไฟล์ Excel แนบมาด้วยค่ะ'
  # HTML body
  mail.HTMLBody = f"""

  <p style="font-family: 'Cordia New', sans-serif; color: black; font-size: 16pt;">
      เรียนทีมงาน,<br>
      รายงานสถานะการสร้างผู้ใช้งานในระบบ {sap_system}
  </p>

  <p style="font-family: 'Cordia New', sans-serif; color: black; font-size: 16pt;">
      <strong>ระบบ:</strong> {sap_system} <br>
      <strong>วันที่:</strong> {today_str} <br>
      <strong>จำนวน Username ที่สร้าง:</strong> {total_users} รายการ <br>
      <strong>อ้างอิงเอกสาร:</strong> {iphr_filename}
  </p>

  <p style="font-family: 'Cordia New', sans-serif; color: black; font-size: 16pt;">
      สามารถตรวจสอบสถานะการสร้างได้จากไฟล์ log ที่แนบมา 
  </p>

  <p style="font-family: 'Cordia New', sans-serif; color: black; font-size: 16pt;">
      ขอบคุณค่ะ,<br>
      <em>Automation</em> <br>
      <em>*This Message auto send by RPA*</em>
  </p>


  """
  # แนบไฟล์
  mail.Attachments.Add(iplog_path)
  mail.Attachments.Add(iphr_path)

  # ส่งเมล (ถ้าอยากให้เปิดหน้าต่าง draft แทน ให้ใช้ mail.Display() แทน mail.Send())
  mail.Send()
  #mail.Display()

  #print("ส่งเมล Outlook เรียบร้อยแล้ว")

#from sendmail import automail_send
#automail_send_status(sap_system, total_users, )
#automail_send_status('s4p', 10, r'C:\Users\hatha\OneDrive - Chulalongkorn University\Documents\work\pyrpa2\template_config\logs\status_log_S4D.xlsx', 'hathaichanok.t@chula.ac.th')