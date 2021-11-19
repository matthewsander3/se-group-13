import Hotel

hotel_cache = []

# When passed a dictionary of hotel information
# (normally, sent from the database)
# Translates it into a HotelObj object.
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
# Translates it into a dict containing:
# - index
# - name
# - rooms
# - weekend differential
# for use in the database
def hotel_to_dict(hotel):
	return hotel.to_dict()

# Takes a list of hotel dictionaries,
# makes them into hotel objects, and appends them to the global hotel list.
# > Returns a list containing all hotels made.
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

# --- Functions to test the above functions. ---
#test_hotel_a = {'index': 0, 'name': 'The Magnolia All Suites', 'weekend_differential': 25, 'rooms': 20}
#test_hotel_b = {'index': 2, 'name': 'The Lofts at Town Centre', 'weekend_differential': 35, 'rooms': 60}
#test_list = [test_hotel_a, test_hotel_b]
#hotels_to_cache(test_list)
#
#for hotel in hotel_cache:
#	print(hotel.to_string())
