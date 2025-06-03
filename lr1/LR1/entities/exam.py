import json
import os
from pathlib import Path

class Exam:
    STORAGE_FILE = Path("storage/exams.json")

    def __init__(self, subject=None, questions=None):
        self.subject = subject
        self.questions = questions or []

    @classmethod
    def load(cls, subject):
        exams = cls.load_all()
        if subject not in exams:
            print(f"Экзамен по предмету '{subject}' не найден.")
            return None
        data = exams[subject]
        return cls(subject=data['subject'], questions=[tuple(q) for q in data['questions']])

    @classmethod
    def load_all(cls):
        if not cls.STORAGE_FILE.exists():
            return {}
        with open(cls.STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def to_dict(self):
        return {
            "subject": self.subject,
            "questions": [list(q) for q in self.questions]
        }

    def save(self):
        exams = self.load_all()
        exams[self.subject] = self.to_dict()
        os.makedirs(self.STORAGE_FILE.parent, exist_ok=True)
        with open(self.STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(exams, f, ensure_ascii=False, indent=4)

    @classmethod
    def delete_exam(cls, subject):
        if not cls.STORAGE_FILE.exists():
            return False
        with open(cls.STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if subject in data:
            del data[subject]
            with open(cls.STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        return False