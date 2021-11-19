import Hotel

hotel_cache = []

# When passed a dictionary of hotel information
# Translates it into a Hotel object.
# > Returns a hotel object.
def dict_to_hotel(hotel_dict):

	index = hotel_dict["index"] #Integer
	name = hotel_dict["name"] #String
	num_rooms = hotel_dict["room_num"] #Integer
	diff = hotel_dict["weekend_diff"] #Integer
	rooms_dict = hotel_dict["room_types"] #Dict
	amenities_list = hotel_dict["amenities"] #List

	return Hotel.Hotel(
		index,
		name,
		diff,
		num_rooms,
		rooms_dict,
		amenities_list
		)

# When passed a hotel object
# Translates it into a dict
def hotel_to_dict(hotel):
	return hotel.to_dict()

# Takes a list of hotel dictionaries,
# makes them into hotel objects, and appends them to the global hotel list.
def hotels_to_list(hotel_list):
	for hotel in hotel_list:
		hotel_cache.append(dict_to_hotel(hotel))

# Find a hotel in the passed list based on it's hotel index / id.
# The list index of the hotel may not always equal the hotel index,
# so this ensures you always access the correct hotel.
# > Returns the hotel found, or null/none if it found no hotel.
def find_list_index_of_hotel(index):
	for hotel in hotel_cache:
		if hotel.get_index() == index:
			return hotel

	return None
