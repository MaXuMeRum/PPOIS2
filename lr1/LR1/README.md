# Система Подготовки Студентов к Экзаменам (CLI)

Эта программная система представляет собой консольное приложение (CLI) для помощи студентам в подготовке к экзаменам, а также для преподавателей для управления учебными материалами и студентами.

## Функциональность

Система предоставляет следующие возможности:

### Для Студентов:
* **Вход в систему:** Авторизация по номеру студенческого билета.
* **Самооценка знаний:** Просмотр текущего уровня готовности к экзаменам и запланированного времени изучения.
* **Консультация по теме:** Проведение консультации по выбранной теме. Система выводит список доступных тем для консультации из `educational_materials.json`. Результатом может быть добавление рекомендованной литературы к изученным материалам студента и повышение готовности.
* **Изучение темы:** Изучение простых тем из файла `materials.json`. Система выводит список доступных простых тем для изучения. Успешное изучение темы повышает уровень готовности.
* **Сдача пробного экзамена:** Прохождение пробного экзамена по выбранному предмету. Система выводит список доступных предметов из `exams.json`. Результаты экзамена оцениваются и обновляется уровень готовности.
* **Запланировать время изучения:** Позволяет студенту добавить дополнительное время к своему общему плану подготовки.

### Для Преподавателей:
* **Добавление данных:**
    * Добавление новых студентов. **При добавлении студента система проверяет, существует ли студент с таким ID, и предотвращает создание дубликата.**
    * Добавление экзаменов (предмет, вопросы, правильные ответы).
    * Добавление дополнительной литературы (с темой, названием, автором, предметом).
    * Добавление простых тем для изучения.
* **Удаление данных:**
    * Удаление студентов.
    * Удаление экзаменов.
    * Удаление дополнительной литературы.
    * Удаление простых тем.

## Структура Проекта

Проект организован следующим образом:

* `main.py`: Точка входа в приложение. Инициализирует консоль и запускает основной цикл программы.
* `console/`: Содержит логику консольного интерфейса и управление состоянием приложения.
    * `console.py`: Основной класс `Console`, который управляет взаимодействием с пользователем, обрабатывает ввод и переключает состояния.
    * `states.py`: Определяет различные состояния приложения (`InitialState`, `StudentState`, `TeacherState`, `AddedState`, `DeletedState`) и их поведение (отображение меню, обработка ввода). Использует шаблон "Состояние" для управления потоком приложения.
* `entities/`: Содержит классы, представляющие основные сущности системы.
    * `student.py`: Класс `Student` для управления данными студента, его результатами экзаменов, изученными материалами, уровнем готовности и **запланированным временем изучения**.
    * `exam.py`: Класс `Exam` для определения структуры экзамена (предмет, вопросы).
    * `material.py`: Класс `Material` для работы с учебными материалами, **объединяющий логику для простых тем (из `materials.json`) и дополнительной литературы (из `educational_materials.json`) с помощью флага `is_simple_topic`**.
    * `additional_classes.py`: Класс `AdditionalClasses` для проведения консультаций.
    * `previous_attempt.py`: Класс `PreviousExamAttempt`, предназначенный для хранения и отображения результатов предыдущих попыток сдачи экзаменов. (Класс присутствует, но на данный момент не используется в основной логике `Student.take_mock_exam()`, где результаты обрабатываются напрямую. Может быть интегрирован для расширения функциональности по ведению истории попыток).
* `storage/`: Директория для хранения данных приложения в формате JSON.
    * `students.json`: Хранит информацию о студентах.
    * `exams.json`: Хранит данные об экзаменах.
    * `materials.json`: Хранит простые темы для изучения.
    * `educational_materials.json`: Хранит информацию о дополнительной литературе.
* `test_entities.py`: Файл, содержащий юнит-тесты для классов, определенных в папке `entities/`.

## Хранение Данных

Все данные в системе хранятся в формате JSON-файлов в директории `storage/`. Каждый класс сущности (студент, экзамен, материал) имеет методы для сохранения (`save()`) и загрузки (`load()`) своих данных из соответствующих JSON-файлов, обеспечивая постоянство данных между запусками приложения.

## Требования

Для запуска системы необходим `Python 3.x`.

## Как Запустить

1.  **Клонируйте репозиторий (если применимо) или распакуйте файлы.**
2.  **Убедитесь, что у вас установлены все необходимые файлы в правильной структуре директорий.**
3.  **Откройте терминал (командную строку) в корневой директории проекта.**
4.  **Запустите главное приложение:**
    ```bash
    python main.py
    ```

## Как Пользоваться

После запуска `main.py` вам будет предложено выбрать роль: "Подготовка к экзамену" (для студентов) или "Добавление данных" (для преподавателей).

* **Для студентов:** После выбора "1", введите свой студенческий ID для входа. Затем выберите желаемое действие из меню студента. Перед запросом ввода названия темы или предмета, система автоматически отобразит список доступных вариантов из базы данных, что упрощает взаимодействие.
* **Для преподавателей:** После выбора "2", вам будет доступно меню для добавления или удаления данных. Следуйте инструкциям в командной строке для выполнения операций. При добавлении нового студента система проверит, не существует ли уже студент с таким же ID.

## Классы

### Exam
Класс, представляющий экзамен.

**Атрибуты**:
* `subject`: Дисциплина, по которой проводится экзамен.
* `questions`: Список вопросов с соответствующими темами и правильными ответами.
    
**Методы**:
* `load(cls, subject: str) -> Optional['Exam']`: Загрузка информации об экзамене по определённому предмету.
* `load_all(cls) -> Dict[str, Dict[str, Any]]`: Загрузка информации обо всех экзаменах из файла.
* `save(self) -> None`: Сохранение информации об экзамене.
* `delete_exam(cls, subject: str) -> bool`: Удаление экзамена из файла по названию предмета. Возвращает `True` в случае успеха, `False` иначе.
* `to_dict(self) -> Dict[str, Any]`: Преобразование информации об экзамене в словарь для сохранения.
 
### Material
Класс, представляющий учебный материал (как простые темы, так и дополнительную литературу).

**Атрибуты**:
* `topic`: Тема учебного материала (обязательно).
* `title`: Название учебного материала (для дополнительной литературы, `None` для простых тем).
* `author`: Автор учебного материала (для дополнительной литературы, `None` для простых тем).
* `subject`: Дисциплина, к которой относится учебный материал (для дополнительной литературы, `None` для простых тем).
* `is_simple_topic`: Флаг, указывающий, является ли это простой темой (`True`) или дополнительной литературой (`False`).

**Методы**:
* `to_dict(self) -> Dict[str, Any]`: Преобразует объект в словарь для сохранения, учитывая `is_simple_topic`.
* `load_educational_material(cls, topic_name: str) -> Optional['Material']`: Загрузка объекта дополнительной литературы по теме.
* `load_simple_topic(cls, topic_name: str) -> Optional['Material']`: Загрузка объекта простой темы по названию.
* `_load_from_file(cls, file_path: Path) -> Dict[str, Any]`: Внутренний метод для загрузки данных из указанного JSON-файла.
* `load_all_educational_materials(cls) -> Dict[str, Any]`: Загрузка всех объектов дополнительной литературы из файла.
* `load_all_simple_topics(cls) -> Dict[str, Any]`: Загрузка всех простых тем из файла.
* `save(self) -> None`: Сохранение учебного материала (либо как простой темы, либо как дополнительной литературы) в соответствующий файл.
* `delete_simple_topic(cls, topic_name: str) -> bool`: Удаление простой темы из файла. Возвращает `True` в случае успеха, `False` иначе.
* `delete_educational_material(cls, topic_name: str) -> bool`: Удаление дополнительной литературы из файла по теме. Возвращает `True` в случае успеха, `False` иначе.

### Student
Класс, представляющий студента.

**Атрибуты**:
* `id`: Номер студенческого билета.
* `last_name`: Фамилия студента.
* `first_name`: Имя студента.
* `exam_result`: Словарь, хранящий результаты пробных экзаменов (например, `{'Математика': '10/15'}`).
* `materials`: Список изученных материалов (включая простые темы и данные о дополнительной литературе).
* `readiness`: Уровень готовности студента к экзаменам (число от 0 до 100).
* `planned_study_time_minutes`: Общее количество минут, запланированных студентом для изучения.

**Методы**:
* `self_assessment(self) -> None`: Отображает текущий уровень готовности студента и запланированное время изучения.
* `study_topic(self) -> None`: Позволяет студенту изучить простую тему из `materials.json`, если она найдена, и увеличивает готовность.
* `take_mock_exam(self) -> None`: Позволяет студенту пройти пробный экзамен по выбранному предмету, оценивает ответы и обновляет готовность.
* `plan_study_time(self) -> None`: Позволяет студенту добавить время к своему общему запланированному времени изучения.
* `show_status(self) -> None`: Отображает общую информацию о студенте, включая готовность, запланированное время и изученные материалы.
* `save(self) -> None`: Сохранение данных студента в файл.
* `load(cls, student_id: str) -> Optional['Student']`: Загрузка данных студента по ID.
* `delete_student(cls, student_id: str) -> bool`: Удаление данных студента из файла по ID. Возвращает `True` в случае успеха, `False` иначе.

### PreviousExamAttempt
Класс, представляющий попытку сдачи экзамена.

**Атрибуты**:
* `exam`: Экзамен, который сдавался (объект `Exam`).
* `answers`: Список ответов студента на вопросы экзамена.

**Методы**:
* `calculate_score(self) -> int`: Метод для подсчета правильных ответов.
* `display_results(self) -> None`: Метод для отображения результатов попытки сдачи экзамена (вопрос, ваш ответ, правильный ответ, итоговый балл).

### AdditionalClasses
Класс, представляющий дополнительные занятия (консультации).

**Атрибуты**:
* `student`: Студент, для которого проводятся дополнительные занятия.
* `topic`: Тема дополнительных занятий.

**Методы**:
* `conduct_consultation(self) -> None`: Метод для проведения консультации по заданной теме. Если материал по теме найден в `educational_materials.json`, он добавляется в изученные материалы студента и увеличивается готовность.

### Console
Класс, представляющий интерфейс командной строки для взаимодействия со студентами и системой.

**Атрибуты**:
* `student`: Текущий авторизованный студент (или `None`).
* `state`: Текущее состояние интерфейса (объект класса-наследника `State`).
* `exam`: Может временно хранить объект `Exam` (не используется как постоянное состояние).

**Методы**:
* `set_state(self, state: State) -> None`: Метод для установки текущего состояния интерфейса.
* `start(self) -> None`: Метод для запуска интерфейса командной строки и основного цикла обработки ввода.
* `log_in(self) -> None`: Метод для осуществления входа студента в систему.
* `process_student_choice(self, choice: str) -> None`: Метод для обработки выбора, сделанного студентом в меню, **включая отображение списков доступных опций перед запросом ввода и обработку новой опции планирования времени.**
* `process_added_choice(self, choice: str) -> None`: Метод для обработки выбора в меню добавления данных (для преподавателя), **включая проверку на существование студента по ID.**
* `process_deleted_choice(self, choice: str) -> None`: Метод для обработки выбора в меню удаления данных (для преподавателя).

## Классы состояний

### State
Абстрактный базовый класс, представляющий состояние интерфейса.

**Атрибуты**:
* `console`: Экземпляр класса `Console`, управляющий состоянием.

**Методы**:
* `show_menu(self) -> None`: Абстрактный метод для отображения меню, специфичного для текущего состояния.
* `handle_input(self, choice: str) -> None`: Абстрактный метод для обработки ввода пользователя, специфичного для текущего состояния.

### InitialState
Класс, представляющий начальное состояние интерфейса (выбор роли).

**Методы**:
* `show_menu(self) -> None`: Отображает меню для выбора роли (студент/преподаватель/выход).
* `handle_input(self, choice: str) -> None`: Обрабатывает выбор пользователя для перехода в соответствующее состояние.

### StudentState
Класс, представляющий состояние интерфейса для авторизованного студента.

**Методы**:
* `show_menu(self) -> None`: Отображает главное меню для студента, **включая новую опцию "Запланировать время изучения."**
* `handle_input(self, choice: str) -> None`: Обрабатывает выбор студента для выполнения операций.

### TeacherState
Класс, представляющий состояние интерфейса для преподавателей.

**Методы**:
* `show_menu(self) -> None`: Отображает меню преподавателя (добавление/удаление данных).
* `handle_input(self, choice: str) -> None`: Обрабатывает выбор преподавателя для перехода в состояние добавления или удаления данных.

### AddedState
Класс, представляющий состояние интерфейса для добавления данных (подменю преподавателя).

**Методы**:
* `show_menu(self) -> None`: Отображает меню для выбора типа данных для добавления.
* `handle_input(self, choice: str) -> None`: Обрабатывает выбор преподавателя для добавления конкретных данных.

### DeletedState
Класс, представляющий состояние интерфейса для удаления данных (подменю преподавателя).

**Методы**:
* `show_menu(self) -> None`: Отображает меню для выбора типа данных для удаления.
* `handle_input(self, choice: str) -> None`: Обрабатывает выбор преподавателя для удаления конкретных данных.