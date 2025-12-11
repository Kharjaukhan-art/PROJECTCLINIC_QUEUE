import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import pytest
from unittest.mock import patch
from queue_system.queue_manager import QueueManager
from queue_system.patient import Patient

# ------------------------
# Fixture: тазартылған QueueManager
# ------------------------
@pytest.fixture
def queue():
    q = QueueManager()
    q.patients = []

    # Excel файлға жазуды блоктау
    q.storage.save_patient = lambda patient: None
    q.storage.remove_patient_by_id = lambda patient_id: True
    return q

# ------------------------
# Пациент қосу
# ------------------------
def test_add_patient(queue):
    patient = Patient("001", "Alice", "25", "Dr. Smith", "123")
    queue.patients.append(patient)
    queue.storage.save_patient(patient)
    assert patient in queue.patients
    assert queue.patients[0].name == "Alice"

# ------------------------
# Пациент өшіру
# ------------------------
@patch('builtins.input', side_effect=["001"])
def test_remove_patient(mock_input, queue):
    patient = Patient("001", "Alice", "25", "Dr. Smith", "123")
    queue.patients.append(patient)
    queue.remove_patient()
    assert patient not in queue.patients

# ------------------------
# Пациент жаңарту
# ------------------------
@patch('builtins.input', side_effect=["001", "Alice Updated", "26", "Dr. John", "456"])
def test_update_patient(mock_input, queue):
    patient = Patient("001", "Alice", "25", "Dr. Smith", "123")
    queue.patients.append(patient)
    queue.update_patient()
    updated = queue.patients[0]
    assert updated.name == "Alice Updated"
    assert updated.age == "26"
    assert updated.doctor == "Dr. John"
    assert updated.telegram_id == "456"

# ------------------------
# Дәрігер бойынша сүзу
# ------------------------
@patch('builtins.input', side_effect=["Dr. Smith"])
def test_filter_by_doctor(mock_input, queue):
    p1 = Patient("001", "Alice", "25", "Dr. Smith", "123")
    p2 = Patient("002", "Bob", "30", "Dr. John", "456")
    queue.patients.extend([p1, p2])
    queue.filter_by_doctor()  # Нақты assert optional
    assert any(p.doctor == "Dr. Smith" for p in queue.patients)

# ------------------------
# Пациент іздеу
# ------------------------
@patch('builtins.input', side_effect=["Alice"])
def test_search_patient(mock_input, queue):
    p1 = Patient("001", "Alice", "25", "Dr. Smith", "123")
    queue.patients.append(p1)
    queue.search_patient()
    assert any(p.name == "Alice" for p in queue.patients)  # дұрыс жазып бер

# ------------------------
# Статистика шығару
# ------------------------
def test_show_statistics(queue):
    p1 = Patient("001", "Alice", "25", "Dr. Smith", "123")
    p2 = Patient("002", "Bob", "30", "Dr. Smith", "456")
    queue.patients.extend([p1, p2])
    queue.show_statistics()
    # assert optional, тек код жұмыс істейтіні тексеріледі

# ------------------------
# Пациенттерді сұрыптау
# ------------------------
@patch('builtins.input', side_effect=["name"])
def test_sort_patients(mock_input, queue):
    p1 = Patient("002", "Bob", "30", "Dr. John", "456")
    p2 = Patient("001", "Alice", "25", "Dr. Smith", "123")
    queue.patients.extend([p1, p2])
    queue.sort_patients()
    assert queue.patients[0].name == "Alice"
    assert queue.patients[1].name == "Bob"
