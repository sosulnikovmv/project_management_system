class User():
    def __init__(self, login, name, position, email, role) -> None:
        self._login = login
        self.name = name
        self.position = position
        self.email = email
        self.role = role

class Manager(User):
    def __init__(self, login, name, position, email, role) -> None:
        super(Manager, self).__init__(login, name, position, email, role)

class Employee(User):
    def __init__(self, login, name, position, email, role) -> None:
        super(Employee, self).__init__(login, name, position, email, role)
        