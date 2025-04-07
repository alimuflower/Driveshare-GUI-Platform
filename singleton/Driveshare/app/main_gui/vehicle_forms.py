import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from app.patterns.singleton import SessionManager

# Host: Add a New Vehicle
def show_add_vehicle_form(root, app):
    app.clear_frame()
    frame = app.main_frame
    user = SessionManager().get_user()

    tk.Label(frame, text="Add Vehicle", font=("Helvetica", 14)).pack(pady=10)

    brands = ['Toyota', 'Honda', 'Ford', 'BMW', 'Chevrolet', 'Tesla', 'Nissan', 'Kia', 'Hyundai']
    
    tk.Label(frame, text="Make:").pack()
    make_var = tk.StringVar()
    make_menu = ttk.Combobox(frame, textvariable=make_var, values=brands)
    make_menu.pack()

    tk.Label(frame, text="Model:").pack()
    model_entry = tk.Entry(frame)
    model_entry.pack()

    tk.Label(frame, text="Year (2010-2025):").pack()
    year_entry = tk.Entry(frame)
    year_entry.pack()

    tk.Label(frame, text="Mileage (0-125000):").pack()
    mileage_entry = tk.Entry(frame)
    mileage_entry.pack()

    tk.Label(frame, text="Price per day:").pack()
    price_entry = tk.Entry(frame)
    price_entry.pack()

    tk.Label(frame, text="Location:").pack()
    location_entry = tk.Entry(frame)
    location_entry.pack()

    tk.Label(app.main_frame, text="Discounts: 3, 7, 20 days (%):").pack()
    d3_entry = tk.Entry(frame);# d3.insert(0, str(car.discounts.get("3", 0)*100)); d3.pack()
    d7_entry = tk.Entry(frame);# d7.insert(0, str(car.discounts.get("7", 0)*100)); d7.pack()
    d20_entry = tk.Entry(frame);# d20.insert(0, str(car.discounts.get("20", 0)*100)); d20.pack()
    d3_entry.pack()
    d7_entry.pack()
    d20_entry.pack()

    def submit():
        try:
            make = make_var.get()
            model = model_entry.get()
            year = int(year_entry.get())
            if year < 2010 or year > 2025:
                raise ValueError("Year must be between 2010 and 2025")
            mileage = int(mileage_entry.get())
            if mileage < 0 or mileage > 125000:
                raise ValueError("Mileage must be between 0 and 125000")
            price = float(price_entry.get())
            location = location_entry.get()
            d3 = float(d3_entry.get())
            d7 = float(d7_entry.get())
            d20 = float(d20_entry.get())
            full_model = f"{make} {model}"
            availability = [(datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
            app.car_service.add_car(user.email, full_model, year, mileage, price, location, availability, d3, d7, d20)
            messagebox.showinfo("Success", "Vehicle added!")
            app.host_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Submit Vehicle", command=submit).pack(pady=10)
    tk.Button(frame, text="Back", command=app.host_dashboard).pack(pady=5)


# Host: Edit or Delete Existing Vehicles
def show_edit_vehicle_form(root, app):
    app.clear_frame()
    frame = app.main_frame
    user = SessionManager().get_user()
    user_cars = [car for car in app.car_service.car_list if car.owner == user.email]

    if not user_cars:
        tk.Label(frame, text="You have no listed vehicles.").pack(pady=10)
        tk.Button(frame, text="Back", command=app.host_dashboard).pack(pady=5)
        return

    tk.Label(frame, text="Edit Your Vehicles", font=("Helvetica", 14)).pack(pady=10)

    def show_edit_screen(car):
        app.clear_frame()
        tk.Label(app.main_frame, text=f"Editing: {car.model} ({car.year})", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(app.main_frame, text="New Price:").pack()
        price_entry = tk.Entry(app.main_frame)
        price_entry.insert(0, str(car.price_per_day))
        price_entry.pack()

        tk.Label(app.main_frame, text="Availability (comma-separated YYYY-MM-DD):").pack()
        avail_entry = tk.Entry(app.main_frame)
        avail_entry.insert(0, ", ".join(car.availability))
        avail_entry.pack()

        tk.Label(app.main_frame, text="Discounts: 3, 7, 20 days (%):").pack()
        d3 = tk.Entry(app.main_frame); d3.insert(0, str(car.discounts.get("3", 0)*100)); d3.pack()
        d7 = tk.Entry(app.main_frame); d7.insert(0, str(car.discounts.get("7", 0)*100)); d7.pack()
        d20 = tk.Entry(app.main_frame); d20.insert(0, str(car.discounts.get("20", 0)*100)); d20.pack()

        def apply_changes():
            try:
                car.price_per_day = float(price_entry.get())
                car.availability = [d.strip() for d in avail_entry.get().split(",") if d.strip()]
                car.discounts = {
                    "3": float(d3.get())/100 if d3.get() else 0,
                    "7": float(d7.get())/100 if d7.get() else 0,
                    "20": float(d20.get())/100 if d20.get() else 0
                }
                messagebox.showinfo("Success", "Vehicle updated.")
                app.host_dashboard()
            except ValueError:
                messagebox.showerror("Invalid input", "Please check your entries.")

        def delete_vehicle():
            # Check if car has been booked before deletion
            for guest in app.auth_service.users:
                if guest.role == 'guest' and hasattr(guest, 'rental_history'):
                    for r in guest.rental_history:
                        if r["car"] == car.model and r["owner"] == car.owner:
                            messagebox.showerror("Delete Error", "This car has bookings and cannot be deleted.")
                            return
            app.car_service.car_list.remove(car)
            messagebox.showinfo("Deleted", "Vehicle deleted.")
            app.host_dashboard()

        tk.Button(app.main_frame, text="Save Changes", command=apply_changes).pack(pady=5)
        tk.Button(app.main_frame, text="Delete Vehicle", command=delete_vehicle).pack(pady=5)
        tk.Button(app.main_frame, text="Back", command=lambda: show_edit_vehicle_form(root, app)).pack(pady=5)

    for car in user_cars:
        tk.Button(frame, text=f"{car.model} ({car.year}) - ${car.price_per_day}", command=lambda c=car: show_edit_screen(c)).pack(pady=3)

    tk.Button(frame, text="Back", command=app.host_dashboard).pack(pady=10)


