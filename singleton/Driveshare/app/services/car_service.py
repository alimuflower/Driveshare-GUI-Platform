from app.patterns.builder import CarBuilder, CarDirector
from app.patterns.class_strategy import PricingStrategy, StandardPricing

class CarService:
    """
    Service for creating and managing car listings.
    """
    def __init__(self):
        self.car_list = []  # in-memory list for now
        self.builder = CarBuilder()
        self.director = CarDirector(self.builder)
        self.pricing_strategy = StandardPricing()

    def set_pricing_strategy(self, strategy: PricingStrategy):
        self.pricing_strategy = strategy

    def calculate_price(self, car, days, user):
        return self.pricing_strategy.calculate_price(car.price_per_day, days, user)

    def add_car(self, owner_email, model, year, mileage, price, location, availability):
        car = self.director.create_basic_car(
            owner_email=owner_email,
            model=model,
            year=year,
            mileage=mileage,
            price=price,
            location=location,
            availability=availability
        )

        print("\nDefine optional discounts for long bookings:")
        try:
            d3 = float(input("% discount for 3-day bookings (e.g., 5 for 5%): ") or 0)
            d7 = float(input("% discount for 7-day bookings (e.g., 10 for 10%): ") or 0)
            d20 = float(input("% discount for 20-day bookings (e.g., 15 for 15%): ") or 0)
            car.discounts = {
                "3": d3 / 100 if d3 > 0 else 0,
                "7": d7 / 100 if d7 > 0 else 0,
                "20": d20 / 100 if d20 > 0 else 0,
            }
        except ValueError:
            print("Invalid discount input. Skipping custom discounts.")
            car.discounts = {}

        self.car_list.append(car)
        print(f"[CarService] Car '{model}' added for owner '{owner_email}'.")

    def list_all_cars(self, return_list=False):
        if not self.car_list:
            print("[CarService] No cars listed yet.")
        for idx, car in enumerate(self.car_list):
            discount_info = []
            if hasattr(car, "discounts"):
                for key in ["3", "7", "20"]:
                    if car.discounts.get(key):
                        discount_info.append(f"{key}-day: {int(car.discounts[key]*100)}% off")
            print(f"{idx + 1}. {car}" + (f" | Discounts: {', '.join(discount_info)}" if discount_info else ""))
        if return_list:
            return self.car_list

    def find_available_cars(self, location=None, date=None):
        results = []
        for car in self.car_list:
            if location and location.lower() not in car.location.lower():
                continue
            if date and date not in car.availability:
                continue
            results.append(car)

        if not results:
            print("[CarService] No matching cars found.")
        else:
            for car in results:
                print(car)
        return results

    def update_availability(self, car, date, remove=True):
        if remove:
            if date in car.availability:
                car.availability.remove(date)
                print(f"[CarService] Removed {date} from availability for {car.model}.")
        else:
            if date not in car.availability:
                car.availability.append(date)
                print(f"[CarService] Added {date} to availability for {car.model}.")

    def update_car_listing(self, owner_email, car_index, new_price=None, new_availability=None):
        owner_cars = [car for car in self.car_list if car.owner == owner_email]
        if not owner_cars:
            print("[CarService] You have no cars listed.")
            return False
        if car_index < 0 or car_index >= len(owner_cars):
            print("[CarService] Invalid car selection.")
            return False
        car = owner_cars[car_index]
        if new_price is not None:
            car.price_per_day = new_price
        if new_availability is not None:
            car.availability = new_availability
        print(f"[CarService] Car '{car.model}' listing updated.")
        return True






