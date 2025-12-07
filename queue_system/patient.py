"""
Пациент класы
"""

class Patient:
    """
    Пациенттің мәліметтерін сақтайтын класс.

    Attributes:
        id (str): Пациенттің бірегей идентификаторы
        name (str): Пациенттің аты
        age (str): Пациенттің жасы
        doctor (str): Пациентті қабылдайтын дәрігердің аты
        telegram_id (str): Пациенттің Telegram ID
    """

    def __init__(self, id: str, name: str, age: str, doctor: str, telegram_id: str):
        self.id = id
        self.name = name
        self.age = age
        self.doctor = doctor
        self.telegram_id = telegram_id

    def update(self, name: str = None, age: str = None, doctor: str = None, telegram_id: str = None):
        """
        Пациенттің мәліметтерін жаңарту.

        Args:
            name (str, optional): Жаңа аты. Егер бос болса, өзгеріс болмайды.
            age (str, optional): Жаңа жасы.
            doctor (str, optional): Жаңа дәрігер.
            telegram_id (str, optional): Жаңа Telegram ID.
        """
        if name:
            self.name = name
        if age:
            self.age = age
        if doctor:
            self.doctor = doctor
        if telegram_id:
            self.telegram_id = telegram_id

    def __str__(self):
        """Пациентті оқуға ыңғайлы форматта шығару"""
        return f"{self.id} | {self.name} | {self.age} | {self.doctor} | {self.telegram_id}"
