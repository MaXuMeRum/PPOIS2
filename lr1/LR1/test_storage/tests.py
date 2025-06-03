import unittest
import json
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from entities.student import Student
from entities.exam import Exam
from entities.material import Material
from entities.additional_classes import AdditionalClasses




class TestEntities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_storage_dir = Path("test_storage")
        cls.test_storage_dir.mkdir(exist_ok=True)

        # Redirect STORAGE_FILE paths for all entities to temporary files
        cls.original_student_file = Student.STORAGE_FILE
        cls.original_exam_file = Exam.STORAGE_FILE
        cls.original_educational_material_file = Material.STORAGE_FILE_EDUCATIONAL
        cls.original_simple_topic_file = Material.STORAGE_FILE_TOPICS
        # cls.original_additional_classes_file = AdditionalClasses.STORAGE_FILE # If AdditionalClasses had a storage file

        Student.STORAGE_FILE = cls.test_storage_dir / "test_students.json"
        Exam.STORAGE_FILE = cls.test_storage_dir / "test_exams.json"
        Material.STORAGE_FILE_EDUCATIONAL = cls.test_storage_dir / "test_educational_materials.json"
        Material.STORAGE_FILE_TOPICS = cls.test_storage_dir / "test_materials.json"

    @classmethod
    def tearDownClass(cls):
        # Restore original STORAGE_FILE paths
        Student.STORAGE_FILE = cls.original_student_file
        Exam.STORAGE_FILE = cls.original_exam_file
        Material.STORAGE_FILE_EDUCATIONAL = cls.original_educational_material_file
        Material.STORAGE_FILE_TOPICS = cls.original_simple_topic_file

        # Clean up temporary test storage directory
        for f in cls.test_storage_dir.iterdir():
            if f.is_file():
                f.unlink()
        cls.test_storage_dir.rmdir()

    def setUp(self):
        for path in [
            Student.STORAGE_FILE,
            Exam.STORAGE_FILE,
            Material.STORAGE_FILE_EDUCATIONAL,
            Material.STORAGE_FILE_TOPICS
        ]:
            if path.exists():
                path.unlink()
            # Create empty JSON files
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    # --- Test for Student class ---
    def test_student_init(self):
        student = Student("123", "Doe", "John")
        self.assertEqual(student.id, "123")
        self.assertEqual(student.last_name, "Doe")
        self.assertEqual(student.first_name, "John")
        self.assertEqual(student.exam_result, {})
        self.assertEqual(student.materials, [])
        self.assertEqual(student.readiness, 0)

    def test_student_save_and_load(self):
        student = Student("123", "Doe", "John", {"Math": "80/100"}, [{"name": "Algebra"}], 50)
        student.save()

        loaded_student = Student.load("123")
        self.assertIsNotNone(loaded_student)
        self.assertEqual(loaded_student.id, "123")
        self.assertEqual(loaded_student.last_name, "Doe")
        self.assertEqual(loaded_student.first_name, "John")
        self.assertEqual(loaded_student.exam_result, {"Math": "80/100"})
        self.assertEqual(loaded_student.materials, [{"name": "Algebra"}])
        self.assertEqual(loaded_student.readiness, 50)

        # Test loading non-existent student
        self.assertIsNone(Student.load("999"))

    def test_student_delete(self):
        student = Student("123", "Doe", "John")
        student.save()
        self.assertTrue(Student.delete_student("123"))
        self.assertIsNone(Student.load("123"))
        # Test deleting non-existent student
        self.assertFalse(Student.delete_student("999"))

    @patch('builtins.input', side_effect=['Test Topic'])
    @patch('entities.material.Material.load_simple_topic',
           return_value=Material(topic="Test Topic", is_simple_topic=True))
    def test_student_study_topic(self, mock_load_topic, mock_input):
        student = Student("123", "Doe", "John")
        initial_readiness = student.readiness
        student.study_topic()
        self.assertIn({"name": "Test Topic"}, student.materials)
        self.assertEqual(student.readiness, min(100, initial_readiness + 10))

    def test_exam_init(self):
        exam = Exam("Math", [("topic1", "q1", "a1")])
        self.assertEqual(exam.subject, "Math")
        self.assertEqual(exam.questions, [("topic1", "q1", "a1")])

    def test_exam_save_and_load(self):
        exam = Exam("Physics", [("Light", "What is c?", "speed of light")])
        exam.save()

        loaded_exam = Exam.load("Physics")
        self.assertIsNotNone(loaded_exam)
        self.assertEqual(loaded_exam.subject, "Physics")
        self.assertEqual(loaded_exam.questions, [("Light", "What is c?", "speed of light")])

        self.assertIsNone(Exam.load("NonExistentSubject"))

    def test_exam_delete(self):
        exam = Exam("Chemistry", [("Elements", "What is H?", "Hydrogen")])
        exam.save()
        self.assertTrue(Exam.delete_exam("Chemistry"))
        self.assertIsNone(Exam.load("Chemistry"))
        self.assertFalse(Exam.delete_exam("NonExistentSubject"))

    # --- Test for Material class ---
    def test_material_init(self):
        # Educational Material
        mat_edu = Material(topic="History", title="World History", author="Author A", subject="History",
                           is_simple_topic=False)
        self.assertEqual(mat_edu.topic, "History")
        self.assertEqual(mat_edu.title, "World History")
        self.assertEqual(mat_edu.author, "Author A")
        self.assertEqual(mat_edu.subject, "History")
        self.assertFalse(mat_edu.is_simple_topic)

        # Simple Topic
        mat_simple = Material(topic="Quantum Physics", is_simple_topic=True)
        self.assertEqual(mat_simple.topic, "Quantum Physics")
        self.assertTrue(mat_simple.is_simple_topic)
        self.assertIsNone(mat_simple.title)
        self.assertIsNone(mat_simple.author)
        self.assertIsNone(mat_simple.subject)

    def test_material_save_load_educational(self):
        mat = Material(topic="Calculus", title="Calculus 101", author="Author B", subject="Math", is_simple_topic=False)
        mat.save()

        loaded_mat = Material.load_educational_material("Calculus")
        self.assertIsNotNone(loaded_mat)
        self.assertEqual(loaded_mat.topic, "Calculus")
        self.assertEqual(loaded_mat.title, "Calculus 101")
        self.assertEqual(loaded_mat.author, "Author B")
        self.assertEqual(loaded_mat.subject, "Math")
        self.assertFalse(loaded_mat.is_simple_topic)
        self.assertIsNone(Material.load_educational_material("NonExistentTopic"))

    def test_material_save_load_simple_topic(self):
        topic = Material(topic="Biology", is_simple_topic=True)
        topic.save()

        loaded_topic = Material.load_simple_topic("Biology")
        self.assertIsNotNone(loaded_topic)
        self.assertEqual(loaded_topic.topic, "Biology")
        self.assertTrue(loaded_topic.is_simple_topic)
        self.assertIsNone(Material.load_simple_topic("NonExistentSimpleTopic"))

    def test_material_delete_educational(self):
        mat = Material(topic="Literature", title="Literary Analysis", author="Author C", is_simple_topic=False)
        mat.save()
        self.assertTrue(Material.delete_educational_material("Literature"))
        self.assertIsNone(Material.load_educational_material("Literature"))
        self.assertFalse(Material.delete_educational_material("NonExistentLiterature"))

    def test_material_delete_simple_topic(self):
        topic = Material(topic="Chemistry Basics", is_simple_topic=True)
        topic.save()
        self.assertTrue(Material.delete_simple_topic("Chemistry Basics"))
        self.assertIsNone(Material.load_simple_topic("Chemistry Basics"))
        self.assertFalse(Material.delete_simple_topic("NonExistentSimpleTopic"))

    # --- Test for AdditionalClasses class ---
    @patch('entities.material.Material.load_educational_material')
    def test_additional_classes_consultation(self, mock_load_material):
        mock_student = Student("mock_id", "Mock", "Student")
        mock_student.materials = []  # Ensure it's empty
        mock_student.readiness = 0

        # Case 1: Material found and added
        mock_material = Material(topic="Math Topic", title="Math Book", author="Math Author", is_simple_topic=False)
        mock_load_material.return_value = mock_material

        consultation = AdditionalClasses(mock_student, "Math Topic")

        with patch('builtins.print') as mock_print:  # Mock print to capture output
            consultation.conduct_consultation()
            self.assertIn(mock_material.to_dict(), mock_student.materials)
            self.assertEqual(mock_student.readiness, 10)
            mock_print.assert_any_call("Рекомендованный материал добавлен:")
            mock_print.assert_any_call(f"- {mock_material.title} (Автор: {mock_material.author})")
            mock_print.assert_any_call("[Обновление] Готовность: 10%")

        # Case 2: Material already present
        mock_student.materials.append(mock_material.to_dict())  # Add it manually
        mock_student.readiness = 10  # Reset readiness for this sub-case
        with patch('builtins.print') as mock_print:
            consultation.conduct_consultation()
            self.assertEqual(mock_student.readiness, 20)  # Readiness should not change
            mock_print.assert_any_call("Материал уже добавлен ранее:")


        mock_load_material.return_value = None
        mock_student.materials = []
        mock_student.readiness = 0
        with patch('builtins.print') as mock_print:
            consultation.conduct_consultation()
            self.assertEqual(mock_student.readiness, 0)  # Readiness should not change
            mock_print.assert_any_call("Материал не найден в educational_materials.json.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)