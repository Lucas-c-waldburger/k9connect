import os
import requests

API_KEY = os.environ['API_KEY']

class ParkSearch:
    def __init__(self, user_location_data):

        self.user_location_data = user_location_data

        self.park_id_list = []

        self.next_page_token = None
        self.times_searched = 0

    def populate_park_id_list(self):
        if self.times_searched >= 3:
            print("All results have already been added to the park id list")
        else:
            if self.next_page_token is not None:
                dog_park_places_id_endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
                                              f"?pagetoken={self.next_page_token}&key={API_KEY}"

            else:
                dog_park_places_id_endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
                                              f"?keyword=dog park&radius=1000000&" \
                                              f"location={self.user_location_data.lat},{self.user_location_data.lng}&key={API_KEY}"

            dog_park_places_id_response = requests.get(dog_park_places_id_endpoint)

            for n in range(0, len(dog_park_places_id_response.json()['results'])):
                self.park_id_list.append(dog_park_places_id_response.json()['results'][n]['place_id'])

            if dog_park_places_id_response.json().get('next_page_token') is not None:
                self.next_page_token = dog_park_places_id_response.json().get('next_page_token')

            self.times_searched += 1

        return self.park_id_list