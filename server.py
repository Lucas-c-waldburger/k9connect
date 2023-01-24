from park_place_info import ParkPlaceDetails
from user_location_data import UserLocationData
from parksearch import ParkSearch
import os
from flask import Flask, render_template
app = Flask(__name__)

API_KEY = os.environ['API_KEY']


# # # TO DO # # #
# decide if modules should nest in parksearch of something different (i dont like having to reinsert
#   the users address into each park place details object!!!!)
# maybe create a meta-modules with everything inside of "test parksearch stuff"



# ----TEST PARKSEARCH STUFF---- #
user_a_address = "207A Derry Hill Court Mount Laurel NJ 08028"
user_a_location_data = UserLocationData(user_a_address)
user_a_parksearch = ParkSearch(user_a_location_data)
dog_parks_place_id_list = user_a_parksearch.populate_park_id_list()
park_details_object_list = [ParkPlaceDetails(park_id, user_a_location_data.formatted_address) for park_id in dog_parks_place_id_list]


def sort_by_miles_away(park):
    return park.travel_details.distance
sorted_park_details_objects = sorted(park_details_object_list, key=sort_by_miles_away)


@app.route("/")
def home_page():
    return render_template("index.html", park_details=sorted_park_details_objects)

# @app.route("/parksearch")
# def parksearch_page():



if __name__ == "__main__":
    app.run(debug=True)
