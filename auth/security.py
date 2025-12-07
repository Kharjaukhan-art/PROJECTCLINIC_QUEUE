"""
Құпия сөзді тексеру
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_password(password: str) -> bool:
    """Парольді .env файлмен салыстыру"""
    clinic_password = os.getenv("CLINIC_PASSWORD")
    return password == clinic_password
