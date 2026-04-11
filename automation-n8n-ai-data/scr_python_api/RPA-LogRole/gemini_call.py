#pip install google-genai
from google import genai

from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
#print(API_KEY)

# 1. ตั้งค่า Client ด้วย API Key ของคุณ
client = genai.Client(api_key=API_KEY)

# 2. ส่งคำถามไปยังโมเดล (แนะนำ gemini-2.0-flash สำหรับความเร็วและฉลาด)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="ช่วยแนะนำเมนูอาหารเย็นสำหรับคนลดน้ำหนักหน่อยครับ"
)

# 3. แสดงผลลัพธ์
print(response.text)