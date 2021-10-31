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
    def __init__(self, name) -> None:
        layouts = [
            [
                sg.Text('Добро пожаловать, {}!'.format(name)), sg.Exit('Выход')
            ]
        ]
        super(ProfileWindow, self).__init__(layouts)

    def open(self):
        window = sg.Window(self._app_name, self._layouts)
        while True:
            event, values = window.read()
            if event == 'Выход' or window.was_closed():
                exit()

class ManagerRegistrationWindow(AppWindow):
    def __init__(self, inappropriate_login_flag=False) -> None:
        layouts = [
            [
                sg.Text('Необходимо создать учётную запись менеджера')
            ],
            [
                sg.Text('Введите логин и пароль:')
            ],
            [
                sg.Text('Логин\t'), sg.InputText('manager', key='login')
            ],
            [
                sg.Text('Пароль\t'), sg.InputText(key='pass', password_char='*')
            ],
            [
                sg.Text('Ошибка: этот логин использовать нельзя!', text_color='orange') if inappropriate_login_flag else sg.Text()
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
                login = values['login']
                window.close()
                return login, pass_md5