import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Material:
    STORAGE_FILE_EDUCATIONAL = Path("storage/educational_materials.json")
    STORAGE_FILE_TOPICS = Path("storage/materials.json") # Для простых тем

    def __init__(self, topic: str, title: Optional[str] = None, author: Optional[str] = None, subject: Optional[str] = None, is_simple_topic: bool = False):
        self.topic = topic
        self.title = title
        self.author = author
        self.subject = subject
        self.is_simple_topic = is_simple_topic

    def to_dict(self) -> Dict[str, Any]:
        if self.is_simple_topic:
            return {"name": self.topic}
        else:
            data = {
                "topic": self.topic,
            }
            if self.subject is not None:
                data["subject"] = self.subject
            if self.title is not None:
                data["title"] = self.title
            if self.author is not None:
                data["author"] = self.author
            return data

    @classmethod
    def load_educational_material(cls, topic_name: str) -> Optional['Material']:
        materials = cls._load_from_file(cls.STORAGE_FILE_EDUCATIONAL)
        for key, data in materials.items():
            if data.get("topic") == topic_name:
                return cls(topic=data.get("topic"),
                           title=data.get("title"),
                           author=data.get("author"),
                           subject=data.get("subject"),
                           is_simple_topic=False)
        return None

    @classmethod
    def load_simple_topic(cls, topic_name: str) -> Optional['Material']:
        topics = cls._load_from_file(cls.STORAGE_FILE_TOPICS)
        if topic_name in topics and topics[topic_name].get("name") == topic_name:
            return cls(topic=topic_name, is_simple_topic=True)
        return None

    @classmethod
    def _load_from_file(cls, file_path: Path) -> Dict[str, Any]:
        if not file_path.exists():
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла {file_path}. Возможно, файл пуст или поврежден. Возвращена пустая база данных.")
            return {}


    @classmethod
    def load_all_educational_materials(cls) -> Dict[str, Any]:
        return cls._load_from_file(cls.STORAGE_FILE_EDUCATIONAL)

    @classmethod
    def load_all_simple_topics(cls) -> Dict[str, Any]:
        return cls._load_from_file(cls.STORAGE_FILE_TOPICS)

    def save(self) -> None:
        if self.is_simple_topic:
            file_path = self.STORAGE_FILE_TOPICS
            data_to_save = self.load_all_simple_topics()
            data_to_save[self.topic] = self.to_dict()
        else:
            file_path = self.STORAGE_FILE_EDUCATIONAL
            data_to_save = self.load_all_educational_materials()
            data_to_save[self.topic] = self.to_dict()

        os.makedirs(file_path.parent, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    @classmethod
    def delete_simple_topic(cls, topic_name: str) -> bool:
        topics = cls._load_from_file(cls.STORAGE_FILE_TOPICS)
        if topic_name in topics:
            del topics[topic_name]
            with open(cls.STORAGE_FILE_TOPICS, "w", encoding="utf-8") as f:
                json.dump(topics, f, ensure_ascii=False, indent=4)
            return True
        return False

    @classmethod
    def delete_educational_material(cls, topic_name: str) -> bool:
        materials = cls._load_from_file(cls.STORAGE_FILE_EDUCATIONAL)
        found_key = None
        for key, data in materials.items():
            if data.get("topic") == topic_name:
                found_key = key
                break
        if found_key:
            del materials[found_key]
            with open(cls.STORAGE_FILE_EDUCATIONAL, "w", encoding="utf-8") as f:
                json.dump(materials, f, ensure_ascii=False, indent=4)
            return True
        return False