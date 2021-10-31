from math import log
from .windows import AuthorizationWindow, ProfileWindow, ManagerRegistrationWindow
import os
import pickle

class ProjectManagement():
    def __init__(self):
        self._credentials_path = os.path.join('./data', 'credentials.dat')
        self._credentials = dict()
        if os.path.exists(self._credentials_path):
            with open(self._credentials_path, 'rb') as f:
                data = f.read()
                self._credentials = pickle.loads(data)
            
    
    def start(self):
        # Initial manager account registration
        if '__manager_login__' not in self._credentials or self._credentials['__manager_login__'] not in self._credentials:
            reg_flag = True
            inappropriate_login_flag = False
            while reg_flag:
                reg_manager_window = ManagerRegistrationWindow(inappropriate_login_flag)
                login, pass_md5 = reg_manager_window.open()
                if login != '__manager_login__':
                    reg_flag = False
                    self._credentials['__manager_login__'] = login
                    self._credentials[login] = pass_md5
                    self._update_credentials()
                else:
                    inappropriate_login_flag = True
        auth_flag = True
        wrong_login_or_pw = False
        while auth_flag:
            authorization_window = AuthorizationWindow(wrong_login_or_pw_flag=wrong_login_or_pw)
            login, pass_md5 = authorization_window.open()
            if login in self._credentials and self._credentials[login] == pass_md5:
                auth_flag = False
            else:
                wrong_login_or_pw = True

        profile_window = ProfileWindow(login)
        profile_window.open()

    def _update_credentials(self):
        with open(self._credentials_path, 'wb') as f:
            data = pickle.dumps(self._credentials)
            f.write(data)       