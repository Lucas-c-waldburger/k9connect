
class ParkRatings:
    def __init__(self, place_details_json):

        self.most_pos_value = None
        self.most_pos_text = None

        self.most_neg_value = None
        self.most_neg_text = None

        self.average_rating = None
        self.stars_line = None

        try:
            self.reviews_as_list = place_details_json["result"]["reviews"]
        except KeyError:
            pass
        else:
            self.review_values = [review["rating"] for review in self.reviews_as_list]
            self.review_texts = [review["text"] for review in self.reviews_as_list]

            self.most_pos_value = max(self.review_values)
            self.most_pos_text = self.review_texts[self.review_values.index(self.most_pos_value)]

            self.most_neg_value = min(self.review_values)  # Find way to get different review if most pos review value same as neg
            self.most_neg_text = self.review_texts[self.review_values.index(self.most_neg_value)]

        try:
            self.average_rating = place_details_json["result"]["rating"]
            self.stars_line = self.render_stars()
        except KeyError:
            try:
                self.average_rating = round(sum(self.review_values) / len(self.review_values))
                self.stars_line = self.render_stars()
            except NameError or KeyError:
                self.average_rating = None

    def render_stars(self):
        stars_line = ""
        for star in range(0, round(self.average_rating)):
            stars_line += "⭐"
        return stars_line