"""
Telegram хабарламалар жіберу
"""

class TelegramNotifier:
    """Кезек келгенде хабарлама жіберу"""

    def __init__(self, bot, queue_manager):
        self.bot = bot
        self.queue_manager = queue_manager

    async def send_message(self, chat_id, text):
        try:
            await self.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"Telegram хабарлама жіберілмеді: {e}")
