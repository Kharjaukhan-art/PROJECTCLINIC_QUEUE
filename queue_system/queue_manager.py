"""
Кезек жүйесін басқару
"""

from storage.excel_storage import ExcelStorage
from queue_system.patient import Patient
from utils.logger import setup_logger

logger = setup_logger()

class QueueManager:
    """Пациенттер кезегін басқару"""

    def __init__(self):
        self.storage = ExcelStorage()
        self.patients = self.storage.load_patients()
        logger.info("QueueManager іске қосылды, %d пациент жүктелді", len(self.patients))

    def show_all_patients(self):
        if not self.patients:
            print("Кезекте пациент жоқ")
            logger.info("Барлық пациенттер көрсетілді: пациент жоқ")
            return
        print("Барлық пациенттер:")
        for p in self.patients:
            print(f"{p.id} | {p.name} | {p.age} | {p.doctor} | {p.telegram_id}")
        logger.info("Барлық пациенттер көрсетілді, саны: %d", len(self.patients))

    def add_patient(self):
        id = input("ID енгізіңіз: ")
        name = input("Аты: ")
        age = input("Жасы: ")
        doctor = input("Дәрігер: ")
        telegram_id = input("Telegram ID: ")
        patient = Patient(id, name, age, doctor, telegram_id)
        self.patients.append(patient)
        self.storage.save_patient(patient)
        print("Пациент тіркелді.")
        logger.info("Пациент қосылды: %s (%s)", name, id)

    async def call_next_patient(self, bot):
        if not self.patients:
            print("Кезекте пациент жоқ")
            logger.info("Келесі пациент шақырылмады: кезекте пациент жоқ")
            return
        patient = self.patients.pop(0)
        self.storage.remove_patient_by_id(patient.id)
        try:
            await bot.send_message(chat_id=patient.telegram_id,
                                   text=f"Құрметті {patient.name}, сіздің кезегіңіз келді! {patient.doctor} дәрігері сізді күтуде.")
            print(f"{patient.name} шақырылды.")
            logger.info("Пациент шақырылды: %s (%s)", patient.name, patient.id)
        except Exception as e:
            logger.error("Telegram хабарлама жіберілмеді: %s", e)

    def remove_patient(self):
        patient_id = input("Өшіру үшін ID енгізіңіз: ")
        removed = self.storage.remove_patient_by_id(patient_id)
        if removed:
            self.patients = [p for p in self.patients if p.id != patient_id]
            print("Пациент өшірілді")
            logger.info("Пациент өшірілді: %s", patient_id)
        else:
            print("Пациент табылмады")
            logger.warning("Пациент табылмады өшіру кезінде: %s", patient_id)

    def filter_by_doctor(self):
        doctor = input("Дәрігердің аты: ")
        filtered = [p for p in self.patients if p.doctor.lower() == doctor.lower()]
        if not filtered:
            print("Пациент табылмады")
            logger.info("Дәрігер бойынша сүзу: пациент табылмады (%s)", doctor)
            return
        for p in filtered:
            print(f"{p.id} | {p.name} | {p.age} | {p.doctor} | {p.telegram_id}")
        logger.info("Дәрігер бойынша сүзу орындалды: %s, табылды: %d", doctor, len(filtered))

    def search_patient(self):
        key = input("Іздеу (ID немесе аты): ").lower()
        results = [p for p in self.patients if p.id.lower() == key or p.name.lower() == key]
        if not results:
            print("Пациент табылмады")
            logger.info("Пациент іздеу: табылмады (%s)", key)
            return
        for p in results:
            print(f"{p.id} | {p.name} | {p.age} | {p.doctor} | {p.telegram_id}")
        logger.info("Пациент іздеу: %s, табылды: %d", key, len(results))

    def show_statistics(self):
        stats = {}
        for p in self.patients:
            stats[p.doctor] = stats.get(p.doctor, 0) + 1
        if not stats:
            print("Статистика жоқ")
            logger.info("Статистика көрсетілмеді: пациент жоқ")
            return
        print("Пациенттер статистикасы:")
        for doc, count in stats.items():
            print(f"{doc}: {count} пациент")
        logger.info("Статистика көрсетілді: %d дәрігер", len(stats))

    def sort_patients(self):
        field = input("Сұрыптау критерийі (id/name/doctor): ").lower()
        if field in ["id", "name", "doctor"]:
            self.patients.sort(key=lambda x: getattr(x, field))
            print("Пациенттер сұрыпталды.")
            logger.info("Пациенттер сұрыпталды: критерий %s", field)
        else:
            print("Қате критерий")
            logger.warning("Қате сұрыптау критерийі енгізілді: %s", field)

    def update_patient(self):
        patient_id = input("Жаңарту үшін ID енгізіңіз: ")
        for p in self.patients:
            if p.id == patient_id:
                name = input("Жаңа аты: ")
                age = input("Жаңа жасы: ")
                doctor = input("Жаңа дәрігер: ")
                telegram_id = input("Жаңа Telegram ID: ")
                p.update(name=name or None, age=age or None, doctor=doctor or None, telegram_id=telegram_id or None)
                self.storage.remove_patient_by_id(patient_id)
                self.storage.save_patient(p)
                print("Пациент жаңартылды")
                logger.info("Пациент жаңартылды: %s (%s)", p.name, p.id)
                return
        print("Пациент табылмады")
        logger.warning("Пациент табылмады жаңарту кезінде: %s", patient_id)
