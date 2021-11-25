import json

from flask import Flask, render_template, make_response, redirect, flash
from flask_restful import Api, Resource, abort, reqparse
import datetime as dt

import HotelHelpers as hp
import ReservationHelpers as rp
import UserHelpers as up

# make new app in Flask and wrap in RESTful API
app = Flask(__name__)
app.config['SECRET_KEY'] = ";pUf;63iVV5&sI`r4XvZ4vqkW.g~jj"

api = Api(app)

parser = reqparse.RequestParser()

# HotelList Endpoint (/hotels)
# Shows all hotels. Takes in no arguments.
class HotelList(Resource):
    def post(self):
        if logout_post():
            return logout_wrapper()

        if home_post():
            return home_wrapper()

        return self.get()

    def get(self):
        output = []
        for hotel in hp.hotel_cache:
            output.append(hp.hotel_to_dict(hotel))
        return make_response(render_template('hotels.html', top_text="All Hotels", hotels=output), 200)

# Hotel (/hotels/[integer])
# Shows the hotel at the given index in the URL. Takes no arguments.
class Hotel(Resource):
    def get(self, hotel_id):
        output = [hp.hotel_to_dict(hp.find_hotel_by_index(hotel_id))]

        if len(output) < 1:
            return "No hotels found at index " + str(hotel_id) + "!"

        hotel_str = "Hotel #" + str(hotel_id) + ":"
        return make_response(render_template('hotels.html', top_text=hotel_str, hotels=output), 200)


# Constants that determine how much to increase or decrease
# the price range of a room if no valid rooms were found.
NO_ROOMS_MIN_PRICE_DECREASE = 25
NO_ROOMS_MAX_PRICE_INCREASE = 25

# Hotel search (/hotels/search)
# Shows all valid hotels within the various arguments passed.
# Arguments include
# - optional - in date (in_year, in_month, in_day)
# - opitional - out date (out_year, out_month, out_day)
# - required - num_rooms
# - required - room_type
class HotelSearch(Resource):
    def post(self):
        if logout_post():
            return logout_wrapper()

        if home_post():
            return home_wrapper()

        #Ints
        parser.add_argument('num_rooms')
        parser.add_argument('price_range_min')
        parser.add_argument('price_range_max')

        #Bools (Amenities)
        parser.add_argument('amen_pool', type=bool)
        parser.add_argument('amen_gym', type=bool)
        parser.add_argument('amen_spa', type=bool)
        parser.add_argument('amen_office', type=bool)

        #Strings
        parser.add_argument('room_type', type=str)
        parser.add_argument('in_date', type=str)
        parser.add_argument('out_date', type=str)

        args = parser.parse_args()

        # In and our years are passed as strings: YYYY-MM-DD
        in_year_list = args["in_date"].split("-")
        out_year_list = args["out_date"].split("-")

        # If we were passed a malformed or empty or null string,
        # catch that error and set it to a default date
        try:
            in_date = dt.date(in_year_list[0], in_year_list[1], in_year_list[2])
        except (IndexError, ValueError):
            in_date = dt.date(1, 1, 1)

        try:
            out_date = dt.date(out_year_list[0], out_year_list[1], out_year_list[2])
        except (IndexError, ValueError):
            out_date = dt.date(9999, 12, 31)

        # Passed as integers, but can be an empty string if the box is empty
        num_rooms = cast_to_int_or_default(args["num_rooms"], 1)
        price_range_min = cast_to_int_or_default(args["price_range_min"], 0)
        price_range_max = cast_to_int_or_default(args["price_range_max"], 10000)

        # Passed as a string, validate it is a room type
        room_type = args["room_type"]
        if room_type not in ["Standard", "Queen", "King"]:
            room_type = "Standard"

        # Passed as multiple bools, we will give it to our search function as a dictionary
        req_amenities = {
            "Pool": args["amen_pool"],
            "Gym": args["amen_gym"],
            "Spa": args["amen_spa"],
            "Business Office": args["amen_office"]
        }

        # Our first shot at searching
        ret_text = "Found Hotels:"
        output = hp.find_certain_hotels(
            room_type,
            num_rooms,
            req_amenities,
            in_date,
            out_date,
            price_range_min,
            price_range_max
            )

        # Did our first shot return no results?
        # Search agin with a wider price range
        if len(output) < 1:
            ret_text = "No hotels found - Found hotels in wider price range:"
            output = hp.find_certain_hotels(
                room_type,
                num_rooms,
                req_amenities,
                in_date,
                out_date,
                price_range_min - NO_ROOMS_MIN_PRICE_DECREASE,
                price_range_max + NO_ROOMS_MAX_PRICE_INCREASE
                )

        # Did our wider prince range return no results?
        # Then it's up to the user, now
        if len(output) < 1:
            ret_text = "No hotels found!"

        return make_response(render_template('hotels.html', top_text=ret_text, hotels=output), 200)

    def get(self):
        return make_response(render_template('hotel_search.html'), 200)

# Passed empty text fields are only populated with the null character ('')
# So run everything though this function to default it to a certain int if it is empty (or cast if it's not)
def cast_to_int_or_default(value: str, default: int) -> int:
    if str is None:
        return default

    try:
        return int(value)
    except (ValueError, TypeError):
        return default


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

# View reservation endpoint
class ViewReservation(Resource):
    # Cancel reservations.
    def post(self):
        if logout_post():
            return logout_wrapper()

        if home_post():
            return home_wrapper()

        parser.add_argument('cancel', type=bool)
        args = parser.parse_args()

        if args["cancel"]:
            removed_reservation = rp.find_reservation_by_index(0) # TODO: Hardcoded 1st
            if removed_reservation is not None:
                rp.reservation_cache.remove(removed_reservation)
                rp.update_file_with_new_reservations()

        return self.get()

    # View reservations.
    def get(self):
        if not is_logged_in():
            return please_login_alert()

        is_admin = is_admin_logged_in()

        output = []
        for reservation in rp.reservation_cache:
            # Admins will see all reservations that are made
            if not is_admin:
                if reservation.get_user_index() != up.active_user_index:
                    continue

            reserved_hotel = hp.find_hotel_by_index(reservation.get_hotel_index())

            reservation_info = rp.reservation_to_dict(reservation)
            reservation_info["in_date_string"] = reservation.get_in_date_string()
            reservation_info["out_date_string"] = reservation.get_out_date_string()
            reservation_info["hotel_info"] = hp.hotel_to_dict(reserved_hotel)
            output.append(reservation_info)

        return make_response(render_template('reservations.html', reservations=output, admin=is_admin), 200)

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

        return redirect("/home")

    def get(self):
        return make_response(render_template('login.html'), 200)

def logout_post() -> bool:
    parser.add_argument('logout', type=bool)
    args = parser.parse_args()

    if args["logout"]:
        return True

    return False

# Wrapper for logging out of a user account.
# use in a resource by invoking it like so:
# `return logout_wrapper()`
def logout_wrapper():
    up.logout()
    return redirect("/login")

def home_post() -> bool:
    parser.add_argument('home', type=bool)
    args = parser.parse_args()

    if args["home"]:
        return True

    return False

def home_wrapper():
    return redirect("/home")

# Checks if the current user is an admin.
# Returns TRUE if so, FALSE if there is no current user
# or if the current is not an admin
def is_admin_logged_in() -> bool:
    return up.check_if_active_user_is_admin()

# Checks if there is a user currently logged in.
# Returns TRUE if there is a user, FALSE otherwise
def is_logged_in() -> bool:
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

        parser.add_argument('fname', type=str, trim = True)
        parser.add_argument('lname', type=str, trim = True)
        parser.add_argument('email', type=str, trim = True)
        parser.add_argument('phone_num', type=str, trim = True)
        parser.add_argument('username', type=str, trim = True)
        parser.add_argument('password', type=str, trim = True)
        args = parser.parse_args()

        f_name = args["fname"]
        l_name = args["lname"]
        email = args["email"]
        phone_num = args["phone_num"]
        username = args["username"]
        password = args["password"]

        if f_name is None:
            return "No first name inputted!"
        if l_name is None:
            return "No last name inputted!"
        if email is None:
            return "No email inputted!"
        if phone_num is None:
            return "No phone number inputted!"
        if username is None:
            return "No username inputted!"
        if password is None:
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

        return redirect("/home")

    def get(self):
        if is_logged_in():
            redirect("/home")

        return make_response(render_template('make_account.html'), 200)

# Home page (/)
# Simple, buttons to either login or make an account
class Welcome(Resource):
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

class Home(Resource):
    def post(self):
        if not is_logged_in():
            return please_login_alert()

        parser.add_argument('viewhotels', type=bool)
        parser.add_argument('searchhotels', type=bool)
        parser.add_argument('viewreservations', type=bool)
        parser.add_argument('customers', type=bool)
        args = parser.parse_args()

        if args['viewhotels']:
            return redirect("/hotels")
        if args['searchhotels']:
            return redirect("/hotels/search")
        if args['viewreservations']:
            return redirect("/reservations")

        if args['customers']:
            if not is_admin_logged_in():
                return admin_only_alert()

            return redirect("/admin/customers")

        return 404

    def get(self):
        if not is_logged_in():
            return please_login_alert()

        curr_user = up.user_to_dict(up.find_user_by_index(up.active_user_index))
        return make_response(render_template('home.html', user=curr_user), 200)

# API Resource Routing here
#
api.add_resource(Welcome,'/')
api.add_resource(Home,'/home')
api.add_resource(Login,'/login')
api.add_resource(MakeAccount,'/makeaccount')
api.add_resource(HotelList,'/hotels')
api.add_resource(Hotel, '/hotels/<int:hotel_id>')
api.add_resource(HotelSearch, '/hotels/search')
api.add_resource(MakeReservation, '/hotels/<int:hotel_id>/reserve')
api.add_resource(ViewReservation, '/reservations')
api.add_resource(Customers, '/admin/customers')

# Initialize all hotels from the json
def init_hotels(json_data: list):
    hp.hotels_to_list(json_data)

# Initialize all reservations from the json
def init_reservations(json_data: list):
    rp.reservations_to_list(json_data)

# Initialize all users from the json
def init_users(json_data: list):
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
