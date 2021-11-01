from .windows import AuthorizationWindow, ProfileWindow, ManagerRegistrationWindow
from .user import Manager, Employee
import os
import pickle

class ProjectManagement():
    def __init__(self) -> None:
        self._credentials_path = os.path.join('./data', 'credentials.dat')
        self._credentials = dict()
        self._users_data_path = os.path.join('./data', 'users_data.dat')
        self._users_data = dict()
        if os.path.exists(self._credentials_path):
            with open(self._credentials_path, 'rb') as f:
                data = f.read()
                self._credentials = pickle.loads(data)
        if os.path.exists(self._users_data_path):
            with open(self._users_data_path, 'rb') as f:
                data = f.read()
                self._users_data = pickle.loads(data)
            
    
    def start(self) -> None:

        # Initial manager account registration
        self._initial_manager_account_registration()
                
        # Authorization
        login = self._authorization()

        # Profile window
        if self._users_data[login]['role'] == 'manager':
            current_user = Manager(**self._users_data[login])
        profile_window = ProfileWindow(current_user)
        profile_window.open()

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
    
    def _initial_manager_account_registration(self) -> None:
        if '__manager_login__' not in self._credentials or self._credentials['__manager_login__'] not in self._credentials:
            inappropriate_login_flag = False
            inappropriate_name_flag = False
            inappropriate_email_flag = False
            reg_manager_window = ManagerRegistrationWindow()
            reg_manager_window.open()
            while True:
                login, pass_md5, name, position, email = reg_manager_window.read()

                # Check login
                inappropriate_login_flag = login == '__manager_login__'
                
                # Check and update name
                name, inappropriate_name_flag = self._check_and_update_name(name)
                reg_manager_window.update('name', name)                
                
                # Check and update email
                email, inappropriate_email_flag = self._check_and_update_email(email)
                reg_manager_window.update('email', email)

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
                    self._users_data[login]['role'] = 'manager'
                    self._update_users_data()
                    break
                else:
                    error_message = self._create_error_message(inappropriate_login_flag, inappropriate_name_flag, inappropriate_email_flag)
                    reg_manager_window.error(error_message=error_message)
            reg_manager_window.close()
    
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
            error_message += 'Ошибка: этот логин использовать нельзя!\n'
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