from app.models.car import Car

class CarBuilder:
    """
    Builder class for constructing Car objects.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self._car = Car()

    def set_owner(self, owner_email):
        self._car.owner = owner_email
        return self

    def set_model(self, model):
        self._car.model = model
        return self

    def set_year(self, year):
        self._car.year = year
        return self

    def set_mileage(self, mileage):
        self._car.mileage = mileage
        return self

    def set_price_per_day(self, price):
        self._car.price_per_day = price
        return self

    def set_location(self, location):
        self._car.location = location
        return self

    def set_availability(self, dates):
        self._car.availability = dates
        return self

    def set_discounts(self, discounts):
        self._car.discounts = discounts
        return self

    def build(self):
        car = self._car
        self.reset()
        return car

class CarDirector:
    """
    Director class to construct cars using predefined logic.
    """
    def __init__(self, builder: CarBuilder):
        self._builder = builder

    def create_basic_car(self, owner_email, model, year, mileage, price, location, availability, discounts):
        car_builder = (
            self._builder
            .set_owner(owner_email)
            .set_model(model)
            .set_year(year)
            .set_mileage(mileage)
            .set_price_per_day(price)
            .set_location(location)
            .set_availability(availability)
            .set_discounts(discounts)
        )
        if discounts:
            car_builder.set_discounts(discounts)

        return car_builder.build()


