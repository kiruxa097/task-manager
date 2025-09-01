import json

'''
Попытка открыть файла с форматом json, при ошибке, (т.е при его отсутствии) ->
-> создать новый файл с форматом json, если же файл есть, то присвоить переменной file содержимое json 
'''

try:
    with open("TaskManager.json", "r", encoding="UTF8") as f:
        file = json.load(f)
except FileNotFoundError:
    with open("TaskManager.json", "w", encoding="UTF8") as f:
        r = {"all_tasks" : [], "users" : []}
        json.dump(r, f, ensure_ascii=False, indent=2)
        file = r

# Аналогично верхнему try/except только с архивом
try:
    with open("ArchiveTasks.json", "r", encoding="UTF8") as f1:
        file_archive = json.load(f1)
except FileNotFoundError:
    with open("ArchiveTasks.json", "w", encoding="UTF8") as f1:
        r = {"users" : []}
        json.dump(r, f1, ensure_ascii=False, indent=2)
        file_archive = r

# класс, который обрабатывает имя и права пользователя
class User():
    def __init__(self, name, is_admin = False):
        self.name = name
        self.is_admin = is_admin
        if not any(user["name"] == self.name for user in file["users"]):
            file["users"].append({"name": self.name, "admin": self.is_admin, "tasks": {}})
            with open("TaskManager.json", "w", encoding="UTF8") as f:
                json.dump(file, f, ensure_ascii=False, indent=2)
        if not any(user["name"] == self.name for user in file_archive["users"]):
            file_archive["users"].append({"name": self.name, "tasks": {}})
            with open("ArchiveTasks.json", "w", encoding="UTF8") as f1:
                json.dump(file_archive, f1, ensure_ascii=False, indent=2)
        print(f"Привет {self.name}")
        print(f"Наличие статуса администратор: {self.is_admin}")

#  класс, который обрабатывает задание и его суть, а также меняет его статус
class Task():
    def __init__(self, user, title, description, assignee = ""):
        self.title = title
        self.description = description
        self.status = "Требует выполнения"
        self.assignee = assignee
        for peop in file["users"]:
            if peop["name"] == user.name:
                peop["tasks"][self.title] = self.description
                with open("TaskManager.json", "w", encoding="UTF8") as t_task:
                    json.dump(file, t_task, ensure_ascii=False, indent=2)

    # функция, которая добавляет выполненные задачи в архив, а также ловит ошибки при отсутсвии такого задания
    def done(self, user):
        try:
            for peop in file["users"]:
                if peop["name"] == user.name:
                    for i in file_archive["users"]:
                        if i["name"] == user.name:
                            i["tasks"][self.title] = self.description
                            with open("ArchiveTasks.json", "w", encoding="UTF8") as task:
                                json.dump(file_archive, task, ensure_ascii=False, indent=2)
                    del peop["tasks"][self.title]
                    with open("TaskManager.json", "w", encoding="UTF8") as task:
                        json.dump(file, task, ensure_ascii=False, indent=2)
        except KeyError:
            print("Такое значение отсутствует!")
        finally:
            print(f"Задание {self.title} успешно выполнено!")
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
# в последнем обновлении этот класс не менялся, через несколько дней все задачи будут добавляться в файл json
class TaskManager():
    def __init__(self):
        self.tasks = []

    @check_admin
    # добавить задачу
    def add_task(self, user, task):
        self.tasks.append(task)
        print(f"Задача {task.title} добавлена.")

    # назначить задачу
    def assign_task(self, task, user):
        task.assignee = user
        print(f"Задача '{task.title}' назначена на {user.name}")

    # показать текущий список задач
    def show_tasks(self):
        if not self.tasks:
            print("Задач нет.")
            return
        for task in self.tasks:
            print(task)
