import Reservation

reservation_cache = []

def dict_to_reservation(reserve_dict):

	user_index = reserve_dict["user_index"] #Integer
	hotel_index = reserve_dict["hotel_index"] #Integer
	num_rooms_reserved = reserve_dict["num_rooms_reserved"] #Integer
	room_type_reserved = reserve_dict["room_type_reserved"] #String
	in_date = reserve_dict["in_date"] #Dict
	out_date = reserve_dict["out_date"] #Dict

	return Reservation.Reservation(
		user_index,
		hotel_index,
		num_rooms_reserved,
		room_type_reserved,
		in_date,
		out_date
		)

def reservation_to_dict(reservation):
	return reservation.to_dict()

def reservations_to_list(reservation_list):
	for reservation in reservation_list:
		reservation_cache.append(dict_to_reservation(reservation))

def find_reservations_by_hotel_index(index):
	output = []
	for reservation in reservation_cache:
		if reservation.hotel_index == index:
			output.append(reservation.to_dict())

	return output

def find_reservations_by_user_index(index):
	output = []
	for reservation in reservation_cache:
		if reservation.user_index == index:
			output.append(reservation.to_dict())

	return output
