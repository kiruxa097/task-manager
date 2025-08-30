class User():  # класс, который обрабатывает имя и права пользователя
    def __init__(self, name, is_admin = False):
        self.name = name
        self.is_admin = is_admin
        print(f"Привет {self.name}")
        print(f"Наличие статуса администратор: {self.is_admin}")

class Task():  #  класс, который обрабатывает задание и его суть, а также меняет его статус
    def __init__(self, title, description, assignee = ""):
        self.title = title
        self.description = description
        self.status = "Требует выполнения"
        self.assignee = assignee

    def done(self):
        self.status = "Выполнен(а)"

    def __repr__(self):
        if not self.assignee:
            return f"Задание: '{self.title}' - [{self.status}]. Исполнитель: не назначен."
        else:
            name_person = self.assignee.name if isinstance(self.assignee, User) else str(self.assignee)
            return f"Задание: '{self.title}' - [{self.status}]. Исполнитель: {name_person}."

# декоратор для проверки прав администратора
def check_admin(func):
    def admin(self, user, *args, **kwargs):
        if user.is_admin:
            return func(self, user, *args, **kwargs)
        else:
            print(f"Доступ для {user.name} запрещен.")
    return admin

# класс, который хранит, добавляет и назначает задачи
class TaskManager():
    def __init__(self):
        self.tasks = []

    @check_admin
    def add_task(self, user, task):
        self.tasks.append(task)
        print(f"Задача {task.title} добавлена.")

    def assign_task(self, task, user):
        task.assignee = user
        print(f"Задача '{task.title}' назначена на {user.name}")

    def show_tasks(self):
        if not self.tasks:
            print("Задач нет.")
            return
        for task in self.tasks:
            print(task)
