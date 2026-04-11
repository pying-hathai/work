from datetime import datetime
import os
from PIL import ImageGrab

def capture_screen(errorlog_path,name_prefix="error"):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path2 = os.path.join(errorlog_path, "error.png")

    screenshot = ImageGrab.grab()
    screenshot.save(file_path2)

    print(f"Screenshot saved: {file_path2}")
    return file_path2