"""
Пайдаланушыны аутентификациялау
"""

import getpass
from auth.security import check_password
from utils.logger import setup_logger

logger = setup_logger()

MAX_ATTEMPTS = 3

def authenticate_user():
    """Пайдаланушыны пароль арқылы тексеру"""
    for attempt in range(MAX_ATTEMPTS):
        password = getpass.getpass("Құпия сөзді енгізіңіз: ")
        if check_password(password):
            print("Сәтті кірдіңіз!")
            return True
        else:
            print("Қате пароль!")
            logger.warning("Қате пароль енгізілді")
    print("Үш рет қате енгізу. Жүйе бұғатталды!")
    return False
