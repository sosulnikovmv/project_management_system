import PySimpleGUI as sg
import hashlib

class AppWindow():
    def __init__(self, layouts) -> None:
        self._layouts = layouts
        self._app_name = 'Менеджер проектов'
    def open(self):
        pass

class AuthorizationWindow(AppWindow):
    def __init__(self, wrong_login_or_pw_flag=False) -> None:
        error_message = ''
        if wrong_login_or_pw_flag:
            error_message = 'Ошибка: неверный логин или пароль!'
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
                sg.Text(error_message, text_color='orange')
            ],
            [
                sg.Submit('Вход'), sg.Exit('Выход')
            ]
        ]
        super(AuthorizationWindow, self).__init__(layouts)

    def open(self):
        window = sg.Window(self._app_name, self._layouts)
        while True:
            event, values = window.read()
            if event == 'Выход' or window.was_closed():
                exit()
            elif event == 'Вход':
                pass_md5 = hashlib.md5(bytes(values['pass'].encode())).hexdigest()
                login = values['login']
                window.close()
                return login, pass_md5

class ProfileWindow(AppWindow):
    def __init__(self, user) -> None:
        self.user = user
        if self.user.role == 'manager':
            layouts = [
                [
                    sg.Text('Добро пожаловать, {}!'.format(self.user.name))
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
                    sg.Text('Добро пожаловать, {}!'.format(self.user.name))
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

    def open(self):
        window = sg.Window(self._app_name, self._layouts)
        while True:
            event, values = window.read()
            if event == 'Выход' or window.was_closed():
                exit()

class ManagerRegistrationWindow(AppWindow):
    def __init__(self, inappropriate_login_flag=False, inappropriate_name_flag=False, inappropriate_email_flag=False, login_to_show='manager', name_to_show='', position_to_show='Менеджер', email_to_show='') -> None:
        error_message = ''
        if inappropriate_login_flag:
            error_message += 'Ошибка: этот логин использовать нельзя!\n'
        if inappropriate_name_flag:
            error_message += 'Ошибка: Имя должно содержать только буквы!\n'
        if inappropriate_email_flag:
            error_message += 'Ошибка: E-mail указан неверно!'
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
                sg.Text(error_message, text_color='orange')
            ],
            [
                sg.Submit('Зарегистрировать'), sg.Exit('Выход')
            ]
        ]
        super(ManagerRegistrationWindow, self).__init__(layouts)
    def open(self):
        window = sg.Window(self._app_name, self._layouts)
        while True:
            event, values = window.read()
            if event == 'Выход' or window.was_closed():
                exit()
            elif event == 'Зарегистрировать':
                pass_md5 = hashlib.md5(bytes(values['pass'].encode())).hexdigest()
                window.close()
                return values['login'], pass_md5, values['name'], values['position'], values['email']