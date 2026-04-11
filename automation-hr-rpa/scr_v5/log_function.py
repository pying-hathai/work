import os
import csv
from datetime import datetime

def write_log(statuslog_path, level, message, context=""):
    log_file = os.path.join(statuslog_path, "run_log.csv")
    log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    row = [log_time, level, context, message]

    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # ถ้าไฟล์ยังไม่มี → เขียน header
        if not file_exists:
            writer.writerow(["time", "level", "context", "message"])
        
        writer.writerow(row)