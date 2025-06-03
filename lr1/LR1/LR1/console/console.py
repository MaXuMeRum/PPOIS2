from typing import Optional, Dict, Any
import json

from console.states import AddedState, DeletedState, InitialState, State, StudentState, TeacherState
from entities.additional_classes import AdditionalClasses
from entities.exam import Exam
from entities.material import Material  # Изменено с EducationalMaterial на Material
from entities.student import Student


class Console:
    def __init__(self) -> None:
        self.student: Optional[Student] = None
        self.state: Optional[State] = None
        self.exam: Optional[Exam] = None
        # self.educational_material: Optional[Material] = None # Это поле больше не нужно, т.к. материалы загружаются по требованию
        self.set_state(InitialState(self))

    def set_state(self, state: State) -> None:
        self.state = state

    def start(self) -> None:
        while True:
            try:
                self.state.show_menu()
                choice = input("\nВыберите действие: ").strip()
                self.state.handle_input(choice)
            except KeyboardInterrupt:
                print("\nПрограмма завершена.")
                break
            except Exception as e:
                print(f"\nПроизошла ошибка: {e}")

    def log_in(self) -> None:
        try:
            student_id = input("Введите номер студенческого билета: ").strip()
            if not student_id:
                print("Ошибка: Номер студенческого билета не может быть пустым.")
                return

            student = Student.load(student_id)
            if student is None:
                print("\nВаш номер не был найден в списке.")
                return
            self.student = student
            print(f"Добро пожаловать, {self.student.first_name} {self.student.last_name}!")
        except Exception as e:
            print(f"\nОшибка при входе в систему: {e}")

    def process_student_choice(self, choice: str) -> None:
        if choice == "1":
            if self.student:
                self.student.self_assessment()
            else:
                print("Студент не авторизован.")
        elif choice == "2":  # Консультация по теме
            if self.student:
                available_materials = Material.load_all_educational_materials()
                if not available_materials:
                    print("В базе данных нет доступных материалов для консультации.")
                    return
                print("\nДоступные темы для консультации:")
                for i, (key, material_data) in enumerate(available_materials.items(), 1):
                    print(
                        f"{i}. {material_data.get('topic')} (Название: {material_data.get('title', 'Нет')}, Автор: {material_data.get('author', 'Нет')})")

                topic = input("Введите название темы для консультации (из списка выше): ").strip()
                if not topic:
                    print("Ошибка: Тема для консультации не может быть пустой.")
                    return
                consultation = AdditionalClasses(self.student, topic)
                consultation.conduct_consultation()
                self.student.save()
            else:
                print("Студент не авторизован.")
        elif choice == "3":  # Изучение темы
            if self.student:
                available_topics = Material.load_all_simple_topics()
                if not available_topics:
                    print("В базе данных нет доступных простых тем для изучения.")
                    return
                print("\nДоступные темы для изучения:")
                for i, topic_data in enumerate(available_topics.values(),
                                               1):  # Используем .values() т.к. простые темы хранятся по ключу-названию
                    print(f"{i}. {topic_data.get('name')}")

                self.student.study_topic()  # Метод student.study_topic() теперь сам запрашивает ввод темы
                self.student.save()
            else:
                print("Студент не авторизован.")
        elif choice == "4":  # Сдача пробного экзамена
            if self.student:
                available_exams = Exam.load_all()
                if not available_exams:
                    print("В базе данных нет доступных экзаменов.")
                    return
                print("\nДоступные предметы для пробного экзамена:")
                for i, subject_name in enumerate(available_exams.keys(), 1):
                    print(f"{i}. {subject_name}")

                self.student.take_mock_exam()  # Метод student.take_mock_exam() теперь сам запрашивает ввод предмета
                self.student.save()
            else:
                print("Студент не авторизован.")
        elif choice == "5":  # Запланировать время изучения
            if self.student:
                self.student.plan_study_time()
                self.student.save()
            else:
                print("Студент не авторизован.")
        else:
            print("Неверное число!")

    def process_added_choice(self, choice: str) -> None:
        try:
            if choice == "1":  # Add Student
                student_id = input("ID студента: ").strip()
                if not student_id:
                    print("Ошибка: ID студента не может быть пустым.")
                    return

                # Проверка на существование студента с таким ID
                if Student.load(student_id) is not None:
                    print(f"Ошибка: Студент с ID '{student_id}' уже существует. Добавление отменено.")
                    return

                last_name = input("Фамилия: ").strip()
                if not last_name:
                    print("Ошибка: Фамилия студента не может быть пустой.")
                    return
                first_name = input("Имя: ").strip()
                if not first_name:
                    print("Ошибка: Имя студента не может быть пустой.")
                    return

                student = Student(student_id, last_name, first_name)
                student.save()
                print("Операция добавления студента прошла успешно.")
            elif choice == "2":  # Add Exam
                subject = input("Название предмета для экзамена: ").strip()
                if not subject:
                    print("Ошибка: Название предмета для экзамена не может быть пустым.")
                    return

                # Проверка на существование экзамена
                if Exam.load(subject) is not None:
                    print(f"Ошибка: Экзамен по предмету '{subject}' уже существует. Добавление отменено.")
                    return

                questions_data = []
                print("Введите вопросы для экзамена (введите '0' для темы, чтобы завершить):")
                while True:
                    topic = input("Тема вопроса: ").strip()
                    if topic == "0":
                        if not questions_data:
                            print("Ошибка: Экзамен должен содержать хотя бы один вопрос.")
                            return
                        break
                    if not topic:
                        print("Ошибка: Тема вопроса не может быть пустой.")
                        continue
                    question = input("Вопрос: ").strip()
                    if not question:
                        print("Ошибка: Вопрос не может быть пустым.")
                        continue
                    correct_answer = input("Правильный ответ: ").strip()
                    if not correct_answer:
                        print("Ошибка: Правильный ответ не может быть пустым.")
                        continue
                    questions_data.append([topic, question, correct_answer])
                exam = Exam(subject, questions_data)
                exam.save()
                print("Операция добавления экзамена прошла успешно.")
            elif choice == "3":  # Add Educational Material to educational_materials.json
                subject = input("Предмет литературы (необязательно, Enter для пропуска): ").strip()
                topic = input("Тема литературы: ").strip()
                if not topic:
                    print("Ошибка: Тема литературы не может быть пустой.")
                    return

                # Проверка на существование материала
                if Material.load_educational_material(topic) is not None:
                    print(f"Ошибка: Дополнительная литература по теме '{topic}' уже существует. Добавление отменено.")
                    return

                title = input("Название книги/материала: ").strip()
                if not title:
                    print("Ошибка: Название книги/материала не может быть пустой.")
                    return
                author = input("Автор: ").strip()
                if not author:
                    print("Ошибка: Автор не может быть пустой.")
                    return

                new_material = Material(
                    subject=subject if subject else None,
                    topic=topic,
                    title=title,
                    author=author,
                    is_simple_topic=False
                )
                new_material.save()
                print("Операция добавления дополнительной литературы прошла успешно.")
            elif choice == "4":  # Add Topic to materials.json
                topic_name = input("Введите название темы для добавления: ").strip()
                if not topic_name:
                    print("Ошибка: Название темы не может быть пустой.")
                    return

                # Проверка на существование простой темы
                if Material.load_simple_topic(topic_name) is not None:
                    print(f"Ошибка: Простая тема '{topic_name}' уже существует. Добавление отменено.")
                    return

                new_topic = Material(topic=topic_name, is_simple_topic=True)
                new_topic.save()
                print("Операция добавления темы прошла успешно.")
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОперация добавления завершилась ошибкой: {e}")

    def process_deleted_choice(self, choice: str) -> None:
        try:
            if choice == "1":
                student_id = input("ID студента для удаления: ").strip()
                if not student_id:
                    print("Ошибка: ID студента не может быть пустым.")
                    return
                if Student.delete_student(student_id):
                    print("Операция удаления студента прошла успешно.")
                else:
                    print("Не удалось удалить студента: студент не найден или файл со студентами не существует.")
            elif choice == "2":
                subject = input("Название экзамена для удаления: ").strip()
                if not subject:
                    print("Ошибка: Название предмета для экзамена не может быть пустым.")
                    return
                if Exam.delete_exam(subject):
                    print("Операция удаления экзамена прошла успешно.")
                else:
                    print("Не удалось удалить экзамен: экзамен не найден или файл с экзаменами не существует.")
            elif choice == "3":  # Delete Educational Material from educational_materials.json
                topic_name = input("Название темы литературы для удаления: ").strip()
                if not topic_name:
                    print("Ошибка: Название темы литературы не может быть пустой.")
                    return
                if Material.delete_educational_material(topic_name):
                    print("Операция удаления дополнительной литературы прошла успешно.")
                else:
                    print("Не удалось удалить дополнительную литературу: материал не найден.")
            elif choice == "4":  # Delete Topic from materials.json
                topic_name = input("Название темы для удаления: ").strip()
                if not topic_name:
                    print("Ошибка: Название темы не может быть пустой.")
                    return
                if Material.delete_simple_topic(topic_name):
                    print("Операция удаления темы прошла успешно.")
                else:
                    print("Не удалось удалить тему: тема не найдена.")
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОперация удаления завершилась ошибкой: {e}")