import json

from flask import Flask, render_template, make_response, redirect
from flask_restful import Api, Resource, abort, fields, reqparse

import HotelHelpers as hp
import ReservationHelpers as rp
import UserHelpers as up

#make new app in Flask and wrap in RESTful API
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

# HotelList
# Shows all hotels
class HotelList(Resource):
    def get(self):
        output = []
        for hotel in hp.hotel_cache:
            output.append(hp.hotel_to_dict(hotel))
        return output

# Hotel
# shows a hotel by it's index
class Hotel(Resource):
    def get(self, hotel_id):
        return hp.find_list_index_of_hotel(hotel_id).to_dict()

## TODO ##
#queries hotels within a date range search parameter
class HotelSearch(Resource):
    #takes in 3 parameters, in and out date are dictionaries, num_rooms is an integer
    def get(self, in_date, out_date, num_rooms):
        return True

# Constant that determines how much to increase
# the max price range of a room if
# no valid rooms were found.
NO_ROOMS_MAX_PRICE_INCREASE = 50

## TODO ##
# Input:
# - list of hotels
# - price range (low -> high)
# - list of amenities
# - room type
#
# Output:
# List of hotel dictionaries
# which have a room available
# that matches all user inputs
#
# if no output was found, with given input,
# increases max price range by NO_ROOMS_MAX_PRICE_INCREASE
# then sees if there are any valid rooms again.

class HotelFilter(Resource):
    def get(self, hotel_list, amenity_list, room_type, price_range_low, price_range_high):

        # Get all hotels in the hotel list we were passed and convert them to objects.
        returned_hotels = []
        for hotel in hotel_list:

            # Now we check for amenities.
            # If all amenities in the passed list
            # are found in our hotel's amenity list,
            # then the hotel is valid -
            # otherwise continue the loop to next hotel.
            has_all_amenites = True
            for amenity in amenity_list:
                if amenity not in hotel.amenities_list:
                    has_all_amenites = False

            if not has_all_amenites:
                continue

            # Now we check for rooms.
            # If we found no rooms, we need to re-query with a larger range.
            if len(hotel.get_num_rooms()) < 1:
                return True

            # If we have rooms now, we need to check that our roomtype is in there somewhere.
            if len(hotel.rooms_list) >= 1:
                for room in hotel.rooms_list:
                    if room.type == room_type:
                        returned_hotels.append(hp.hotel_to_dict(hotel))
                        break

            else:
                return None

        return returned_hotels

## TODO ##
# Rooms
# Shows all rooms
class Rooms(Resource):
    def get(self):
        return True

## TODO ##
# RoomIndex
# Shows Rooms by index
class RoomIndex(Resource):
    def get(self, room_id):
        return True

## TODO ##
# RoomMax
# Shows rooms under a max price
class RoomMax(Resource):
    def get(self, max):
        return True

## TODO ##
# RoomRange
# Shows Rooms within a price range
class RoomRange(Resource):
    def get(self, min, max):
        return True

## TODO ##
# Customers
# Shows all customers
class Customers(Resource):
    def get(self):
        return True

## TODO ##
#create reservation endpoint
class MakeReservation(Resource):
    def put(self):
        args = parser.parse_args()
        return True
    def get(self):
        return "This is where you make a reservation"

## TODO ##
#view reservation endpoint
class ViewReservation(Resource):
    def put(self):
        args = parser.parse_args()
        return True
    def get(self):
        return "This is where you make a reservation"


## TODO ##
#cancel reservation endpoint
class CancelReservation(Resource):
    def put(self):
        # Passed a user index and a hotel index.
        if not True:
            return "No reservations found", 404

        #code here to cancel a reservation in the DB

        return "Reservation cancelled", 200
    def get(self):
        return "This is where you cancel reservations", 202

# Login node.
class Login(Resource):
    def post(self):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        username = str(args["username"])
        password = str(args["password"])

        if len(username) < 1:
            return "No username inputted!"
        if len(password) < 1:
            return "No password inputted!"

        for user in up.user_cache:
            if user.get_username() != username:
                continue

            #check if the password matches
            if user.get_password() != password:
                return "Incorrect password!"
            up.active_user = user

        if not up.active_user:
            return "Username not found."

        return redirect("hotels")

    def get(self):
        return make_response(render_template('login.html'), 200)

# Make Account node.
class MakeAccount(Resource):
    def post(self):
        parser.add_argument('fname', type=str)
        parser.add_argument('lname', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone_num', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        f_name = str(args["fname"])
        l_name = str(args["lname"])
        email = str(args["email"])
        phone_num = str(args["phone_num"])
        username = str(args["username"])
        password = str(args["password"])

        if len(f_name) < 1:
            return "No first name inputted!"
        if len(l_name) < 1:
            return "No last name inputted!"
        if len(email) < 1:
            return "No email inputted!"
        if len(phone_num) < 1:
            return "No phone number inputted!"
        if len(username) < 1:
            return "No username inputted!"
        if len(password) < 1:
            return "No password inputted!"

        for user in up.user_cache:
            if user.get_username() == username:
                return "Username already exists!"

        new_user = up.make_user(
            username,
            password,
            f_name,
            l_name,
            email,
            phone_num,
            0
        )

        up.user_cache.append(new_user)
        up.update_file_with_new_user()
        up.active_user = new_user

        return redirect("hotels")

    def get(self):
        return make_response(render_template('make_account.html'), 200)

# Home page
class Home(Resource):
    def post(self):
        parser.add_argument('login', type=bool)
        parser.add_argument('makeaccount', type=bool)
        args = parser.parse_args()

        if args['login']:
            return redirect("login")
        if args['makeaccount']:
            return redirect("makeaccount")

        return 404

    def get(self):
        return make_response(render_template('welcome.html'), 200)

##
##API Resource Routing here
##
api.add_resource(Home,'/')
api.add_resource(Login,'/login')
api.add_resource(MakeAccount,'/makeaccount')
api.add_resource(HotelList,'/hotels')
api.add_resource(Hotel, '/hotels/index/<int:hotel_id>')
api.add_resource(HotelSearch, '/hotels/search/<in_date>/<out_date>/<int:num_rooms>')
api.add_resource(HotelFilter, '/hotels/search/filter/<room_type>/<int:price_range_low>/<int:price_range_high>')
#api.add_resource(Rooms, "/rooms")
#api.add_resource(RoomIndex, '/rooms/index/<int:room_id>')
#api.add_resource(RoomMax, '/rooms/list/<int:max>')
#api.add_resource(RoomRange, '/rooms/list/<int:max>/<int:min>')
api.add_resource(Customers, '/admin/customers')
api.add_resource(MakeReservation, '/reservations/make')
api.add_resource(ViewReservation, '/reservations/view')
api.add_resource(CancelReservation, '/reservations/cancel')

def init_hotels(json_data):
    hp.hotels_to_list(json_data)

def init_reservations(json_data):
    rp.reservations_to_list(json_data)

def init_users(json_data):
    up.users_to_list(json_data)

if __name__ == "__main__":
    hotel_file = open("hotels.json", "r")
    init_hotels(json.load(hotel_file))

    reservation_file = open("reservations.json", "r")
    init_reservations(json.load(reservation_file))

    user_file = open("users.json", "r")
    init_users(json.load(user_file))

    app.run(debug = True) #Chnage this when testing is done

    hotel_file.close()
    reservation_file.close()
    user_file.close()
