# Hotel object: new(integer, string, integer, integer)
#  - stores reservation status
#  - has a list of rooms (list of roomobj objects)
#  - has a list of amenities (list of strings)
#  - other vars:
#    - index (unique - integer)
#    - name (string)
#    - diff (weekend differential - integer)
#    - numRooms (integer)
class Hotel:
    rooms_dict = {}
    amenities_list = []
    def __init__(self, index, name, diff, num_rooms, rooms_dict, amenities_list):
        self.index = index
        self.name = name
        self.num_rooms = num_rooms
        self.diff = diff
        self.rooms_dict = rooms_dict
        self.amenities_list = amenities_list

    #Setters
    def set_index(self, x):
        self.index = x
    def set_name(self, x):
        self.name = x
    def set_num_rooms(self, x):
        self.num_rooms = x
    def set_diff(self, x):
        self.diff = x

    def set_rooms_dict(self, x):
        self.rooms_dict = x
    def set_amenities_lists(self, x):
        self.amenities_list = x

    #Getters
    def get_index(self):
        return self.index
    def get_name(self):
        return self.name
    def get_num_rooms(self):
        return self.num_rooms
    def get_diff(self):
        return self.diff

    def get_rooms_dict(self):
        return self.rooms_dict
    def get_amenities_lists(self):
        return self.amenities_list

    # Turns a hotel object back into a dict for database use.
    def to_dict(self):
        return_dict = {}

        return_dict["index"] = self.get_index()
        return_dict["name"] = self.get_name()
        return_dict["rooms"] = self.get_num_rooms()
        return_dict["weekend_differential"] = self.get_diff()
        return_dict["rooms_dict"] = self.get_rooms_dict()
        return_dict["amenity_list"] = self.get_amenities_lists()

        return return_dict

    # Simple to_string of a hotel object for testing.
    def to_string(self):
        return "Hotel at index " + str(self.get_index()) + ": " + self.get_name()
