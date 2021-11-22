import json

from flask import Flask, render_template, make_response, redirect, flash
from flask_restful import Api, Resource, abort, reqparse
import datetime as dt

import HotelHelpers as hp
import ReservationHelpers as rp
import UserHelpers as up

#make new app in Flask and wrap in RESTful API
app = Flask(__name__)
app.config['SECRET_KEY'] = ";pUf;63iVV5&sI`r4XvZ4vqkW.g~jj"
api = Api(app)

parser = reqparse.RequestParser()

# HotelList Endpoint (/hotels)
# Shows all hotels. Takes in no arguments.
class HotelList(Resource):
    def get(self):
        output = []
        for hotel in hp.hotel_cache:
            output.append(hp.hotel_to_dict(hotel))
        return make_response(render_template('hotels.html', top_text="All Hotels", hotels=output), 200)

# Hotel (/hotels/index/[integer])
# Shows the hotel at the given index in the URL. Takes no arguments.
class Hotel(Resource):
    def get(self, hotel_id):
        output = [hp.hotel_to_dict(hp.find_list_index_of_hotel(hotel_id))]

        if len(output) < 1:
            return "No hotels found at index " + str(hotel_id) + "!"

        hotel_str = "Hotel #" + str(hotel_id) + ":"
        return make_response(render_template('hotels.html', top_text=hotel_str, hotels=output), 200)

# Hotel search (/hotels/search)
# Shows all valid hotels within the various arguments passed.
# Arguments include
# - optional - in date (in_year, in_month, in_day)
# - opitional - out date (out_year, out_month, out_day)
# - required - num_rooms
# - required - room_type
class HotelSearch(Resource):
    def post(self):
        parser.add_argument('in_year', type=int)
        parser.add_argument('in_month', type=int)
        parser.add_argument('in_day', type=int)
        parser.add_argument('out_year', type=int)
        parser.add_argument('out_month', type=int)
        parser.add_argument('out_day', type=int)
        parser.add_argument('num_rooms', type=int)
        parser.add_argument('room_type', type=str)
        args = parser.parse_args()

        in_year = args["in_year"]
        in_month = args["in_month"]
        in_day = args["in_day"]

        out_year = args["out_year"]
        out_month = args["out_month"]
        out_day = args["out_day"]

        # Turn our inputted dates into datetime objects.
        # If they didn't enter a date, or the dates are invalid somehow,
        # then leave the objects as null / none.
        in_date = None
        if in_year and in_month and in_day:
            in_date = dt.date(in_year, in_month, in_day)

        out_date = None
        if out_year and out_month and out_day:
            out_date = dt.date(out_year, out_month, out_day)

        output = []

        for hotel in hp.hotel_cache:
            if args["room_type"] not in hotel.get_rooms_dict():
                continue

            final_room_num = hotel.get_num_rooms()
            # Loop through every reservation we have.
            for reservation in rp.reservation_cache:
                if reservation.get_hotel_index() != hotel.get_index():
                    continue

                # If the current reservation falls outside of the date specified, we don't need to care
                if in_date is not None and out_date is not None:
                    if in_date < reservation.get_in_date() and out_date > reservation.get_out_date():
                        continue

                final_room_num = final_room_num - reservation.get_num_rooms_reserved()

            # If the number of available rooms less than the specified number of rooms, don't show the hotel
            if final_room_num >= args["num_rooms"]:
                output.append(hp.hotel_to_dict(hotel))

        return make_response(render_template('hotels.html', top_text="Searched Hotels:", hotels=output), 200)

    def get(self):
        return make_response(render_template('hotel_search.html'), 200)

# Constants that determine how much to increase or decrease
# the price range of a room if no valid rooms were found.
NO_ROOMS_MIN_PRICE_DECREASE = 25
NO_ROOMS_MAX_PRICE_INCREASE = 25

## TODO ##
# Hotel Filter (/hotels/filter)
# Filters a passed list of hotels further
class HotelFilter(Resource):
    def post(self, price_range_low, price_range_high):
        parser.add_argument('num_rooms', type=int)
        parser.add_argument('room_type', type=str)
        args = parser.parse_args()

        num_rooms = int(args["num_rooms"])
        room_type = int(args["room_type"])

        hotel_list = [] #TODO: This needs to be passed in.
        amenity_list = [] #TODO: Ditto

        # Check with our price range
        returned_hotels = hp.find_certain_hotels(
            hotel_list,
            num_rooms,
            amenity_list,
            room_type,
            price_range_low,
            price_range_high
        )

        # No price range? Try again with a bigger range
        if len(returned_hotels) < 1:
            returned_hotels = hp.find_certain_hotels(
                hotel_list,
                num_rooms,
                amenity_list,
                room_type,
                price_range_low - NO_ROOMS_MIN_PRICE_DECREASE,
                price_range_high + NO_ROOMS_MAX_PRICE_INCREASE
            )

        return returned_hotels if len(returned_hotels) > 0 else "No hotels found!"

    def post(self):
        pass

# Customers (/admin/customers)
# Shows all users, only available to admins.
class Customers(Resource):
    def get(self):
        if not is_logged_in():
            return please_login_alert()

        if not is_admin_logged_in():
            return admin_only_alert()

        output = []
        for user in up.user_cache:
            output.append(up.user_to_dict(user))

        return output

## TODO ##
# Create reservation endpoint
class MakeReservation(Resource):
    def post(self):
        if not is_logged_in():
            return please_login_alert()

        args = parser.parse_args()
        return True
    def get(self):
        return "This is where you make a reservation"

## TODO ##
# View reservation endpoint
class ViewReservation(Resource):
    def post(self):
        if not is_logged_in():
            return please_login_alert()

        args = parser.parse_args()
        return True
    def get(self):
        return "This is where you make a reservation"


## TODO ##
# Cancel reservation endpoint
class CancelReservation(Resource):
    def post(self):
        if not is_logged_in():
            return please_login_alert()

        # Passed a user index and a hotel index.
        if not True:
            return "No reservations found", 404

        #code here to cancel a reservation in the DB

        return "Reservation cancelled", 200
    def get(self):
        if not is_logged_in():
            return please_login_alert()

        return "This is where you cancel reservations", 202

# Login (/login)
# Allows a user or admin to login to their account.
class Login(Resource):
    def post(self):
        if is_logged_in():
            flash("Log out first!") # Obviously don't include this in the end
            return

        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        username = str(args["username"])
        password = str(args["password"])

        if len(username) < 1:
            flash("Please enter a username to continue!")
            return
        if len(password) < 1:
            flash("Please enter a password to continue!")
            return

        if not up.login(username, password):
            flash("Login failed! Uername or password incorrect.")
            return

        return redirect("/hotels")

    def get(self):
        return make_response(render_template('login.html'), 200)

# Wrapper for logging out of a user account.
# use in a resource by invoking it like so:
# `return logout_wrapper()`
def logout_wrapper():
    up.logout()
    return redirect("/login")

# Checks if the current user is an admin.
# Returns TRUE if so, FALSE if there is no current user
# or if the current is not an admin
def is_admin_logged_in():
    return up.check_if_active_user_is_admin()

# Checks if there is a user currently logged in.
# Returns TRUE if there is a user, FALSE otherwise
def is_logged_in():
    return up.active_user_index >= 0

# Wrapper for an alert for when a user is not
# logged in when a page requires a login.
# invoke like so: `return please_login_alert()`
def please_login_alert():
    flash("You are not logged in! Please login to continue.")
    return redirect("/login")

def admin_only_alert():
    abort(401, message = "This page is for admins only!")

# Make account. (/makeaccount)
# Allows a user to make a new account.
class MakeAccount(Resource):
    def post(self):
        if is_logged_in():
            flash("Log out first!") # Obviously don't include this in the end
            return

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
        up.active_user_index = up.user_cache.index(new_user)

        return redirect("/hotels")

    def get(self):
        return make_response(render_template('make_account.html'), 200)

# Home page (/)
# Simple, buttons to either login or make an account
class Home(Resource):
    def post(self):
        parser.add_argument('login', type=bool)
        parser.add_argument('makeaccount', type=bool)
        args = parser.parse_args()

        if args['login']:
            return redirect("/login")
        if args['makeaccount']:
            return redirect("/makeaccount")

        return 404

    def get(self):
        return make_response(render_template('welcome.html'), 200,)

# API Resource Routing here
#
api.add_resource(Home,'/')
api.add_resource(Login,'/login')
api.add_resource(MakeAccount,'/makeaccount')
api.add_resource(HotelList,'/hotels')
api.add_resource(Hotel, '/hotels/index/<int:hotel_id>')
api.add_resource(HotelSearch, '/hotels/search')
api.add_resource(HotelFilter, '/hotels/search/<int:price_range_low>/<int:price_range_high>')
api.add_resource(Customers, '/admin/customers')
api.add_resource(MakeReservation, '/reservations/make')
api.add_resource(ViewReservation, '/reservations/view')
api.add_resource(CancelReservation, '/reservations/cancel')

# Initialize all hotels from the json
def init_hotels(json_data):
    hp.hotels_to_list(json_data)

# Initialize all reservations from the json
def init_reservations(json_data):
    rp.reservations_to_list(json_data)

# Initialize all users from the json
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
