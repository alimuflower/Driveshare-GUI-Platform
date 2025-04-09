from app.patterns.singleton import SessionManager

class BookingObserver:
    def update(self, message):
        print(f"[BookingObserver] {message}")

class BookingService:
    def __init__(self, car_service, auth_service):
        self.car_service = car_service
        self.auth_service = auth_service
        self.active_bookings = {}  # {user_email: (car, days)}
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def book_car(self, car_index, days):
        user = SessionManager().get_user()
        if not user:
            print("[BookingService] You must be logged in to book a car.")
            return

        if user.email in self.active_bookings:
            print("[BookingService] You already have a pending booking.")
            return

        if days < 1 or days > 30:
            print("[BookingService] You can only book between 1 and 30 days.")
            return

        available_cars = self.car_service.car_list
        if not available_cars or car_index < 0 or car_index >= len(available_cars):
            print("[BookingService] Invalid car selection.")
            return

        car = available_cars[car_index]
        if len(car.availability) < days:
            print("[BookingService] Not enough available days for this car.")
            return

        self.active_bookings[user.email] = (car, days)
        print(f"[BookingService] Booking saved. Please proceed to checkout to confirm.")

    def checkout(self):
        user = SessionManager().get_user()
        if not user:
            print("[BookingService] You must be logged in to checkout.")
            return

        if user.email not in self.active_bookings:
            print("[BookingService] No active booking found.")
            return

        car, days = self.active_bookings[user.email]
        base_total = car.price_per_day * days
        final_total = base_total

        host_discount = 0
        for key in ["3", "7", "20"]:
            if int(key) <= days and key in car.discounts:
                host_discount = car.discounts[key]
        final_total -= final_total * host_discount

        # Show receipt preview
        print("\n=== Checkout Preview ===")
        print(f"Guest: {user.name}")
        print(f"Car: {car.model} ({car.year})")
        print(f"Location: {car.location}")
        print(f"Duration: {days} days")
        print(f"Rate: ${car.price_per_day}/day")
        print(f"Base Total: ${base_total:.2f}")
        if host_discount > 0:
            print(f"Host Discount Applied: {int(host_discount * 100)}%")
        print(f"Final Total: ${final_total:.2f}")
        print("=========================")

        #confirm = input("Do you want to confirm this booking? (y/n): ").strip().lower()
        #if confirm != "y":
        #    print("[BookingService] Booking cancelled.")
        #    del self.active_bookings[user.email]
        #    return

        # Reserve dates
        booked_dates = car.availability[:days]
        for date in booked_dates:
            self.car_service.update_availability(car, date, remove=True)

        # Record booking
        rental_record = {
            "car": car.model,
            "days": days,
            "total": round(final_total, 2),
            "owner": car.owner,
            "date": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        user.rental_history.append(rental_record)

        owner = self.auth_service.get_user_by_email(car.owner)
        if owner:
            owner.rental_history.append(rental_record)

        print("\n=== Booking Confirmed ===")
        print(f"Booking confirmed for {car.model} for {days} days.")
        self.notify_observers(f"Booking complete: {user.name} confirmed booking for {car.model}.")
        del self.active_bookings[user.email]


class MessageService:
    @staticmethod
    def send_notification(user, message):
        print(f"[MessageService] Notification to {user.email}: {message}")







