import User
import json

user_cache = []
active_user_index = -1

# Makes a new user object with all passed parameters.
# > Returns a user object.
def make_user(
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_num: str,
        admin_status: bool
        ) -> User:

    return User.User(
        len(user_cache),
        username,
        password,
        first_name,
        last_name,
        email_address,
        phone_num,
        admin_status
        )

# Take a dictionariy representing a user
# and translates it to a user object.
# > Returns a user object.
def dict_to_user(user_dict: dict) -> User:

    index = user_dict["index"]
    username = user_dict["username"]
    password = user_dict["password"]
    first_name = user_dict["first_name"]
    last_name = user_dict["last_name"]
    email_address = user_dict["email_address"]
    phone_num = user_dict["phone_num"]
    admin_status = user_dict["admin_status"]

    return User.User(
        index,
        username,
        password,
        first_name,
        last_name,
        email_address,
        phone_num,
        admin_status
        )

# Takes a user object and converts it to a dictionary.
# > Returns a dictionary.
def user_to_dict(user: User):
    return user.to_dict()

# Takes a list of user dictionaries,
# makes them into user objects,
# and appends them to the global user list.
def users_to_list(user_list: list):
    for user in user_list:
        user_cache.append(dict_to_user(user))

def find_user_by_index(index: int) -> User or None:
    for user in user_cache:
        if user.get_index() == index:
            return user

    return None

# Updates the userfile to the current user cache.
def update_file_with_new_user():
    data = []
    for user in user_cache:
        data.append(user_to_dict(user))

    user_file = open("users.json", "w")
    json.dump(data, user_file, indent = 2)

    user_file.close()

def login(username: str, password: str) -> bool:
    global active_user_index

    for user in user_cache:
        if user.get_username() != username:
            continue

        #check if the password matches
        if user.get_password() != password:
            return False

        set_active_user(user.get_index())

    return True

def logout():
    set_active_user(-1)

def set_active_user(new_index: int):
    global active_user_index
    active_user_index = new_index

def check_if_user_is_admin(user: User) -> bool:
    return user.get_admin_status()

def check_if_active_user_is_admin() -> bool:
    for user in user_cache:
        if user.get_index() == active_user_index:
            return user.get_admin_status()

    return False
