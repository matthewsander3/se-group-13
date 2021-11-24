import datetime as dt

class Reservation:
    def __init__(self, index, user_index, hotel_index, num_rooms_reserved, room_type_reserved, in_date, out_date):
        self.index = index
        self.user_index = user_index
        self.hotel_index = hotel_index
        self.num_rooms_reserved = num_rooms_reserved
        self.room_type_reserved = room_type_reserved
        self.in_date = in_date
        self.out_date = out_date

    def get_index(self):
        return self.index
    def get_user_index(self):
        return self.user_index
    def get_hotel_index(self):
        return self.hotel_index
    def get_num_rooms_reserved(self):
        return self.num_rooms_reserved
    def get_room_type_reserved(self):
        return self.room_type_reserved

    def get_in_date(self): #Returns a datetime object
        return self.in_date
    def get_out_date(self): #Returns a datetime object
        return self.out_date

    def get_in_date_dict(self): #Returns a dict
        in_date_dict = {}
        in_date_dict["year"] = self.in_date.year
        in_date_dict["month"] = self.in_date.month
        in_date_dict["day"] = self.in_date.day
        return in_date_dict

    def get_out_date_dict(self): #Returns a dict
        out_date_dict = {}
        out_date_dict["year"] = self.out_date.year
        out_date_dict["month"] = self.out_date.month
        out_date_dict["day"] = self.out_date.day
        return out_date_dict

    def get_in_date_string(self): #Returns a string
        in_date_string = str(self.in_date.year) + "/" + str(self.in_date.month) + "/" + str(self.in_date.day)
        return in_date_string

    def get_out_date_string(self): #Returns a string
        out_date_string = str(self.out_date.year) + "/" + str(self.out_date.month) + "/" + str(self.out_date.day)
        return out_date_string

    # Turns a hotel object back into a dict for database use.
    def to_dict(self):
        return_dict = {}

        return_dict["index"] = self.get_index()
        return_dict["user_index"] = self.get_user_index()
        return_dict["hotel_index"] = self.get_hotel_index()
        return_dict["num_rooms_reserved"] = self.get_num_rooms_reserved()
        return_dict["room_type_reserved"] = self.get_room_type_reserved()
        return_dict["in_date"] = self.get_in_date_dict()
        return_dict["out_date"] = self.get_out_date_dict()

        return return_dict

    # Checks if the in or out date of the reservation is on a weekend
    # 0-5 = weekday, 6-7 = weekend, for datetime
    def is_on_weekend(self):
        return self.get_in_date().weekday() >= 5 or self.get_out_date.weekday() >= 5
