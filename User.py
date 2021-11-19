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

    def to_dict(self):
        return_dict = {}

        return_dict["index"] = "Test return"

        return return_dict
