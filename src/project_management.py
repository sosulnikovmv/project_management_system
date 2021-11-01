from .windows import AuthorizationWindow, ProfileWindow, ManagerRegistrationWindow
from .user import Manager, Employee
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
            inappropriate_email_flag = False
            name_to_show = ''
            login_to_show = 'manager'
            position_to_show = 'Менеджер'
            email_to_show = ''
            while reg_flag:
                reg_manager_window = ManagerRegistrationWindow(
                    inappropriate_login_flag=inappropriate_login_flag, 
                    inappropriate_name_flag=inappropriate_name_flag, 
                    inappropriate_email_flag=inappropriate_email_flag,
                    login_to_show=login_to_show, 
                    name_to_show=name_to_show,
                    position_to_show=position_to_show,
                    email_to_show=email_to_show
                )
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
                
                # Set position to show
                position_to_show = position

                # Check email
                email_to_show = email
                email = email.split('@')
                if len(email) == 2:
                    email[-1] = email[-1].split('.')
                    if len(email[1]) == 2 and email[0] and email[1][0] and email[1][1]:
                        temp_email = email[0].lower() + '@' + email[1][0].lower() + '.' + email[1][1].lower()
                        email = temp_email
                        del temp_email
                        email_to_show = email
                        inappropriate_email_flag = False
                    else:
                        inappropriate_email_flag = True
                else:
                    inappropriate_email_flag = True

                # Check all errors
                if not inappropriate_login_flag and not inappropriate_name_flag and not inappropriate_email_flag:
                    reg_flag = False
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
                
        
        # Authorization
        authorization_window = AuthorizationWindow()
        authorization_window.open()
        while True:
            login, pass_md5 = authorization_window.read()
            if login in self._credentials and self._credentials[login] == pass_md5:
                break
            else:
                authorization_window.error()
        authorization_window.close()

        # Profile window
        if self._users_data[login]['role'] == 'manager':
            current_user = Manager(**self._users_data[login])
        profile_window = ProfileWindow(current_user)
        profile_window.open()

    def _update_credentials(self):
        with open(self._credentials_path, 'wb') as f:
            data = pickle.dumps(self._credentials)
            f.write(data)       
    
    def _update_users_data(self):
        with open(self._users_data_path, 'wb') as f:
            data = pickle.dumps(self._users_data)
            f.write(data)       