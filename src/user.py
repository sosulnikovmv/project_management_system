class User():
    def __init__(self, login, name, position, email) -> None:
        self._login = login
        self._name = name
        self._position = position
        self._email = email

class Manager(User):
    def __init__(self, login, name, position, email) -> None:
        super(self, Manager).__init__(login, name, position, email)

class Employee(User):
    def __init__(self, login, name, position, email) -> None:
        super(self, Employee).__init__(login, name, position, email)
        