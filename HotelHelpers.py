from datetime import date
import json
import Hotel
import ReservationHelpers as rp

hotel_cache = []

# When passed a dictionary of hotel information
# Translates it into a Hotel object.
# > Returns a hotel object.
def dict_to_hotel(hotel_dict: dict) -> Hotel:

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
def hotel_to_dict(hotel: Hotel):
    return hotel.to_dict()

# Takes a list of hotel dictionaries,
# makes them into hotel objects, and appends them to the global hotel list.
def hotels_to_list(hotel_list: list):
    for hotel in hotel_list:
        hotel_cache.append(dict_to_hotel(hotel))

# Find a hotel in the passed list based on it's hotel index / id.
# The list index of the hotel may not always equal the hotel index,
# so this ensures you always access the correct hotel.
# > Returns the hotel found, or null/none if it found no hotel.
def find_hotel_by_index(index: int) -> Hotel or None:
    for hotel in hotel_cache:
        if hotel.get_index() == index:
            return hotel

    return None

def find_certain_hotels(
        room_type: str,
        num_rooms: int,
        req_amenities: dict,
        in_date: date,
        out_date: date,
        price_range_min: int,
        price_range_max: int
        ) -> list:

    output = []
    for hotel in hotel_cache:
        rooms = hotel.get_rooms_dict()
        if room_type not in rooms:
            continue

        has_enough_rooms = False
        final_room_num = hotel.get_num_rooms()
        # Loop through every reservation we have.
        for reservation in rp.reservation_cache:
            if reservation.get_hotel_index() != hotel.get_index():
                continue

            # If the current reservation falls outside of the date specified, we don't need to care
            if in_date < reservation.get_in_date() and out_date > reservation.get_out_date():
                continue

            final_room_num = final_room_num - reservation.get_num_rooms_reserved()
        if final_room_num >= num_rooms:
            has_enough_rooms = True

        # Check that any room type is in our price range
        is_affordabale = False
        if rooms[room_type] <= price_range_max and rooms[room_type] >= price_range_min:
            is_affordabale = True

        # Check that it has all the amenities we want
        has_amenities = True
        for amenity in req_amenities:
            if not req_amenities[amenity]: #We don't want this amenity
                continue
            if amenity not in hotel.get_amenities_lists(): #We don't have an amenity we want
                has_amenities = False

        # If the number of available rooms less than the specified number of rooms, don't show the hotel
        if is_affordabale and has_amenities and has_enough_rooms:
            output.append(hotel_to_dict(hotel))

    return output

# Updates the userfile to the current user cache.
def update_file_with_new_hotel():
    data = []
    for hotel in hotel_cache:
        data.append(hotel_to_dict(hotel))

    hotel_file = open("hotels.json", "w")
    json.dump(data, hotel_file, indent = 2)

    hotel_file.close()
