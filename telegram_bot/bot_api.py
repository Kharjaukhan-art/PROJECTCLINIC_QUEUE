"""
Telegram Bot API инициализациясы
"""

import os
from dotenv import load_dotenv
from telegram import Bot
from telegram_bot.notifier import TelegramNotifier

load_dotenv()

async def init_bot(queue_manager):
    """Ботты инициализациялау"""
    token = os.getenv("CLINIC_BOT_TOKEN")
    bot = Bot(token=token)
    notifier = TelegramNotifier(bot, queue_manager)
    return notifier
