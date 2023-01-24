import requests
import os

API_KEY = os.environ['API_KEY']


class ParkTravelDetails:
    def __init__(self, user_address, park_address):
        """Finds user's distance in miles from a dog park, as well as the estimated duration of travel time"""

        self.user_address = user_address
        self.park_address = park_address

        self.distance_matrix_endpoint = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={self.user_address}&" \
                                   f"destinations={self.park_address}&units=imperial&key={API_KEY}"

        self.distance_matrix_response_json = requests.get(self.distance_matrix_endpoint).json()

        self.distance = self.get_distance()
        self.duration = self.get_duration()

    def get_distance(self):
        return self.distance_matrix_response_json['rows'][0]['elements'][0]['distance']['text']

    def get_duration(self):
        return self.distance_matrix_response_json['rows'][0]['elements'][0]['duration']['text']

    def convert_matrix_distance_to_meters(self, matrix_distance):
        distance_in_meters = float("".join(matrix_distance.strip(" mi").split(","))) * 1609
        return distance_in_meters

