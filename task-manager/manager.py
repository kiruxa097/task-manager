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

# Аналогично верхнему try/except только работает с архивом
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
            print("Такая задача отсутствует!")
        finally:
            print(f"Задача {self.title} успешно выполнена!")

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
    # добавить задачу
    def __init__(self, user, title, description):
        self.title = title
        self.description = description
        self.status = "Требует выполнения"
        for peop in file["users"]:
            if peop["name"] == user.name:
                peop["tasks"][self.title] = self.description
                with open("TaskManager.json", "w", encoding="UTF8") as t_task:
                    json.dump(file, t_task, ensure_ascii=False, indent=2)
        print(f"Задача '{self.title}' - [{self.description}] добавлена. Исполнитель: {user.name}.")

    @check_admin
    # назначить задачу
    def assign_task(self, user, executor, person):
        print(f"Задача {self.title} исполнителя: {executor}, теперь назначена на {person}")
        for u in file["users"]:
            if u["name"] == executor:
                del u["tasks"][self.title]
        for u in file["users"]:
            if u["name"] == person:
                u["tasks"][self.title] = self.description
        with open("TaskManager.json", "w", encoding="UTF8") as f:
            json.dump(file, f, ensure_ascii=False, indent=2)

    @check_admin
    # показать текущий список задач
    def show_tasks(self, user, person):
        print(f"Задачи у пользователя '{person}': ")
        with open("TaskManager.json", "r", encoding="UTF8") as f:
            data = json.load(f)
            for i in data["users"]:
                if i["name"] == person:
                    print(i["tasks"])
                    
