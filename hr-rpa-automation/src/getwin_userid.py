#pip install pywinauto
import pygetwindow as gw
import pyautogui
import time

def activate_getwin_userid():
    found = False

    # หาหน้าต่างที่ชื่อมีคำว่า "การปรับปรุงที่อยู่"
    for win in gw.getAllWindows():
        if "การปรับปรุงที่อยู่" in win.title:
            window = pyautogui.getWindowsWithTitle(win.title)
            if window:
                window[0].activate()
                #print(f"พบหน้าต่าง: {win.title}")
                time.sleep(2)
                pyautogui.press('tab')
                time.sleep(2)
                pyautogui.press('enter')
                found = True
                break

    if not found:
        #print("ไม่พบหน้าต่างชื่อ 'การปรับปรุงที่อยู่'")
        return False


    #window = pyautogui.getWindowsWithTitle("การปรับปรุงที่อยู่")
    #if window:
    #    window[0].activate()
    #    print("การปรับปรุงที่อยู่ window found")
    #    pyautogui.press('tab')
    #    time.sleep(2)
    #    pyautogui.press('enter')

#ตัวอย่างการใช้งาน
#from getwin_userid import activate_getwin_userid
#activate_getwin_userid()



