from cryptography.fernet import Fernet
import os
import getpass

KEY_FILE = "secret.key"
PASSWORD_FILE = "encrypted_password.bin"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def save_password(plain_password: str):
    key = load_key()
    f = Fernet(key)
    encrypted = f.encrypt(plain_password.encode())
    with open(PASSWORD_FILE, "wb") as f_out:
        f_out.write(encrypted)
    print("รหัสผ่านถูกบันทึกและเข้ารหัสเรียบร้อยแล้ว")

def load_password() -> str:
    key = load_key()
    f = Fernet(key)
    with open(PASSWORD_FILE, "rb") as f_in:
        encrypted = f_in.read()
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()

if __name__ == "__main__":
    # รับรหัสผ่านจากผู้ใช้แบบไม่แสดงบนหน้าจอ
    user_password = getpass.getpass("กรุณาใส่รหัสผ่านที่จะเข้ารหัส: ")
    save_password(user_password)

    # โหลดรหัสผ่านมาแสดง (ถอดรหัส)
    password = load_password()
    #print(f"รหัสผ่านที่ถอดรหัสได้: {password}")
