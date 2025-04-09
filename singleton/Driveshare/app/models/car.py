class Car:
    """
    Represents a car listed for rental on DriveShare.
    """
    def __init__(self):
        self.owner = None
        self.model = None
        self.year = None
        self.mileage = None
        self.price_per_day = None
        self.location = None
        self.availability = []  # list of available date strings (e.g., '2025-04-10')
        self.discounts = {}  # host-defined discounts: {"3": 0.05, "7": 0.10, "20": 0.15}

    def __repr__(self):
        base = (
            f"<Car {self.model} ({self.year}) - ${self.price_per_day}/day - "
            f"Owner: {self.owner} - Location: {self.location}>"
        )
        if self.discounts:
            formatted = [f"{k}-day: {int(v * 100)}%" for k, v in sorted(self.discounts.items()) if v > 0]
            return f"{base} - Discounts: {', '.join(formatted)}"
        return base

