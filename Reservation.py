class Reservation:
    def __init__(self, user_index, hotel_index, num_rooms_reserved, room_type_reserved, in_date, out_date):
        self.user_index = user_index
        self.hotel_index = hotel_index
        self.num_rooms_reserved = num_rooms_reserved
        self.room_type_reserved = room_type_reserved
        self.in_date = in_date
        self.out_date = out_date

    # Turns a hotel object back into a dict for database use.
    def to_dict(self):
        return_dict = {}

        return_dict["user_index"] = "Test return"

        return return_dict
