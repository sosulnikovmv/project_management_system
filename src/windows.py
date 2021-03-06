import PySimpleGUI as sg
import hashlib

class AppWindow():
    def __init__(self, layouts: list) -> None:
        self._layouts = layouts
        self._app_name = 'Менеджер проектов'
        self._size = (640, 420)

    def open(self):
        pass

    def read(self):
        pass

    def close(self):
        pass

    def error(self):
        pass

    def update(self):
        pass

class AuthorizationWindow(AppWindow):
    def __init__(self) -> None:
        layouts = [
            [
                sg.Text('Авторизация. Введите логин и пароль:')
            ],
            [
                sg.Text('Логин\t'), sg.InputText(key='login')
            ],
            [
                sg.Text('Пароль\t'), sg.InputText(key='pass', password_char='*')
            ],
            [
                sg.Text('', text_color='orange', key='error_message')
            ],
            [
                sg.Submit('Войти', key='submit')
            ]
        ]
        super(AuthorizationWindow, self).__init__(layouts)

    def open(self):
        self._window = sg.Window(self._app_name, self._layouts, size=self._size, resizable=True)

    def read(self):
        while True:
            event, values = self._window.read()
            if event == 'exit' or self._window.was_closed():
                exit()
            elif event == 'submit':
                pass_md5 = hashlib.md5(bytes(values['pass'].encode())).hexdigest()
                login = values['login']
                return login, pass_md5
    
    def error(self):
        self._window.Elem('error_message').Update(value='Ошибка: неверный логин или пароль!')

    def close(self):
        self._window.close()

class ProfileWindow(AppWindow):
    def __init__(self, user) -> None:
        self._user = user
        if self._user.role == 'manager':
            layouts = [
                [
                    sg.Text('Здравствуйте, {}!'.format(self._user.name))
                ],
                [
                    sg.Button('Создать пользователя', key='create_user')
                ],
                [
                    sg.Button('Проекты', key='projects')
                ],
                [
                    sg.Button('Задачи', key='tasks')
                ],
                [
                    sg.Button('Сотрудники', key='employees')
                ],
                [
                    sg.Exit('Выход', key='logout')
                ]
            ]
        elif self._user.role == 'employee':
            layouts = [
                [
                    sg.Text('Здравствуйте, {}!'.format(self._user.name))
                ],
                [
                    sg.Button('Проекты', key='projects')
                ],
                [
                    sg.Button('Задачи', key='tasks')
                ],
                [
                    sg.Exit('Выход', key='logout')
                ]
            ]
        else:
            raise NotImplementedError
        super(ProfileWindow, self).__init__(layouts)

    def open(self) -> None:
        self._window = sg.Window(self._app_name, self._layouts, size=self._size, resizable=True)
    
    def read(self) -> str:
        while True:
            event, values = self._window.read()
            if event == 'exit' or self._window.was_closed():
                exit()
            else:
                return event
    
    def close(self) -> None:
        self._window.close()

class RegistrationWindow(AppWindow):
    def __init__(self, role, login_to_show = 'manager', name_to_show = '', position_to_show = 'Менеджер', email_to_show = '') -> None:        
        layouts = [
            [
                sg.Text('Необходимо создать учётную запись менеджера' if role == 'manager' else 'Создание учётной записи сотрудника')
            ],
            [
                sg.Text('Введите данные:')
            ],
            [
                sg.Text('Логин\t  '), sg.InputText(login_to_show, key='login')
            ],
            [
                sg.Text('Пароль\t  '), sg.InputText(key='pass', password_char='*')
            ],
            [
                sg.Text('Имя\t  '), sg.InputText(name_to_show, key='name')
            ],
            [
                sg.Text('Должность'), sg.InputText(position_to_show, key='position')
            ],
            [
                sg.Text('E-mail\t  '), sg.InputText(email_to_show, key='email')
            ],
            [
                sg.Text('', text_color='orange', key='error_message')
            ],
            [
                sg.Submit('Зарегистрировать', key='submit'), sg.Exit('Выход' if role == 'manager' else 'В главное меню', key='exit' if role == 'manager' else 'main_menu')
            ]
        ]
        super(RegistrationWindow, self).__init__(layouts)
    
    def open(self) -> None:
        self._window = sg.Window(self._app_name, self._layouts, size=self._size, resizable=True)        
    
    def read(self):
        while True:
            event, values = self._window.read()
            if event == 'exit' or self._window.was_closed():
                exit()
            elif event == 'main_menu':
                return event, None, None, None, None, None
            elif event == 'submit':
                pass_md5 = hashlib.md5(bytes(values['pass'].encode())).hexdigest()
                return event, values['login'], pass_md5, values['name'], values['position'], values['email']

    def error(self, error_message: str) -> None:
        self._window.Find('error_message', error_message).Update(value=error_message)
    
    def close(self) -> None:
        self._window.close()

    def update(self, field: str, value: str) -> None:
        self._window.Find(field).Update(value=value)
    
class ListOfEmployeesWindow(AppWindow):
    def __init__(self, users_data: dict) -> None:
        
        list_of_names = [[users_data[login][key] for key in users_data[login]] for login in users_data]
        header = ['Login', 'Имя', 'Должность', 'E-mail', 'Роль']
        layouts = [
            [
                sg.Text('Список сотрудников')
            ],
            [
                #sg.LBox(table, expand_x=True, expand_y=True, horizontal_scroll=True),
                sg.Table(list_of_names, headings=header, vertical_scroll_only=False, expand_x=True, expand_y=True)
            ],
            [
                sg.Exit('В главное меню', key='main_menu')
            ]
        ]
        super().__init__(layouts)
    
    def open(self):
        self._window = sg.Window(self._app_name, self._layouts, size=self._size, resizable=True)

    def read(self):
        while True:
            event, _ = self._window.read()
            if event == 'exit' or self._window.was_closed():
                exit()
            elif event == 'main_menu':
                return event
    
    def error(self):
        return super().error()
    
    def close(self):
        self._window.close()
    
    def update(self):
        return super().update()