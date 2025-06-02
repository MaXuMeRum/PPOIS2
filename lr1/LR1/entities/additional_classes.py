from entities.material import Material


class AdditionalClasses:
    def __init__(self, student, topic):
        self.student = student
        self.topic = topic

    def conduct_consultation(self):
        print(f"\nКонсультация по теме: {self.topic}")
        material = Material.load_educational_material(self.topic)
        if material:
            material_data = material.to_dict()
            if material_data not in self.student.materials:
                self.student.materials.append(material_data)
                print("Рекомендованный материал добавлен:")
            else:
                print("Материал уже добавлен ранее:")

            title_display = material.title if material.title else "Без названия"
            author_display = material.author if material.author else "Неизвестен"
            print(f"- {title_display} (Автор: {author_display})")

            self.student.readiness = min(100, self.student.readiness + 10)
            print(f"[Обновление] Готовность: {self.student.readiness}%")
        else:
            print("Материал не найден в educational_materials.json.")