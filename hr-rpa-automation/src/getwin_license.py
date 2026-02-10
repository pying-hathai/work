#pip install pywinauto
import pygetwindow as gw
import pyautogui
import time

#windows = gw.getAllWindows()
#
#for win in windows:
#    if win.title:
#        print(win.title)

#window = pyautogui.getWindowsWithTitle("ลิขสิทธิ์")
#if window:
#    window[0].activate()
#    print("พบหน้า ลิขสิทธิ์")

def activate_getwin_license():
    found = False

    # หาหน้าต่างที่ชื่อมีคำว่า "ลิขสิทธิ์"
    for win in gw.getAllWindows():
        if "ลิขสิทธิ์" in win.title:
            window = pyautogui.getWindowsWithTitle(win.title)
            if window:
                window[0].activate()
                #print(f"ลิขสิทธิ์: {win.title}")
                time.sleep(1)
                pyautogui.press('enter')
                found = True
                break

    if not found:
        #print("ไม่พบหน้าต่างชื่อ 'ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย'")
        return False

#ตัวอย่างการใช้งาน
#from getwin_license import activate_getwin_license
#activate_getwin_license()