import win32com.client

def get_status_text():
    # เข้าถึง SAP GUI session
    sap = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    application = sap.Children(0)
    connection = application.Children(0)
    session = connection.Children(0)

    # ดึงข้อความจาก status bar
    status_text = session.findById("wnd[0]/sbar").Text
    #print("Status:", status_text)
    return status_text  # <-- คืนค่าผลลัพธ์

#เรียกใช้ฟังก์ชัน
#from getwin_status import get_status_text
#status_txt = get_status_text()
#print("Status:", status_txt)