from .windows import AuthorizationWindow, ProfileWindow, RegistrationWindow, ListOfEmployeesWindow
from .user import Manager, Employee
import os
import pickle

class ProjectManagement():
    def __init__(self) -> None:
        self._credentials_path = os.path.join('./data', 'credentials.dat')
        self._credentials = dict()
        self._users_data_path = os.path.join('./data', 'users_data.dat')
        self._users_data = dict()
        self._current_user = None
        if os.path.exists(self._credentials_path):
            with open(self._credentials_path, 'rb') as f:
                data = f.read()
                self._credentials = pickle.loads(data)
        if os.path.exists(self._users_data_path):
            with open(self._users_data_path, 'rb') as f:
                data = f.read()
                self._users_data = pickle.loads(data)
            
    
    def start(self) -> None:
        # Create manager user if he is not created
        self._create_manager()
        
        # Application working loop
        event = 'logout'
        while True:
            event = self._action(event)

    def _action(self, event) -> str:
        # Authorization
        if event == 'logout':
            login = self._authorization()
            if self._users_data[login]['role'] == 'manager':
                self._current_user = Manager(**self._users_data[login])
            elif self._users_data[login]['role'] == 'employee':
                self._current_user = Employee(**self._users_data[login])
            return 'main_menu'
        
        # Main menu
        elif event == 'main_menu':
            return self._main_menu(self._current_user)

        # Create user
        elif event == 'create_user':
            event = self._create_user(role='employee')
            return 'main_menu'
        
        # Print employees list
        elif event == 'employees':
            return self._employees_list(role=self._current_user.role)
        
        else:
            raise NotImplementedError
        
    def _main_menu(self, user):
        profile_window = ProfileWindow(user)
        profile_window.open()
        event = profile_window.read()
        profile_window.close()
        return event

    def _authorization(self) -> str:
        authorization_window = AuthorizationWindow()
        authorization_window.open()
        while True:
            login, pass_md5 = authorization_window.read()
            if login in self._credentials and self._credentials[login] == pass_md5:
                break
            else:
                authorization_window.error()
        authorization_window.close()
        return login
    
    def _create_manager(self) -> None:
        if '__manager_login__' not in self._credentials or self._credentials['__manager_login__'] not in self._credentials:
            _ = self._create_user(role='manager')
    
    def _create_user(self, role: str = 'emploee') -> None:
        inappropriate_login_flag = False
        inappropriate_name_flag = False
        inappropriate_email_flag = False
        registration_window = RegistrationWindow(
            role=role,
            login_to_show='manager' if role == 'manager' else '', 
            position_to_show='Менеджер' if role == 'manager' else 'Сотрудник'
        )
        registration_window.open()
        while True:
            event, login, pass_md5, name, position, email = registration_window.read()

            # Turn back to main menu
            if event == 'main_menu':
                break

            # Check login
            inappropriate_login_flag = login == '__manager_login__' or login in self._credentials
            
            # Check and update name
            name, inappropriate_name_flag = self._check_and_update_name(name)
            registration_window.update('name', name)                
            
            # Check and update email
            email, inappropriate_email_flag = self._check_and_update_email(email)
            registration_window.update('email', email)

            # Check all errors
            if not inappropriate_login_flag and not inappropriate_name_flag and not inappropriate_email_flag:
                self._credentials['__manager_login__'] = login
                self._credentials[login] = pass_md5
                self._update_credentials()
                self._users_data[login] = dict()
                self._users_data[login]['login'] = login
                self._users_data[login]['name'] = name
                self._users_data[login]['position'] = position
                self._users_data[login]['email'] = email
                self._users_data[login]['role'] = role
                self._update_users_data()
                break
            else:
                error_message = self._create_error_message(inappropriate_login_flag, inappropriate_name_flag, inappropriate_email_flag)
                registration_window.error(error_message=error_message)
        registration_window.close()
        return event

    def _employees_list(self, role):
        list_of_employees_window = ListOfEmployeesWindow(self._users_data)
        list_of_employees_window.open()
        while True:
            event = list_of_employees_window.read()
            if event == 'main_menu':
                list_of_employees_window.close()
                return event

    def _check_and_update_name(self, name: str) -> tuple:
        # For empty name
        if not name:
            return name, False
        
        # Check if all symbols are alphabetic and splitted with spaces
        name = name.split(' ')
        inappropriate_name_flag = False
        if len(name):
            for elem in name:
                inappropriate_name_flag |= not elem.isalpha()
        else:
            inappropriate_name_flag = True
        
        # Make name to be perceptually appropriate
        temp_name = ''
        for elem in name:
            if elem:
                temp_name += elem.capitalize() + ' '
        name = temp_name[:-1]

        return name, inappropriate_name_flag

    def _check_and_update_email(self, email: str) -> tuple:
        temp_email = email.split('@')
        if len(temp_email) == 2:
            temp_email[-1] = temp_email[-1].split('.')
            if len(temp_email[1]) == 2 and temp_email[0] and temp_email[1][0] and temp_email[1][1]:
                temp_email = temp_email[0].lower() + '@' + temp_email[1][0].lower() + '.' + temp_email[1][1].lower()
                email = temp_email
                return email, False
            else:
                return email.lower(), True
        else:
            return email.lower(), True

    def _create_error_message(self, inappropriate_login_flag: bool, inappropriate_name_flag: bool, inappropriate_email_flag: bool) -> str:
        error_message = ''
        if inappropriate_login_flag:
            error_message += 'Ошибка: этот логин занят!\n'
        if inappropriate_name_flag:
            error_message += 'Ошибка: Имя должно содержать только буквы!\n'
        if inappropriate_email_flag:
            error_message += 'Ошибка: E-mail указан неверно!'
        return error_message

    def _update_credentials(self) -> None:
        with open(self._credentials_path, 'wb') as f:
            data = pickle.dumps(self._credentials)
            f.write(data)       
    
    def _update_users_data(self) -> None:
        with open(self._users_data_path, 'wb') as f:
            data = pickle.dumps(self._users_data)
            f.write(data)       