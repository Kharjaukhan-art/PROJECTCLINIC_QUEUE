"""
Логгерді баптау: UTF-8, консоль және файлға жазу
"""

import logging

def setup_logger():
    logger = logging.getLogger("clinic_logger")
    logger.setLevel(logging.DEBUG)  # Барлық деңгейлер жазылады

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Консольге барлық деңгейлер
    ch.setFormatter(formatter)

    # File Handler
    fh = logging.FileHandler("clinic.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)  # Файлға барлық деңгейлер
    fh.setFormatter(formatter)

    # Қайталап қосылмау үшін
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
