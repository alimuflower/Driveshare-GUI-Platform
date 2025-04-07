
class ReviewService:
    def __init__(self):
        self.reviews = {}

    def add_review(self, host_email, guest_email, car_model, rating, comment):
        if host_email not in self.reviews:
            self.reviews[host_email] = []
        self.reviews[host_email].append({
            "guest": guest_email,
            "car": car_model,
            "rating": rating,
            "comment": comment
        })

    def get_reviews_for_host(self, host_email):
        print(self.reviews.get(host_email, []))
        return self.reviews.get(host_email, [])
