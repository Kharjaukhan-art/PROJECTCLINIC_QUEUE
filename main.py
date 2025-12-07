import asyncio
from auth.login import authenticate_user
from queue_system.queue_manager import QueueManager
from telegram_bot.bot_api import init_bot
from utils.logger import setup_logger

logger = setup_logger()

async def main():
    try:
        if not authenticate_user():
            logger.warning("Пайдаланушы жүйеге кіре алмады")
            return

        queue = QueueManager()
        bot = await init_bot(queue)

        logger.info("Бағдарлама іске қосылды")
        while True:
            print("\n--- Кезек жүйесі ---")
            print("1. Келесі пациентті шақыру")
            print("2. Барлық пациенттер")
            print("3. Пациент тіркеу")
            print("4. Пациент өшіру")
            print("5. Дәрігер бойынша сүзу")
            print("6. Пациент іздеу")
            print("7. Статистика")
            print("8. Сұрыптау")
            print("9. Пациент жаңарту")
            print("10. Шығу")

            choice = input("Таңдау жасаңыз: ")

            if choice == "1":
                await queue.call_next_patient(bot)
                logger.info("Келесі пациент шақырылды")
            elif choice == "2":
                queue.show_all_patients()
                logger.info("Барлық пациенттер көрсетілді")
            elif choice == "3":
                queue.add_patient()
                logger.info("Пациент қосылды")
            elif choice == "4":
                queue.remove_patient()
                logger.info("Пациент өшірілді")
            elif choice == "5":
                queue.filter_by_doctor()
                logger.info("Дәрігер бойынша сүзу орындалды")
            elif choice == "6":
                queue.search_patient()
                logger.info("Пациент іздеу орындалды")
            elif choice == "7":
                queue.show_statistics()
                logger.info("Статистика көрсетілді")
            elif choice == "8":
                queue.sort_patients()
                logger.info("Пациенттер сұрыпталды")
            elif choice == "9":
                queue.update_patient()
                logger.info("Пациент жаңартылды")
            elif choice == "10":
                logger.info("Бағдарлама аяқталды")
                print("Бағдарлама аяқталды.")
                break
            else:
                logger.warning("Қате таңдау жасалды: %s", choice)
                print("Қате таңдау. Қайта енгізіңіз.")
    except Exception as e:
        logger.exception("Негізгі циклда қате шықты: %s", e)

if __name__ == "__main__":
    asyncio.run(main())
