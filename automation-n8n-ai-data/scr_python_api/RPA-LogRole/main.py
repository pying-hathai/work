#pip install python-docx pandas openpyxl google-genai
#pip install python-docx requests
#pip install python-dotenv

import requests
import json
from docx import Document
from google import genai
from dotenv import load_dotenv
import os
#pip install pandas openpyxl
import pandas as pd
from io import StringIO

# 0. โหลดการตั้งค่า
print("--- [1/5] Initializing Program ---")

load_dotenv()
API_KEY = os.getenv("API_KEY")
INPUT_PATH = os.getenv("INPUT_PATH")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")

# 1. อ่านไฟล์ DOCX
print("\n--- [2/5] Reading Document ---")

file_path = os.path.join(INPUT_PATH, "Log_input.docx")
doc = Document(file_path)
text = "\n".join([p.text for p in doc.paragraphs])
#print(text)

# 2. เตรียม Prompt
print("\n--- [3/5] Preparing AI Prompt ---")

instruction = """
คุณคือผู้ช่วยที่แปลงข้อความจากเอกสารเป็นตารางข้อมูล JSON เพื่อนำไปทำ CSV/Excel

[เงื่อนไขการสกัดข้อมูล]
- คอลัมน์ที่ต้องการ: Module, Username, Action, System, Role, StartDate, EndDate, Remark
- Module: คัดเลือกเฉพาะ HR, Analytic, MM, FI
- System: คัดเลือกเฉพาะ S4P, FEP
- Action: แบ่งเป็น 3 ประเภทเท่านั้น: 
   1. "เพิ่มสิทธิ์" (ถ้าพบคำว่า assign หรือ เพิ่ม หรือ เพิ่มสิทธิ์) 
   2. "ปิดสิทธิ์" (ถ้าพบคำว่า close หรือ ปิด หรือ ปิดสิทธิ์)
   3. "แก้วันที่สิ้นสุด role"

[กฎการลงวันที่ (Format: dd.mm.yyyy)]
- ปิดสิทธิ์ หรือ close ใส่ค่าใน EndDate
- เพิ่มสิทธิ์ หรือ assign ใส่ค่าใน StartDate
- แก้วันที่สิ้นสุด role ใส่ค่าใน EndDate

[ข้อมูลที่ต้องกรองออก]
- กำหนดสิทธิการคิวรี
- ตรวจสอบงานค้าง
- ตรวจสอบสายการอนุมัติการลา
- ตรวจสอบสายอนุมัติขออยู่ OT
- Maintain Table
- Assign substitution
- ปิด delegate ตำแหน่งว่าง
- Structural Authorize Profile
[ข้อกำหนด Output]
1. 1 Role ต่อ 1 Object (บรรทัด)
2. ถ้าพบข้อมูลซ้ำ (Username + Role + StartDate + EndDate) ให้ใส่คำว่า "duplicate" ใน Remark
3. **สำคัญ**: ตอบกลับในรูปแบบ JSON Array เท่านั้น ห้ามมีคำอธิบายประกอบ ห้ามมี Markdown อื่นนอกจาก [ ]

"""

prompt = instruction + "\n\nข้อมูล:\n" + text


# 3. ส่งข้อมูลให้ AI
print("\n--- [4/5] Calling Gemini API (Gemini) ---")
client = genai.Client(api_key=API_KEY)

# ส่งคำถามไปยังโมเดล (แนะนำ gemini-2.0-flash สำหรับความเร็วและฉลาด)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# ลบ markdown tag ```json ... ``` ออกเพื่อให้เหลือแต่เนื้อ JSON
clean_json = response.text.replace("```json", "").replace("```", "").strip()

# กำหนดชื่อไฟล์ output และรวมเข้ากับ Path
file_name = "LogRole_Report.xlsx"
full_output_path = os.path.join(OUTPUT_PATH, file_name)

# 4. แปลงข้อมูลและบันทึกไฟล์
print("\n--- [5/5] Processing Data & Saving Excel ---")
try:
    data_list = json.loads(clean_json)
    df = pd.DataFrame(data_list)
    
    # บันทึกเป็น Excel
    df.to_excel(full_output_path, index=False)
    print("Success File created at: {full_output_path}")
except Exception as e:
    print("Error parsing JSON:", e)
    print("Response text:", response.text)