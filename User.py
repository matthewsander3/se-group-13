#This will be a User object, contains:
    #Not really sure how to handle user yet, pushing this for future use
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

    def to_dict(self):
        return_dict = {}

        return_dict["index"] = self.index
        return_dict["username"] = self.get_username()
        return_dict["password"] = self.get_password()
        return_dict["first_name"] = self.get_f_name()
        return_dict["last_name"] = self.get_l_name()
        return_dict["email_address"] = self.get_email()
        return_dict["phone_num"] = self.get_phone_num()
        return_dict["admin_status"] = self.get_admin_status()

        return return_dict
