import User
import json

user_cache = []
active_user = None

# Makes a new user object with all passed parameters.
# > Returns a user object.
def make_user(username, password, first_name, last_name, email_address, phone_num, admin_status):
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
def dict_to_user(user_dict):

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
def user_to_dict(user):
	return user.to_dict()

# Takes a list of user dictionaries,
# makes them into user objects,
# and appends them to the global user list.
def users_to_list(user_list):
	for user in user_list:
		user_cache.append(dict_to_user(user))

# Updates the userfile to the current user cache.
def update_file_with_new_user():
	data = []
	for user in user_cache:
		data.append(user_to_dict(user))

	user_file = open("users.json", "w")
	json.dump(data, user_file, indent = 2)

	user_file.close()


def login(username, password):
    for user in user_cache:
        if user.get_username() != username:
            continue

        #check if the password matches
        if user.get_password() != password:
            return False
        active_user = user

    return active_user

def logout():
	active_user = None

def check_if_user_is_admin(user):
	return user.get_admin_status()

def check_if_active_user_is_admin():
	return active_user.get_admin_status()
