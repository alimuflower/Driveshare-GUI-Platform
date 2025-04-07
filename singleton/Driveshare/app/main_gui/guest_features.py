import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
from app.patterns.singleton import SessionManager

def show_available_cars(root, app):
    app.clear_frame()
    tk.Label(app.main_frame, text="Available Cars", font=("Helvetica", 14)).pack(pady=10)
    cars = app.car_service.list_all_cars(return_list=True)
    if not cars:
        tk.Label(app.main_frame, text="No cars available.").pack()
    else:
        for car in cars:
            tk.Label(app.main_frame, text=str(car)).pack()
    tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=10)

def show_booking_form(root, app):
    app.clear_frame()
    user = SessionManager().get_user()
    cars = app.car_service.list_all_cars(return_list=True)
    if not cars:
        tk.Label(app.main_frame, text="No cars available to book.").pack()
        tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=10)
        return

    tk.Label(app.main_frame, text="Select a Car to Book", font=("Helvetica", 14)).pack(pady=10)
    for idx, car in enumerate(cars):
        btn = tk.Button(app.main_frame, text=f"{idx + 1}. {car.model} ({car.year}) - ${car.price_per_day}/day",
                        command=lambda i=idx: confirm_days(i))
        btn.pack(pady=2)

    def confirm_days(index):
        days = simpledialog.askinteger("Booking Duration", "Enter number of days (1-30):", minvalue=1, maxvalue=30)
        if days:
            app.booking_service.book_car(index, days)

    tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=10)

def send_message_to_host_gui(root, app):
    app.clear_frame()
    user = SessionManager().get_user()

    tk.Label(app.main_frame, text="Send Message to Host", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(app.main_frame, text="Host Email:").pack()
    host_email_entry = tk.Entry(app.main_frame)
    host_email_entry.pack()

    tk.Label(app.main_frame, text="Message:").pack()
    message_entry = tk.Text(app.main_frame, height=5, width=40)
    message_entry.pack()

    def send():
        host_email = host_email_entry.get()
        message = message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty.")
            return
        app.messaging_service.send_message(user.email, host_email, message)
        messagebox.showinfo("Sent", "Message sent to host.")
        app.guest_dashboard()

    tk.Button(app.main_frame, text="Send Message", command=send).pack(pady=5)
    tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=5)

def leave_review_gui(root, app):
    app.clear_frame()
    user = SessionManager().get_user()
    if not user.rental_history:
        tk.Label(app.main_frame, text="No rentals to review.").pack()
        tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=10)
        return

    tk.Label(app.main_frame, text="Leave a Review", font=("Helvetica", 14)).pack(pady=10)

    for rental in user.rental_history:
        host = rental["owner"]
        car = rental["car"]

        frame = tk.Frame(app.main_frame)
        frame.pack(pady=5)
        tk.Label(frame, text=f"{car} rented from {host}").pack()

        tk.Label(frame, text="Rating (1-5):").pack()
        rating_entry = tk.Entry(frame)
        rating_entry.pack()

        tk.Label(frame, text="Review:").pack()
        text_entry = tk.Text(frame, height=3, width=40)
        text_entry.pack()

        def submit_review(host_email=host, car_model=car, r_entry=rating_entry, t_entry=text_entry):
            try:
                rating = int(r_entry.get())
                if not 1 <= rating <= 5:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Rating", "Please enter a number from 1 to 5.")
                return

            review_text = t_entry.get("1.0", tk.END).strip()
            if not review_text:
                messagebox.showerror("Missing Review", "Please enter a review message.")
                return

            app.review_service.add_review(host_email, user.email, car_model, rating, review_text)
            messagebox.showinfo("Success", "Review submitted!")
            app.guest_dashboard()

        tk.Button(frame, text="Submit Review", command=submit_review).pack(pady=3)

def show_payment_interface(root, app):
    app.clear_frame()
    user = SessionManager().get_user()

    if user.email not in app.booking_service.active_bookings:
        tk.Label(app.main_frame, text="No active booking to pay for.").pack()
        tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=10)
        return

    car, days = app.booking_service.active_bookings[user.email]
    base_total = car.price_per_day * days

    discount_total = base_total
    host_discount = 0
    for key in ["3", "7", "20"]:
        if int(key) <= days and key in car.discounts:
            host_discount = car.discounts[key]
    discount_total -= discount_total * host_discount

    guest_discount = 0.1 if simpledialog.askstring("Promo", "Enter promo code (optional):") == "firstride" else 0
    if guest_discount:
        discount_total -= discount_total * guest_discount

    tk.Label(app.main_frame, text="=== Payment Preview ===", font=("Helvetica", 12)).pack(pady=10)
    tk.Label(app.main_frame, text=f"Car: {car.model}").pack()
    tk.Label(app.main_frame, text=f"Duration: {days} days").pack()
    tk.Label(app.main_frame, text=f"Base Total: ${base_total:.2f}").pack()
    if host_discount:
        tk.Label(app.main_frame, text=f"Host Discount: {int(host_discount*100)}%").pack()
    if guest_discount:
        tk.Label(app.main_frame, text="Guest Discount: 10% (firstride)").pack()
    tk.Label(app.main_frame, text=f"Final Total: ${discount_total:.2f}").pack()

    def confirm_payment():
        app.payment_proxy.pay(discount_total, car.owner)
        app.booking_service.checkout()
        app.guest_dashboard()

    tk.Button(app.main_frame, text="Pay Now", command=confirm_payment).pack(pady=5)
    tk.Button(app.main_frame, text="Cancel", command=app.guest_dashboard).pack(pady=5)

def view_rental_history_gui(root, app):
    app.clear_frame()
    user = SessionManager().get_user()

    tk.Label(app.main_frame, text="Rental History", font=("Helvetica", 14)).pack(pady=10)

    if not user.rental_history:
        tk.Label(app.main_frame, text="No past rentals.").pack()
    else:
        for r in user.rental_history:
            tk.Label(app.main_frame, text=f"Car: {r['car']} | Host: {r['owner']} | Date: {r['date']} | Total: ${r['total']}").pack()

    tk.Button(app.main_frame, text="Back", command=app.guest_dashboard).pack(pady=10)

