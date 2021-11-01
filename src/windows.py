import PySimpleGUI as sg
import hashlib

class AppWindow():
    def __init__(self, layouts: list) -> None:
        self._layouts = layouts
        self._app_name = 'Менеджер проектов'

    def open(self):
        pass

    def read(self):
        pass

    def close(self):
        pass

    def error(self):
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
                sg.Submit('Вход', key='submit'), sg.Exit('Выход', key='exit')
            ]
        ]
        super(AuthorizationWindow, self).__init__(layouts)

    def open(self):
        self._window = sg.Window(self._app_name, self._layouts)

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
        self.user = user
        if self.user.role == 'manager':
            layouts = [
                [
                    sg.Text('Здравствуйте, {}!'.format(self.user.name))
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
                    sg.Button('Исполнители', key='employees')
                ],
                [
                    sg.Exit('Выход')
                ]
            ]
        elif self.user.role == 'employee':
            layouts = [
                [
                    sg.Text('Здравствуйте, {}!'.format(self.user.name))
                ],
                [
                    sg.Button('Проекты', key='projects')
                ],
                [
                    sg.Button('Задачи', key='tasks')
                ],
                [
                    sg.Exit('Выход')
                ]
            ]
        else:
            raise NotImplementedError
        super(ProfileWindow, self).__init__(layouts)

    def open(self) -> None:
        window = sg.Window(self._app_name, self._layouts)
        while True:
            event, values = window.read()
            if event == 'Выход' or window.was_closed():
                exit()

class ManagerRegistrationWindow(AppWindow):
    def __init__(self, login_to_show = 'manager', name_to_show = '', position_to_show = 'Менеджер', email_to_show = '') -> None:        
        layouts = [
            [
                sg.Text('Необходимо создать учётную запись менеджера')
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
                sg.Submit('Зарегистрировать', key='submit'), sg.Exit('Выход', key='exit')
            ]
        ]
        super(ManagerRegistrationWindow, self).__init__(layouts)
    
    def open(self) -> None:
        self._window = sg.Window(self._app_name, self._layouts)        
    
    def read(self):
        while True:
            event, values = self._window.read()
            if event == 'exit' or self._window.was_closed():
                exit()
            elif event == 'submit':
                pass_md5 = hashlib.md5(bytes(values['pass'].encode())).hexdigest()
                return values['login'], pass_md5, values['name'], values['position'], values['email']

    def error(self, error_message: str) -> None:
        self._window.Find('error_message', error_message).Update(value=error_message)
    
    def close(self) -> None:
        self._window.close()

    def update(self, field: str, value: str) -> None:
        self._window.Find(field).Update(value=value)