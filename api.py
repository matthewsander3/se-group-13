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

valid_roomtypes = ["Standard", "Queen", "King"]

# HotelList Endpoint (/hotels)
# Shows all hotels. Takes in no arguments.
class HotelList(Resource):
    def post(self):
        if logout_post():
            return logout_wrapper()
        if login_post():
            return login_wrapper()
        if home_post():
            return home_wrapper()

        reserved_hotel = reserve_post()
        if reserved_hotel >= 0:
           return redirect("/hotels/" + str(reserved_hotel) + "/reserve")

        edited_hotel = edit_hotel_post()
        if is_admin_logged_in() and edited_hotel >= 0:
           return redirect("/hotels/" + str(edited_hotel) + "/edit")

        return self.get()

    def get(self):
        output = []
        for hotel in hp.hotel_cache:
            output.append(hp.hotel_to_dict(hotel))
        curr_user = up.get_active_user_dict()
        return make_response(render_template('hotels.html', user=curr_user, top_text="All Hotels", hotels=output), 200)

# Hotel (/hotels/[integer])
# Shows the hotel at the given index in the URL. Takes no arguments.
class Hotel(Resource):
    def post(self, hotel_id):
        if logout_post():
            return logout_wrapper()
        if login_post():
            return login_wrapper()
        if home_post():
            return home_wrapper()

        reserved_hotel = reserve_post()
        if reserved_hotel >= 0:
           return redirect("/hotels/" + hotel_id + "/reserve")

        edited_hotel = edit_hotel_post()
        if is_admin_logged_in() and edited_hotel >= 0:
           return redirect("/hotels/" + hotel_id + "/edit")

        return abort(404)

    def get(self, hotel_id):
        output = [hp.hotel_to_dict(hp.find_hotel_by_index(hotel_id))]

        if len(output) < 1:
            flash("No hotels found at index " + str(hotel_id) + "!")
            return redirect("/hotels")

        hotel_str = "Hotel #" + str(hotel_id) + ":"
        curr_user = up.get_active_user_dict()
        return make_response(render_template('hotels.html', user=curr_user, top_text=hotel_str, hotels=output), 200)


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
        if login_post():
            return login_wrapper()
        if home_post():
            return home_wrapper()

        reserved_hotel = reserve_post()
        if reserved_hotel >= 0:
           return redirect("/hotels/" + str(reserved_hotel) + "/reserve")

        edited_hotel = edit_hotel_post()
        if is_admin_logged_in() and edited_hotel >= 0:
           return redirect("/hotels/" + str(edited_hotel) + "/edit")

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

        # In and out dates are passed as strings: YYYY-MM-DD
        in_year_list = args["in_date"].split("-")
        out_year_list = args["out_date"].split("-")

        # If we were passed a malformed or empty or null string,
        # catch that error and set it to a default date
        try:
            in_date = dt.date(int(in_year_list[0]), int(in_year_list[1]), int(in_year_list[2]))
        except (IndexError, ValueError):
            in_date = dt.date(1, 1, 1)

        try:
            out_date = dt.date(int(out_year_list[0]), int(out_year_list[1]), int(out_year_list[2]))
        except (IndexError, ValueError):
            out_date = dt.date(9999, 12, 31)

        # Passed as integers, but can be an empty string if the box is empty
        num_rooms = cast_to_int_or_default(args["num_rooms"], 1)
        price_range_min = cast_to_int_or_default(args["price_range_min"], 0)
        price_range_max = cast_to_int_or_default(args["price_range_max"], 10000)

        # Passed as a string, validate it is a room type
        room_type = args["room_type"]
        if room_type not in valid_roomtypes:
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

        curr_user = up.get_active_user_dict()
        return make_response(render_template('hotels.html', user=curr_user, top_text=ret_text, hotels=output), 200)

    def get(self):
        curr_user = up.get_active_user_dict()
        return make_response(render_template('hotel_search.html', user=curr_user), 200)

# Create reservation endpoint
class EditHotel(Resource):
    def post(self, hotel_id):
        if not is_logged_in():
            return please_login_alert()
        if not is_admin_logged_in():
            return admin_only_alert()

        if logout_post():
            return logout_wrapper()
        if home_post():
            return home_wrapper()

        parser.add_argument('new_name')
        parser.add_argument('new_num_rooms')
        parser.add_argument('new_weekend_diff')

        parser.add_argument('gym_status', type=bool)
        parser.add_argument('spa_status', type=bool)
        parser.add_argument('office_status', type=bool)
        parser.add_argument('pool_status', type=bool)

        parser.add_argument('standard_cost')
        parser.add_argument('queen_cost')
        parser.add_argument('king_cost')

        args = parser.parse_args()

        old_version = hp.find_hotel_by_index(hotel_id)

        name = args["new_name"]
        num_rooms = cast_to_int_or_default(args["new_num_rooms"], old_version.get_num_rooms())
        diff = cast_to_int_or_default(args["new_weekend_diff"], old_version.get_diff())

        rooms_dict = {}
        s_cost = cast_to_int_or_default(args["standard_cost"], -1)
        if s_cost >= 0:
            rooms_dict["Standard"] = s_cost

        q_cost = cast_to_int_or_default(args["queen_cost"], -1)
        if q_cost >= 0:
            rooms_dict["Queen"] = q_cost

        k_cost = cast_to_int_or_default(args["king_cost"], -1)
        if k_cost >= 0:
            rooms_dict["King"] = k_cost

        amenities_list = []
        if args["gym_status"]:
            amenities_list.append("Gym")
        if args["spa_status"]:
            amenities_list.append("Spa")
        if args["pool_status"]:
            amenities_list.append("Pool")
        if args["office_status"]:
            amenities_list.append("Business Office")

        old_version.set_name(name)
        old_version.set_num_rooms(num_rooms)
        old_version.set_diff(diff)
        old_version.set_rooms_dict(rooms_dict)
        old_version.set_amenities_lists(amenities_list)
        hp.update_file_with_new_hotel()

        return redirect("/hotels/"+ str(hotel_id))

    def get(self, hotel_id):
        output = hp.hotel_to_dict(hp.find_hotel_by_index(hotel_id))

        if not output:
            flash("No hotels found at index " + str(hotel_id) + "!")
            return redirect("/hotels")

        curr_user = up.get_active_user_dict()
        return make_response(render_template('edit_hotel.html', user=curr_user, hotel=output), 200)


# Passed empty text fields are only populated with the null character ('')
# So run everything though this function to default it to a certain int if it is empty (or cast if it's not)
def cast_to_int_or_default(value: str, default: int) -> int:
    if value is None:
        return default

    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# Customers (/customers/admin)
# Shows all users, only available to admins.
class Customers(Resource):
    def post(self):
        if not is_logged_in():
            return please_login_alert()
        if not is_admin_logged_in():
            return admin_only_alert()
        if logout_post():
            return logout_wrapper()
        if home_post():
            return home_wrapper()

        for user in up.user_cache:
            parser.add_argument(str(user.get_index())+"-delete", type=bool)
        args = parser.parse_args()

        for key in args:
            if "delete" not in key:
                continue

            if args[key]:
                argument_split = key.split("-")
                remove_user = up.find_user_by_index(int(argument_split[0]))
                up.user_cache.remove(remove_user)
                up.update_file_with_new_user()
                flash("Deleted " + remove_user.get_username() + "\'s account.")

        return self.get()

    def get(self):
        if not is_logged_in():
            return please_login_alert()

        if not is_admin_logged_in():
            return admin_only_alert()

        output = []
        for user in up.user_cache:
            output.append(up.user_to_dict(user))

        curr_user = up.get_active_user_dict()
        return make_response(render_template('customers.html', user=curr_user, customers=output), 200)

class EditCustomer(Resource):
    def post(self, user_id):

        if not is_logged_in():
            return please_login_alert()

        curr_user = up.find_user_by_index(user_id)
        if not curr_user:
            flash("User not found!")
            return redirect("/home")

        if up.active_user_index != user_id and not is_admin_logged_in():
            return admin_only_alert()

        if logout_post():
            return logout_wrapper()
        if home_post():
            return home_wrapper()

        parser.add_argument('username', type=str, trim = True)
        parser.add_argument('fname', type=str, trim = True)
        parser.add_argument('lname', type=str, trim = True)
        parser.add_argument('password', type=str, trim = True)
        parser.add_argument('email', type=str, trim = True)
        parser.add_argument('phone_num', type=str, trim = True)
        args = parser.parse_args()

        if len(args["username"]) >= 2:
            curr_user.set_username(args["username"])
        if len(args["fname"]) >= 2:
            curr_user.set_f_name(args["fname"])
        if len(args["lname"]) >= 2:
            curr_user.set_l_name(args["lname"])
        if len(args["password"]) >= 2:
            curr_user.set_password(args["password"])
        if len(args["email"]) >= 2:
            curr_user.set_email(args["email"])
        if len(args["phone_num"]) >= 2:
            curr_user.set_phone_num(args["phone_num"])

        up.update_file_with_new_user()

        return redirect("/home")

    def get(self, user_id):
        if not is_logged_in():
            return please_login_alert()

        if up.active_user_index != user_id and not is_admin_logged_in():
            return admin_only_alert()

        curr_user = up.get_active_user_dict()
        output = up.user_to_dict(up.find_user_by_index(user_id))
        return make_response(render_template('edit_customer.html', user=curr_user, customer=output), 200)


# Create reservation endpoint
class MakeReservation(Resource):
    def post(self, hotel_id):
        if not is_logged_in():
            return please_login_alert()

        parser.add_argument('sdate', type=str)
        parser.add_argument('edate', type=str)
        parser.add_argument('roomType', type=str)
        parser.add_argument('numRooms')
        args = parser.parse_args()

        # In and out dates are passed as strings: YYYY-MM-DD
        in_year_list = args["sdate"].split("-")
        out_year_list = args["edate"].split("-")

        in_date = None
        out_date = None

        # If we were passed a malformed or empty or null string,
        # catch that error and set it to a default date
        try:
            in_date = dt.date(int(in_year_list[0]), int(in_year_list[1]), int(in_year_list[2]))
        except (IndexError, ValueError):
            flash("Invalid or incorrect start date, please retry.")
            return redirect("/hotels/"+ str(hotel_id) + "/reserve")

        try:
            out_date = dt.date(int(out_year_list[0]), int(out_year_list[1]), int(out_year_list[2]))
        except (IndexError, ValueError):
            flash("Invalid or incorrect end date, please retry.")
            return redirect("/hotels/"+ str(hotel_id) + "/reserve")

        if in_date < dt.date.today() or out_date < dt.date.today():
            flash("You can't make a reservation in the past.")
            return redirect("/hotels/"+ str(hotel_id) + "/reserve")

        if out_date < in_date:
            flash("You cannot reserve for an out date prior to the in date.")
            return redirect("/hotels/"+ str(hotel_id) + "/reserve")

        room_type = args["roomType"]
        if room_type not in valid_roomtypes:
            flash("Invalid room type, please retry.")
            return redirect("/hotels/"+ str(hotel_id) + "/reserve")

        num_rooms = cast_to_int_or_default(args["numRooms"], 1)

        # Now we calculate our price
        hotel = hp.find_hotel_by_index(hotel_id)
        hotel_prices = hotel.get_rooms_dict()
        if room_type not in hotel_prices:
            flash("That room type is not valid for that hotel.")
            return redirect("/hotels/"+ str(hotel_id) + "/reserve")

        # We get the price for our room type...
        price = hotel_prices[room_type]

        is_weekend_reservation = False
        # If we start or end on a weekend...
        if rp.is_on_weekend(in_date) or rp.is_on_weekend(out_date):
            is_weekend_reservation = True

        # If the time between the in date and the outdate puts us on or past a weekend...
        if (in_date - out_date).days + in_date.weekday() >= 5:
            is_weekend_reservation = True

        # ...Add in the weekend differential to the price
        if is_weekend_reservation:
            price = price + hotel.get_diff()

        price = price * num_rooms

        new_reservation = rp.make_reservation(
            up.active_user_index,
            hotel_id,
            num_rooms,
            room_type,
            price,
            in_date,
            out_date,
        )

        rp.reservation_cache.append(new_reservation)
        print("Success")
        return redirect("/hotels/"+ str(hotel_id) + "/reserve/confirm_" + str(new_reservation.get_index()))

    def get(self, hotel_id):
        if not is_logged_in():
            return please_login_alert()

        hotel = hp.find_hotel_by_index(hotel_id)
        if not hotel:
            return abort(404)
        hotel_info = hp.hotel_to_dict(hotel)
        curr_user = up.get_active_user_dict()
        return make_response(render_template('make_reservation.html', user=curr_user, hotel=hotel_info), 200)

class ConfirmReservation(Resource):
    def post(self, hotel_id, reservation_id):
        parser.add_argument('confirm_reservation', type=bool)
        parser.add_argument('edit_reservation', type=bool)
        args = parser.parse_args()

        to_confirm = rp.find_reservation_by_index(reservation_id)

        if args["edit_reservation"]:
            rp.reservation_cache.remove(to_confirm)
            return redirect("/hotels/" + str(hotel_id) + "/reserve")

        if args["confirm_reservation"]:
            rp.update_file_with_new_reservations()
            flash("Reservation successful!")
            return redirect("/home")

        return abort(404)

    def get(self, hotel_id, reservation_id):
        if not is_logged_in():
            return please_login_alert()

        to_confirm = rp.find_reservation_by_index(reservation_id)
        reserved_hotel = hp.find_hotel_by_index(hotel_id)

        reservation_info = rp.reservation_to_dict(to_confirm)
        reservation_info["in_date_string"] = to_confirm.get_in_date_string()
        reservation_info["out_date_string"] = to_confirm.get_out_date_string()
        reservation_info["hotel_info"] = hp.hotel_to_dict(reserved_hotel)
        reservation_info["is_past"] = (to_confirm.get_in_date() <= dt.date.today())

        curr_user = up.get_active_user_dict()
        return make_response(render_template('res_confirm.html', user=curr_user, res=reservation_info), 200)

# View reservation endpoint
class ViewReservation(Resource):
    # Cancel reservations.
    def post(self):
        if logout_post():
            return logout_wrapper()
        if login_post():
            return login_wrapper()
        if home_post():
            return home_wrapper()

        for reservation in rp.reservation_cache:
            parser.add_argument(str(reservation.get_index())+"-cancel", type=bool)
        args = parser.parse_args()

        for key in args:
            if "cancel" not in key:
                continue

            if args[key]:
                argument_split = key.split("-")
                removed_reservation = rp.find_reservation_by_index(int(argument_split[0]))
                if removed_reservation is not None:
                    rp.reservation_cache.remove(removed_reservation)
                    rp.update_file_with_new_reservations()

        return self.get()

    # View reservations.
    def get(self):
        if not is_logged_in():
            return please_login_alert()

        curr_user = up.get_active_user_dict()

        output = []
        for reservation in rp.reservation_cache:
            # Admins will see all reservations that are made
            if not curr_user["admin_status"]:
                if reservation.get_user_index() != up.active_user_index:
                    continue

            reserved_hotel = hp.find_hotel_by_index(reservation.get_hotel_index())

            reservation_info = rp.reservation_to_dict(reservation)
            reservation_info["in_date_string"] = reservation.get_in_date_string()
            reservation_info["out_date_string"] = reservation.get_out_date_string()
            reservation_info["hotel_info"] = hp.hotel_to_dict(reserved_hotel)
            reservation_info["is_past"] = (reservation.get_in_date() <= dt.date.today())
            output.append(reservation_info)

        return make_response(render_template('reservations.html', user=curr_user, reservations=output), 200)

# Login (/login)
# Allows a user or admin to login to their account.
class Login(Resource):
    def post(self):
        if is_logged_in():
            return redirect("/home")

        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        username = args["username"]
        password = args["password"]

        try:
            if len(username) < 1:
                flash("Please enter a username to continue!")
                return redirect("/login")
            if len(password) < 1:
                flash("Please enter a password to continue!")
                return redirect("/login")
        except (ValueError, TypeError):
            flash("An error occured. Please try again.")
            return redirect("/login")

        if not up.login(username, password):
            flash("Login failed! Uername or password incorrect.")
            return redirect("/login")

        return redirect("/home")

    def get(self):
        if is_logged_in():
            return redirect("/home")

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

def login_post() -> bool:
    parser.add_argument('login', type=bool)
    args = parser.parse_args()

    if args["login"]:
        return True

    return False

def login_wrapper():
    return redirect("/login")

# Checks for make reservation posts.
# If a reservation post is found, return which hotel it was directed to.
# Otherwise return -1 if none found.
def reserve_post():
    for hotel in hp.hotel_cache:
        parser.add_argument(str(hotel.get_index())+"-reserve", type=bool)
    args = parser.parse_args()

    for key in args:
        if "reserve" not in key:
            continue

        if args[key]:
            argument_split = key.split("-")
            return int(argument_split[0])

    return -1

def edit_hotel_post():
    for hotel in hp.hotel_cache:
        parser.add_argument(str(hotel.get_index())+"-edit", type=bool)
    args = parser.parse_args()

    for key in args:
        if "edit" not in key:
            continue

        if args[key]:
            argument_split = key.split("-")
            return int(argument_split[0])

    return -1


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
    return abort(401, message = "This page is for admins only!")

# Make account. (/makeaccount)
# Allows a user to make a new account.
class MakeAccount(Resource):
    def post(self):
        if is_logged_in():
            flash("You are already logged in.") # Obviously don't include this in the end
            return redirect("/home")

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

        try:
            if len(f_name) < 2:
                flash("No first name inputted!")
                return redirect("/makeaccount")
            if len(l_name) < 2:
                flash("No last name inputted!")
                return redirect("/makeaccount")
            if len(email) < 2:
                flash("No email inputted!")
                return redirect("/makeaccount")
            if len(phone_num) < 2:
                flash("No phone number inputted!")
                return redirect("/makeaccount")
            if len(username) < 2:
                flash("No username inputted!")
                return redirect("/makeaccount")
            if len(password) < 2:
                flash("No password inputted!")
                return redirect("/makeaccount")
        except (ValueError, TypeError):
            flash("An error occured. Please try again.")
            return redirect("/makeaccount")

        for user in up.user_cache:
            if user.get_username() == username:
                flash("Username already exists!")
                return redirect("/makeaccount")

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
        up.set_active_user(new_user.get_index())

        return redirect("/home")

    def get(self):
        if is_logged_in():
            return redirect("/home")

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

        return abort(404)

    def get(self):
        return make_response(render_template('welcome.html'), 200,)

class Home(Resource):
    def post(self):
        if not is_logged_in():
            return please_login_alert()

        if logout_post():
            return logout_wrapper()

        parser.add_argument('viewhotels', type=bool)
        parser.add_argument('searchhotels', type=bool)
        parser.add_argument('viewreservations', type=bool)
        parser.add_argument('customers', type=bool)
        parser.add_argument('editaccount', type=bool)
        args = parser.parse_args()

        if args['viewhotels']:
            return redirect("/hotels")
        if args['searchhotels']:
            return redirect("/hotels/search")
        if args['viewreservations']:
            return redirect("/reservations")
        if args['editaccount']:
            return redirect("/customers/"+str(up.active_user_index))

        if args['customers']:
            if not is_admin_logged_in():
                return admin_only_alert()

            return redirect("/customers/admin")

        return abort(404)

    def get(self):
        if not is_logged_in():
            return please_login_alert()

        curr_user = up.get_active_user_dict()
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
api.add_resource(EditHotel, '/hotels/<int:hotel_id>/edit')
api.add_resource(MakeReservation, '/hotels/<int:hotel_id>/reserve')
api.add_resource(ConfirmReservation, '/hotels/<int:hotel_id>/reserve/confirm_<int:reservation_id>')
api.add_resource(ViewReservation, '/reservations')
api.add_resource(Customers, '/customers/admin')
api.add_resource(EditCustomer, '/customers/<int:user_id>')

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

    app.run()

    hotel_file.close()
    reservation_file.close()
    user_file.close()
