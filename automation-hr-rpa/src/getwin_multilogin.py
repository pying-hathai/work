#pip install pywinauto
import pygetwindow as gw
import pyautogui
import time

#windows = gw.getAllWindows()
#
#for win in windows:
#    if win.title:
#        print(win.title)
#window = pyautogui.getWindowsWithTitle("ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย")
#if window:
#    window[0].activate()
#    print("พบ ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย")


def activate_getwin_multilogin():
    found = False

    # หาหน้าต่างที่ชื่อมีคำว่า "ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย"
    for win in gw.getAllWindows():
        if "ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย" in win.title:
            window = pyautogui.getWindowsWithTitle(win.title)
            if window:
                window[0].activate()
                #print(f"ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย: {win.title}")
                time.sleep(1)
                pyautogui.press('tab')
                time.sleep(1)
                pyautogui.press('down')
                time.sleep(1)
                pyautogui.press('enter')
                found = True
                break

    if not found:
        #print("ไม่พบหน้าต่างชื่อ 'ข้อมูลใบอนุญาตสำหรับการเข้าสู่ระบบแบบผู้ใช้หลายราย'")
        return False


#ตัวอย่างการใช้งาน
#from getwin_multilogin import activate_getwin_multilogin
#activate_getwin_multilogin()



