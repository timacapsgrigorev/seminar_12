import csv
import os


class FIOValidator:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not value.istitle() or not value.isalpha():
            raise ValueError(f"Недопустимое имя {self.name}. Допускаются только имена с заглавной буквы.")
        setattr(instance, self.name, value)


class Student:
    first_name = FIOValidator()
    last_name = FIOValidator()
    middle_name = FIOValidator()

    def __init__(self, first_name, last_name, middle_name):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.subjects = self.load_subjects()
        self.scores = {subject: {'grades': [], 'test_results': []} for subject in self.subjects}

    def load_subjects(self):
        """Загрузка названий предметов из CSV файла"""
        subjects = []
        with open('subjects.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                subjects.extend(row)
        return subjects


    def add_score(self, subject, grade, test_result):
        """Проверка наличия предмета в списке доступных предметов"""
        if subject not in self.subjects:
            raise ValueError(f"Предмет '{subject}' не найден для студента.")

        """Проверка допустимости оценки и результатов теста"""
        if grade < 2 or grade > 5 or test_result < 0 or test_result > 100:
            raise ValueError("Недопустимая оценка или результат.")

        """Добавление оценки и результатов теста"""
        self.scores[subject]['grades'].append(grade)
        self.scores[subject]['test_results'].append(test_result)

    def average_score(self, subject):
        """Расчет среднего балла по тестам для предмета"""
        if not self.scores[subject]['test_results']:
            return 0
        return sum(self.scores[subject]['test_results']) / len(self.scores[subject]['test_results'])

    def overall_average_score(self):
        """Расчет общего среднего балла по всем предметам"""
        all_scores = []
        for subject in self.subjects:
            all_scores.extend(self.scores[subject]['grades'])
        if not all_scores:
            return 0
        return sum(all_scores) / len(all_scores)


# Создание экземпляра студента
student = Student("Иванов", "Иван", "Иванович")

# Добавление оценок и результатов тестов для предметов
student.add_score("Математика", 4, 85)
student.add_score("Математика", 5, 95)
student.add_score("Физика", 3, 70)
student.add_score("Физика", 4, 90)

# Расчет и вывод среднего балла по предметам
print("Средний балл по математике:", student.average_score("Математика"))
print("Средний балл по физике:", student.average_score("Физика"))

# Расчет и вывод общего среднего балла
print("Общий средний балл:", student.overall_average_score())
