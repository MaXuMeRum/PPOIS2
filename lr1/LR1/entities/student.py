import json
import os
from pathlib import Path
from entities.material import Material
from entities.exam import Exam


class Student:
    STORAGE_FILE = Path("storage/students.json")

    def __init__(self, student_id, last_name, first_name, exam_result=None, materials=None, readiness=0):
        self.id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.exam_result = exam_result or {}
        self.materials = materials or []
        self.readiness = readiness

    def self_assessment(self):
        print(f"[Самооценка] Текущая готовность: {self.readiness}%")

    def study_topic(self):
        topic_name = input("Введите название темы для изучения (из materials.json): ").strip()

        simple_topic = Material.load_simple_topic(topic_name)

        if simple_topic:
            topic_data_to_store = {"name": topic_name}
            if topic_data_to_store not in self.materials:
                self.materials.append(topic_data_to_store)
                print(f"Тема '{topic_name}' успешно изучена (из materials.json).")
                self.readiness = min(100, self.readiness + 10)
                print(f"[Обновление] Готовность: {self.readiness}%")
            else:
                print(f"Тема '{topic_name}' уже была изучена ранее.")
        else:
            print(f"Тема '{topic_name}' не найдена в materials.json.")

    def take_mock_exam(self):
        subject = input("Введите название предмета для пробного экзамена: ").strip()
        exam = Exam.load(subject)
        if not exam:
            return

        correct_answers = 0
        for i, (topic, question, correct_answer) in enumerate(exam.questions, 1):
            print(f"\nВопрос {i} по теме '{topic}':")
            print(question)
            student_answer = input("Ваш ответ: ").strip()
            if student_answer.lower() == correct_answer.lower():
                print("Верно!")
                correct_answers += 1
                self.readiness = min(100, self.readiness + 20)
            else:
                print(f"Неверно. Правильный ответ: {correct_answer}")
            print(f"[Обновление] Готовность: {self.readiness}%")

        self.exam_result[subject] = f"{correct_answers}/{len(exam.questions)}"
        print(f"\nВы набрали {correct_answers} из {len(exam.questions)} по предмету '{subject}'.")
        self.save()

    def show_status(self):
        print(f"\nСтудент: {self.first_name} {self.last_name} | Готовность: {self.readiness}%")
        print("\nИзученные материалы:")
        if not self.materials:
            print("Нет изученных материалов.")
        for i, m_data in enumerate(self.materials, 1):
            if "name" in m_data:
                print(f"{i}. Тема: '{m_data['name']}' (просто тема)")
            else:
                subject_info = f"(Предмет: {m_data.get('subject', 'Не указан')})" if m_data.get('subject') else ""
                title_info = f"'{m_data.get('title', 'Без названия')}'"
                author_info = f"(Автор: {m_data.get('author', 'Неизвестен')})"
                print(
                    f"{i}. Тема: '{m_data.get('topic', 'Без темы')}' {title_info} {author_info} {subject_info}".strip())

    def save(self):
        os.makedirs(self.STORAGE_FILE.parent, exist_ok=True)
        data = {}
        if self.STORAGE_FILE.exists():
            with open(self.STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[self.id] = {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "exam_result": self.exam_result,
            "materials": self.materials,
            "readiness": self.readiness
        }
        with open(self.STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, student_id):
        if not cls.STORAGE_FILE.exists():
            return None
        with open(cls.STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if student_id in data:
                s_data = data[student_id]
                return cls(s_data["id"], s_data["last_name"], s_data["first_name"],
                           s_data.get("exam_result", {}), s_data.get("materials", []),
                           s_data.get("readiness", 0))
            return None

    @classmethod
    def delete_student(cls, student_id):
        if not cls.STORAGE_FILE.exists():
            return False
        with open(cls.STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if student_id in data:
            del data[student_id]
            with open(cls.STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        return False