import Reservation
import json
from datetime import date

reservation_cache = []

# Makes a new reservation object with all passed parameters.
# > Returns a reservation object.
def make_reservation(
        user_index: int,
        hotel_index: int,
        num_rooms_reserved: int,
        room_type_reserved: str,
        in_date: date,
        out_date: date
        ) -> Reservation:

    return Reservation.Reservation(
        len(reservation_cache),
        user_index,
        hotel_index,
        num_rooms_reserved,
        room_type_reserved,
        in_date,
        out_date,
        )

# When passed a dictionary of reservation info
# Translates it into a Reservation object.
# > Returns a Reservation object.
def dict_to_reservation(reserve_dict: dict):

    index = len(reservation_cache)
    user_index = reserve_dict["user_index"] #Integer
    hotel_index = reserve_dict["hotel_index"] #Integer
    num_rooms_reserved = reserve_dict["num_rooms_reserved"] #Integer
    room_type_reserved = reserve_dict["room_type_reserved"] #String
    in_date = date(
        reserve_dict["in_date"]["year"],
        reserve_dict["in_date"]["month"],
        reserve_dict["in_date"]["day"]
        )
    out_date = date(
        reserve_dict["out_date"]["year"],
        reserve_dict["out_date"]["month"],
        reserve_dict["out_date"]["day"]
        )

    return Reservation.Reservation(
        index,
        user_index,
        hotel_index,
        num_rooms_reserved,
        room_type_reserved,
        in_date,
        out_date
        )

# When passed a Reservation, converts it to a dictionary.
# > Returns a dict.
def reservation_to_dict(reservation: Reservation):
    return reservation.to_dict()

# Takes a list of Reservation dictionaries,
# makes them into Reservation objects,
# and appends them to the global Reservation list.
def reservations_to_list(reservation_list: list):
    for reservation in reservation_list:
        reservation_cache.append(dict_to_reservation(reservation))

def find_reservation_by_index(index: int):
    for reservation in reservation_cache:
        if reservation.get_index() == index:
            return reservation

    return None

# Finds all reservations in the list that belong
# to a certain hotel index.
# > Returns a list of reservation dictionaries.
def find_reservations_by_hotel_index(index: int):
    output = []
    for reservation in reservation_cache:
        if reservation.hotel_index == index:
            output.append(reservation_to_dict(reservation))

    return output

# Finds all reservations in the list that belong
# to a certain user index.
# > Returns a list of reservation dictionaries.
def find_reservations_by_user_index(index: int):
    output = []
    for reservation in reservation_cache:
        if reservation.user_index == index:
            output.append(reservation_to_dict(reservation))

    return output

# Updates the reservation_file to the current reservation cache.
def update_file_with_new_reservations():
    data = []
    for reserve in reservation_cache:
        data.append(reservation_to_dict(reserve))

    reservation_file = open("reservations.json", "w")
    json.dump(data, reservation_file, indent = 2)

    reservation_file.close()
