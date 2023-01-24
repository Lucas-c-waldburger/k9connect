
import requests

class ParkSearch:
    def __init__(self, user):

        self.park_id_list = []

        self.populate_park_id_list(user)

    def populate_park_id_list(self, user, *next_page_token):

        dog_park_places_id_endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
                                        f"?keyword=dog park&radius=1000000{next_page_token}&location={user.lat},{user.lng}&key={API_KEY}"

        dog_park_places_id_response = requests.get(dog_park_places_id_endpoint)

        for n in range(0, len(dog_park_places_id_response.json()['results'])):
            id = dog_park_places_id_response.json()['results'][n]['place_id']
            self.park_id_list.append(id)

        if dog_park_places_id_response.json().get('next_page_token') is not None:
            new_next_page_token = f"&pagetoken={dog_park_places_id_response.json().get('next_page_token')}"
            self.populate_park_id_list(user, new_next_page_token)


        print(f"all = {self.park_id_list}")


def get_dog_park_place_ids_as_list(*users):
    all_dog_parks_place_id_list = []
    shared_dog_parks_place_id_list = []
    next_page = "&radius=100"
    for user in users:
        dog_park_places_id_endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
                                      f"?keyword=dog park{next_page}&location={user.lat},{user.lng}&key={API_KEY}"
        dog_park_places_id_response = requests.get(dog_park_places_id_endpoint)

        for n in range(0, len(dog_park_places_id_response.json()['results'])):
            id = dog_park_places_id_response.json()['results'][n]['place_id']

            if id in all_dog_parks_place_id_list and id not in shared_dog_parks_place_id_list:
                shared_dog_parks_place_id_list.append(id)
            else:
                all_dog_parks_place_id_list.append(id)
    print(f"all = {all_dog_parks_place_id_list}")
    print(f"shared = {shared_dog_parks_place_id_list}")
    return shared_dog_parks_place_id_list