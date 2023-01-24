import requests
import os
from geographiclib.geodesic import Geodesic
from park_place_info import ParkPlaceDetails
from user_location_data import UserLocationData
from parksearch import ParkSearch

# PLACE ID
API_KEY = os.environ['API_KEY']


# ---------USER LOCATION DATA---------- #
user_a_address = "207A Derry Hill Court Mount Laurel NJ 08028"
# user_b_address = "10 Fairview Dr. South Basking Ridge NJ 07920"

user_a_location_data = UserLocationData(user_a_address)
# user_b = UserLocationData(user_b_address)


# ---------DOG PARK PLACE_IDS---------- #



# def find_shared_parks(user_1, user_2):
#     user_1_parksearch = ParkSearch(user_1)
#     user_2_parksearch = ParkSearch(user_2)
#
#     matching_park_list = []
#
#     while len(matching_park_list) < 2 or user_1_parksearch.times_searched < 3:
#         user_1_parksearch.populate_park_id_list()
#         user_2_parksearch.populate_park_id_list()
#         for park in user_2_parksearch.park_id_list:
#             if park in user_1_parksearch.park_id_list:
#                 matching_park_list.append(park)
#         time.sleep(1)
#
#     return matching_park_list

user_a_parksearch = ParkSearch(user_a_location_data)
dog_parks_place_id_list = user_a_parksearch.populate_park_id_list()
# print(dog_parks_place_id_list)

# ---------DOG PARK DETAILS---------- #
park_details_object_list = [ParkPlaceDetails(park_id) for park_id in dog_parks_place_id_list]

# for park in park_details_object_list:
#     print(park.name)

# ---------DOG PARK PLACE_ID LIST COMPARE 2 USERS---------- #


def find_distance_between_users(user_1, user_2):
    distance_matrix_endpoint = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=" \
                               f"{user_1.formatted_address}&destinations={user_2.formatted_address}&units=" \
                               f"imperial&key={API_KEY}"
    distance_matrix_response = requests.get(distance_matrix_endpoint)

    travel_distance = distance_matrix_response.json()['rows'][0]['elements'][0]['distance']['text']
    distance_in_meters = float("".join(travel_distance.strip(" mi").split(","))) * 1609
    return distance_in_meters


def find_midway_lat_lng(user_1, user_2):
    # define path between user 1 and 1
    l = Geodesic.WGS84.InverseLine(user_1.lat, user_1.lng, user_2.lat, user_2.lng)
    # Compute the midpoint
    m = l.Position(0.5 * l.s13)
    return m['lat2'], m['lon2']

#
#     # # PHOTOS
#     photo_filename = "place_images/Image_not_available.png"
#     # try:
#     #     photo_reference = place_details_response.json()["result"]["photos"][0]["photo_reference"]
#     # except KeyError:
#     #     photo_filename = "place_images/Image_not_available.png"
#     # else:
#     #     photo_endpoint = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"
#     #
#     #     photo_response = requests.get(photo_endpoint)
#     #     photo_filename = f"place_images/{str(place_name)}.png"
#     #
#     #     with open(f"{photo_filename}", 'wb') as file:
#     #         file.write(photo_response.content)
#     #
#

# ----------- FINDING HOW MANY MILES AWAY DOG PARKS ARE FROM USER LOCATION ------------ #


for place in park_details_object_list:
    print(place.photo_url_list[0])

