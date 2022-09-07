class User:
    def __init__(self, index, username, password, first_name, last_name, email_address, phone_num, admin_status):
        self.index = index
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_num = phone_num
        self.admin_status = bool(admin_status)

    def get_index(self):
        return self.index
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_f_name(self):
        return self.first_name
    def get_l_name(self):
        return self.last_name
    def get_email(self):
        return self.email_address
    def get_phone_num(self):
        return self.phone_num
    def get_admin_status(self):
        return self.admin_status

    def set_index(self, x: int):
        self.index = x
    def set_username(self, x):
        self.username = x
    def set_password(self, x):
        self.password = x
    def set_f_name(self, x):
        self.first_name = x
    def set_l_name(self, x):
        self.last_name = x
    def set_email(self, x):
        self.email_address = x
    def set_phone_num(self, x):
        self.phone_num = x
    def set_admin_status(self, x: bool):
        self.admin_status = x

    def to_dict(self):
        return_dict = {}

        return_dict["index"] = self.get_index()
        return_dict["username"] = self.get_username()
        return_dict["password"] = self.get_password()
        return_dict["first_name"] = self.get_f_name()
        return_dict["last_name"] = self.get_l_name()
        return_dict["email_address"] = self.get_email()
        return_dict["phone_num"] = self.get_phone_num()
        return_dict["admin_status"] = self.get_admin_status()

        return return_dict
