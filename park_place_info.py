import requests
import os
from park_ratings import ParkRatings
from park_travel_details import ParkTravelDetails

API_KEY = os.environ['API_KEY']


class ParkPlaceDetails:
    def __init__(self, park_id, user_formatted_address):
        place_details_endpoint = f"https://maps.googleapis.com/maps/api/place/details/json?" \
                                 f"&place_id={park_id}&key={API_KEY}"
        self.place_details_response_json = requests.get(place_details_endpoint).json()

        if self.check_if_permanently_closed():
            pass

        else:
            self.name = self.place_details_response_json["result"]["name"]
            self.formatted_address = self.place_details_response_json["result"]["formatted_address"]
            self.maps_url = self.place_details_response_json["result"]["url"]

            # TRAVEL DETAILS
            self.travel_details = ParkTravelDetails(user_address=user_formatted_address,
                                                    park_address=self.formatted_address)
            # RATING INFO
            self.ratings = ParkRatings(self.place_details_response_json)

            self.phone = self.try_phone()
            self.hours = self.try_hours()
            self.website_url = self.try_website_url()
            self.photo_url_list = self.try_photo_urls()


    def check_if_permanently_closed(self):
        if self.place_details_response_json["result"]["business_status"] != "OPERATIONAL":
            return True

    def try_phone(self):
        try:
            return self.place_details_response_json["result"]["formatted_phone_number"]
        except KeyError:
            return None

    def format_hours_response(self, hours):
        return [str(entry.encode('ascii', 'ignore')).strip("b").strip("'").replace("AM", "AM-") for entry in hours]

    def try_hours(self):
        try:
            hours = self.place_details_response_json["result"]["opening_hours"]["weekday_text"]
        except KeyError:
            return "Not available"
        else:
            return self.format_hours_response(hours)

    def try_website_url(self):
        try:
            return self.place_details_response_json["result"]["website"]
        except KeyError:
            return None

    def try_photo_urls(self):
        # return "place_images/Image_not_available.png"
        try:
            photo_reference_list = [entry["photo_reference"] for entry in
                                    self.place_details_response_json["result"]["photos"]]
        except KeyError:
            photo_url_list = [
                "data:image/png;base64,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"]
        else:
            photo_url_list = [
                f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={API_KEY}"
                for photo_ref in photo_reference_list]
        finally:
            return photo_url_list

        #
        #     photo_response = requests.get(photo_endpoint)
        #     photo_filename = f"place_images/{str(place_name)}.png"
        #
        #     with open(f"{photo_filename}", 'wb') as file:
        #         file.write(photo_response.content)
