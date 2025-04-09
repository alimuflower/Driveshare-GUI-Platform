from app.services.auth_service import AuthService
from app.services.car_service import CarService
from app.services.booking_service import BookingService, BookingObserver
from app.patterns.singleton import SessionManager
from datetime import datetime, timedelta


def get_upcoming_dates(days=30):
    today = datetime.today()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]


class MainMenuMediator:
    def __init__(self):
        self.auth_service = AuthService()
        self.car_service = CarService()
        self.booking_service = BookingService(self.car_service, self.auth_service)
        self.booking_service.add_observer(BookingObserver())

    def run(self):
        while True:
            user = SessionManager().get_user()

            if user is None:
                self.display_main_menu()
                choice = input("Choose an option: ")

                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login_user()
                elif choice == "3":
                    email = input("Enter your email for password recovery: ")
                    self.auth_service.recover_password(email)
                elif choice == "4":
                    print("Exiting DriveShare. Goodbye!")
                    break
                else:
                    print("Invalid option.")
            else:
                if user.role == "host":
                    self.host_menu(user)
                elif user.role == "guest":
                    self.guest_menu(user)

    def display_main_menu(self):
        print("\n=== DriveShare Main Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Recover Password")
        print("4. Exit")

    def register_user(self):
        email = input("Email: ")
        password = input("Password: ")
        name = input("Full Name: ")
        role_input = input("Register as host or guest? (h/g): ")
        role = "host" if role_input.lower() == "h" else "guest"
        print("\nAnswer the following 3 security questions:")
        q1 = input("What is your favorite color? ")
        q2 = input("What is your pet's name? ")
        q3 = input("What city were you born in? ")
        self.auth_service.register_user(email, password, name, [q1, q2, q3], role)
        user = self.auth_service.get_user_by_email(email)
        if user:
            self.auth_service.session.set_user(user)
            print(f"\n[Welcome] {user.name}, you are now logged in as a {role}.")

    def login_user(self):
        email = input("Email: ")
        password = input("Password: ")
        if self.auth_service.login_user(email, password):
            user = SessionManager().get_user()
            print(f"Welcome back, {user.name}!")

    def host_menu(self, user):
        print("\n=== Host Menu ===")
        print("1. View All Cars")
        print("2. Add Your Own Vehicle")
        print("3. Edit Vehicle Discounts")
        print("4. View Booking Menu")
        print("5. Delete a Vehicle")
        print("6. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            self.car_service.list_all_cars()
        elif choice == "2":
            brand = input("Vehicle Brand: ")
            model = input("Vehicle Model: ")

            while True:
                year_input = input("Model Year: ")
                if year_input.isdigit():
                    year = int(year_input)
                    break
                print("Model year must be a valid number.")

            while True:
                mileage_input = input("Mileage: ")
                if mileage_input.isdigit():
                    mileage = int(mileage_input)
                    break
                print("Mileage must be a valid number.")

            while True:
                price_input = input("Price per day: ")
                try:
                    price = float(price_input)
                    break
                except ValueError:
                    print("Price must be a valid number.")

            location = input("Location: ")
            self.car_service.add_car(user.email, f"{brand} {model}", year, mileage, price, location, get_upcoming_dates())

        elif choice == "3":
            owner_cars = [car for car in self.car_service.car_list if car.owner == user.email]
            if not owner_cars:
                print("You have no cars listed.")
                return
            print("\nYour Cars:")
            for idx, car in enumerate(owner_cars):
                print(f"{idx + 1}. {car.model} - ${car.price_per_day}/day")
            car_index = input("Select a car to edit discounts (by number): ")
            if not car_index.isdigit() or int(car_index) < 1 or int(car_index) > len(owner_cars):
                print("Invalid selection.")
                return
            car = owner_cars[int(car_index) - 1]
            try:
                d3 = float(input("% discount for 3-day bookings: ") or 0)
                d7 = float(input("% discount for 7-day bookings: ") or 0)
                d20 = float(input("% discount for 20-day bookings: ") or 0)
                car.discounts = {
                    "3": d3 / 100 if d3 > 0 else 0,
                    "7": d7 / 100 if d7 > 0 else 0,
                    "20": d20 / 100 if d20 > 0 else 0,
                }
                print("Discounts updated.")
            except ValueError:
                print("Invalid input. Discounts not changed.")

        elif choice == "4":
            print("\n=== Bookings for Your Cars ===")
            for guest in self.auth_service.users:
                if guest.role == "guest" and guest.rental_history:
                    for r in guest.rental_history:
                        if r["owner"] == user.email:
                            print(f"Guest: {guest.name} | Car: {r['car']} | Days: {r['days']} | Total: ${r['total']} | Date: {r['date']}")

        elif choice == "5":
            owner_cars = [car for car in self.car_service.car_list if car.owner == user.email]
            if not owner_cars:
                print("You have no cars to delete.")
                return
            print("\nYour Cars:")
            for idx, car in enumerate(owner_cars):
                print(f"{idx + 1}. {car.model} - ${car.price_per_day}/day")
            car_index = input("Select a car to delete (by number): ")
            if not car_index.isdigit() or int(car_index) < 1 or int(car_index) > len(owner_cars):
                print("Invalid selection.")
                return
            self.car_service.car_list.remove(owner_cars[int(car_index) - 1])
            print("Car deleted successfully.")

        elif choice == "6":
            self.auth_service.logout_user()
        else:
            print("Invalid option.")

    def guest_menu(self, user):
        print("\n=== Guest Menu ===")
        print("1. View All Cars")
        print("2. Book a Car")
        print("3. Checkout")
        print("4. View Rental History")
        print("5. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            cars = self.car_service.list_all_cars(return_list=True)
            for idx, car in enumerate(cars):
                discount_info = []
                for d in ["3", "7", "20"]:
                    if car.discounts.get(d):
                        discount_info.append(f"{d}-day: {int(car.discounts[d]*100)}% off")
                print(f"{idx+1}. {car.model} - ${car.price_per_day}/day" + (f" | Discounts: {', '.join(discount_info)}" if discount_info else ""))

        elif choice == "2":
            cars = self.car_service.list_all_cars(return_list=True)
            if not cars:
                return
            for i, car in enumerate(cars):
                print(f"{i+1}. {car.model} - ${car.price_per_day}/day")
            car_index = int(input("Choose car number: ")) - 1
            days = int(input("Days to book: "))
            self.booking_service.book_car(car_index, days)

        elif choice == "3":
            self.booking_service.checkout()

        elif choice == "4":
            if not user.rental_history:
                print("No rental history.")
            else:
                for r in user.rental_history:
                    print(f"Car: {r['car']}, Host: {r['owner']}, Date: {r['date']}, Total: ${r['total']}")

        elif choice == "5":
            self.auth_service.logout_user()
        else:
            print("Invalid option.")

def main():
    MainMenuMediator().run()

if __name__ == "__main__":
    main()
