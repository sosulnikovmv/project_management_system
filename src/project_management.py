from math import log
from .windows import AuthorizationWindow, ProfileWindow, ManagerRegistrationWindow
import os
import pickle

class ProjectManagement():
    def __init__(self):
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
            
    
    def start(self):

        # Initial manager account registration
        if '__manager_login__' not in self._credentials or self._credentials['__manager_login__'] not in self._credentials:
            reg_flag = True
            inappropriate_login_flag = False
            inappropriate_name_flag = False
            name_to_show = ''
            login_to_show = 'manager'
            while reg_flag:
                reg_manager_window = ManagerRegistrationWindow(inappropriate_login_flag=inappropriate_login_flag, inappropriate_name_flag=inappropriate_name_flag, login_to_show=login_to_show, name_to_show=name_to_show)
                login, pass_md5, name, position, email = reg_manager_window.open()
                # Check login
                if login != '__manager_login__':
                    inappropriate_login_flag = False
                else:
                    login_to_show = login
                    inappropriate_login_flag = True
                
                # Check name
                name_to_show = name
                name = name.split(' ')
                inappropriate_name_flag = False
                if len(name):
                    for elem in name:
                        inappropriate_name_flag |= not elem.isalpha()
                else:
                    inappropriate_name_flag = True
                if not inappropriate_name_flag:
                    temp_name = ''
                    for elem in name:
                        temp_name += elem.capitalize() + ' '
                    name = temp_name[:-1]
                    del temp_name
                    name_to_show = name
                
                # Check all errors
                if not inappropriate_login_flag and not inappropriate_name_flag:
                    reg_flag = False
                    self._credentials['__manager_login__'] = login
                    self._credentials[login] = pass_md5
                    self._update_credentials()
                
        
        # Authorization
        auth_flag = True
        wrong_login_or_pw = False
        while auth_flag:
            authorization_window = AuthorizationWindow(wrong_login_or_pw_flag=wrong_login_or_pw_flag)
            login, pass_md5 = authorization_window.open()
            if login in self._credentials and self._credentials[login] == pass_md5:
                auth_flag = False
            else:
                wrong_login_or_pw_flag = True

        # Profile window
        profile_window = ProfileWindow(login)
        profile_window.open()

    def _update_credentials(self):
        with open(self._credentials_path, 'wb') as f:
            data = pickle.dumps(self._credentials)
            f.write(data)       