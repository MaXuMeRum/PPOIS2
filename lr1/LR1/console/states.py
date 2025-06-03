from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from console.console import Console # Избегает циклических импортов

class State(ABC):
    def __init__(self, console: 'Console') -> None:
        self.console = console

    @abstractmethod
    def show_menu(self) -> None:
        pass

    @abstractmethod
    def handle_input(self, choice: str) -> None:
        pass


class InitialState(State):
    def show_menu(self) -> None:
        print("\n Выберите пункт")
        print("1. Подготовка к экзамену.")
        print("2. Добавление данных.")
        print("0. Выход.")

    def handle_input(self, choice: str) -> None:
        try:
            if choice == "1":
                self.console.log_in()
                if self.console.student:
                    self.console.set_state(StudentState(self.console))
            elif choice == "2":
                self.console.set_state(TeacherState(self.console))
            elif choice == "0":
                exit()
            else:
                print("Неверный ввод!")
        except Exception as e:
            print(f"\nОшибка: {e}")


class StudentState(State):
    def show_menu(self) -> None:
        print("\n     Главное меню")
        print("1. Самооценка знаний.")
        print("2. Консультация по теме.")
        print("3. Изучение темы.")
        print("4. Сдача пробного экзамена.")
        print("5. Запланировать время изучения.") # Новый пункт
        print("0. Выход.")

    def handle_input(self, choice: str) -> None:
        try:
            if choice == "0":
                self.console.student = None
                self.console.set_state(InitialState(self.console))
                return
            self.console.process_student_choice(choice)
        except Exception as e:
            print(f"\nОшибка при обработке ввода: {e}")


class TeacherState(State):
    def show_menu(self) -> None:
        print("\n     Меню преподавателя")
        print("1. Добавить данные.")
        print("2. Удалить данные.")
        print("0. Выход.")

    def handle_input(self, choice: str) -> None:
        try:
            if choice == "1":
                self.console.set_state(AddedState(self.console))
            elif choice == "2":
                self.console.set_state(DeletedState(self.console))
            elif choice == "0":
                self.console.student = None
                self.console.set_state(InitialState(self.console))
                return
            else:
                print("Неверное число!")
        except Exception as e:
            print(f"\nОшибка при обработке ввода: {e}")


class AddedState(State):
    def show_menu(self) -> None:
        print("\n     Добавить:")
        print("1. Студента.")
        print("2. Экзамен.")
        print("3. Дополнительную литературу.")
        print("4. Тему.")
        print("0. Выход.")

    def handle_input(self, choice: str) -> None:
        try:
            if choice == "0":
                self.console.student = None
                self.console.set_state(TeacherState(self.console))
                return
            self.console.process_added_choice(choice)
        except Exception as e:
            print(f"\nОшибка при добавлении: {e}")


class DeletedState(State):
    def show_menu(self) -> None:
        print("\n     Удалить:")
        print("1. Студента.")
        print("2. Экзамен.")
        print("3. Дополнительную литературу.")
        print("4. Тему.")
        print("0. Выход.")

    def handle_input(self, choice: str) -> None:
        try:
            if choice == "0":
                self.console.student = None
                self.console.set_state(TeacherState(self.console))
                return
            self.console.process_deleted_choice(choice)
        except Exception as e:
            print(f"\nОшибка при удалении: {e}")