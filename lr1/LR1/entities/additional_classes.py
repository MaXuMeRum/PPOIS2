from entities.material import Material  # Изменено с EducationalMaterial на Material


class AdditionalClasses:
    def __init__(self, student, topic):
        self.student = student
        self.topic = topic

    def conduct_consultation(self):
        print(f"\nКонсультация по теме: {self.topic}")
        material = Material.load_educational_material(self.topic)  # Используем load_educational_material
        if material:
            material_data = material.to_dict()
            # Проверяем, есть ли уже материал с такой же темой и типом (образовательный)
            already_added = False
            for m in self.student.materials:
                if m.get('topic') == material_data.get('topic') and 'name' not in m:  # 'name' только у простых тем
                    already_added = True
                    break

            if not already_added:
                self.student.materials.append(material_data)
                print("Рекомендованный материал добавлен:")
                self.student.readiness = min(100, self.student.readiness + 10)
                print(f"[Обновление] Готовность: {self.student.readiness}%")
            else:
                print("Материал уже добавлен ранее:")

            title_display = material.title if material.title else "Без названия"
            author_display = material.author if material.author else "Неизвестен"
            print(f"- {title_display} (Автор: {author_display})")

        else:
            print("Материал не найден в educational_materials.json.")