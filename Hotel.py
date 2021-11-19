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
    rooms_dict = []
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
    def set_numRooms(self, x):
        self.num_rooms = x

    #Getters
    def get_index(self):
        return self.index
    def get_name(self):
        return self.name
    def get_num_rooms(self):
        return self.numRooms
    def get_diff(self):
        return self.diff
    def get_numRooms(self):
        return self.numRooms

    # Removes a certain room object from the rooms list.
    def remove_room(self, room):
        self.rooms_list.remove(room)
    # Removes a certain amenity from the amenities list.
    def remove_amenity(self, amenity):
        self.amenities_list.remove(amenity)

    # Turns a hotel object back into a dict for database use.
    def to_dict(self):
        return_dict = {}

        return_dict["index"] = self.get_index()
        return_dict["name"] = self.get_name()
        return_dict["rooms"] = self.get_num_rooms()
        return_dict["weekend_differential"] = self.get_diff()

        return return_dict

    # Simple to_string of a hotel object for testing.
    def to_string(self):
        return "Hotel at index " + str(self.get_index()) + ": " + self.get_name()
