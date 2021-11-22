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

def is_amenity_in_hotel(amenity, hotel):
    return amenity in hotel.get_amenity_list()


def find_certain_hotels(hotel_list, num_rooms, amenity_list, room_type, price_range_low, price_range_high):

    # Get all hotels in the hotel list we were passed and convert them to objects.
    returned_hotels = []
    for hotel in hotel_list:

        # Now we check for amenities.
        # If all amenities in the passed list are found in our hotel's amenity list,
        # then the hotel is valid - otherwise continue the loop to next hotel.
        has_all_amenites = True
        for amenity in amenity_list:
            if not is_amenity_in_hotel(amenity, hotel):
                has_all_amenites = False

        if not has_all_amenites:
            continue

        # Now we check for rooms.
        if len(hotel.get_num_rooms()) < 1:
            continue

        # If we have a valid hotel now, we need to check that it holds our room_type.
        our_rooms = hotel.get_rooms_dict()
        if room_type not in our_rooms:
            continue

        if our_rooms[room_type] >= num_rooms:
            returned_hotels.append(hotel_to_dict(hotel))

    return returned_hotels
