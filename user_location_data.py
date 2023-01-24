import os
import requests

API_KEY = os.environ['API_KEY']

class UserLocationData:
    """Object that gets a user's place_id, latitude, and longitude"""

    def __init__(self, user_address):
        location_endpoint = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?" \
                            f"input={user_address}&inputtype=textquery&fields=place_id%2Cgeometry%2Cformatted_address" \
                            f"&key={API_KEY}"
        location_response_json = requests.get(location_endpoint).json()['candidates'][0]

        self.formatted_address = location_response_json['formatted_address']
        self.place_id = location_response_json['place_id']
        self.lat = location_response_json['geometry']['location']['lat']
        self.lng = location_response_json['geometry']['location']['lng']