import User

user_cache = []

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

def user_to_dict(user):
	return user.to_dict()

def users_to_list(user_list):
	for user in user_list:
		user_cache.append(dict_to_user(user))
