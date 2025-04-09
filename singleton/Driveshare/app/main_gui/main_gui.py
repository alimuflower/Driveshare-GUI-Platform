import email
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from app.services.auth_service import AuthService
from app.services.car_service import CarService
from app.services.booking_service import BookingService, BookingObserver
from app.services.messaging_service import MessagingService
from app.services.review_service import ReviewService
from app.services.payment_proxy import PaymentProxy
from app.patterns.singleton import SessionManager
from datetime import datetime, timedelta

class DriveShareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DriveShare Platform")

        self.auth_service = AuthService()
        self.car_service = CarService()
        self.booking_service = BookingService(self.car_service, self.auth_service)
        self.messaging_service = MessagingService()
        self.booking_service.add_observer(BookingObserver(self.messaging_service))
        self.review_service = ReviewService()
        self.payment_proxy = PaymentProxy()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Welcome to DriveShare", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Login", width=20, command=self.login_user).pack(pady=5)
        tk.Button(self.main_frame, text="Register", width=20, command=self.register_user).pack(pady=5)
        tk.Button(self.main_frame, text="Forgot Password", width=20, command=self.show_forgot).pack(pady=5)
        tk.Button(self.main_frame, text="Exit", width=20, command=self.root.quit).pack(pady=5)

    def login_user(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Email:").pack()
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack()

        tk.Label(self.main_frame, text="Password:").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        def attempt_login():
            email = email_entry.get()
            password = password_entry.get()
            if self.auth_service.login_user(email, password):
                user = SessionManager().get_user()
                if user.role == "host":
                    self.host_dashboard()
                else:
                    self.guest_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")

        tk.Button(self.main_frame, text="Login", command=attempt_login).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.show_main_menu).pack()


    def show_forgot(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Answer the following questions:", font=("Helvetica", 16)).pack(pady=10)


        tk.Label(self.main_frame, text="What is your email?").pack(pady=10)
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack()

        tk.Label(self.main_frame, text="What is your favorite color?").pack(pady=10)
        color_entry = tk.Entry(self.main_frame)
        color_entry.pack()

        tk.Label(self.main_frame, text="What is the name of your pet?").pack(pady=10)
        pet_entry = tk.Entry(self.main_frame)
        pet_entry.pack()

        tk.Label(self.main_frame, text="What is the name of the city you were born in?").pack(pady=10)
        city_entry = tk.Entry(self.main_frame)
        city_entry.pack()

        def submit_answers():
            email = email_entry.get()
            answers = [
                color_entry.get(),
                pet_entry.get(),
                city_entry.get()
            ]

            success = self.auth_service.recover_password(email, answers)


            if success:
                tk.messagebox.showinfo("Success", f"Identity confirmed. your password is: {success}")
            else:
                tk.messagebox.showerror("Failed", "Security answers incorrect. Password recovery failed.")

        tk.Button(self.main_frame, text="Submit", command=submit_answers).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.show_main_menu).pack(pady=10)



    def register_user(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Full Name: ").pack()
        name_entry = tk.Entry(self.main_frame)
        name_entry.pack()

        tk.Label(self.main_frame, text="Email: ").pack()
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack()

        tk.Label(self.main_frame, text="Password: ").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        def getPass():
            return password_entry.get()

        tk.Label(self.main_frame, text="Role (host/guest):").pack()
        role_entry = tk.Entry(self.main_frame)
        role_entry.pack()

        tk.Label(self.main_frame, text="Favorite Color:").pack()
        q1_entry = tk.Entry(self.main_frame)
        q1_entry.pack()

        tk.Label(self.main_frame, text="Pet's Name:").pack()
        q2_entry = tk.Entry(self.main_frame)
        q2_entry.pack()

        tk.Label(self.main_frame, text="City Born In:").pack()
        q3_entry = tk.Entry(self.main_frame)
        q3_entry.pack()

        def register():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            role = role_entry.get().lower()
            answers = [q1_entry.get(), q2_entry.get(), q3_entry.get()]


            self.auth_service.register_user(email, password, name, answers, role)
            user = self.auth_service.get_user_by_email(email)
            if user:
                SessionManager().set_user(user)
                if role == "host":
                    self.host_dashboard()
                else:
                    self.guest_dashboard()

        tk.Button(self.main_frame, text="Submit", command=register).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.show_main_menu).pack()

    def host_dashboard(self):
        self.clear_frame()
        user = SessionManager().get_user()
        tk.Label(self.main_frame, text=f"Welcome, {user.name} (Host)", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="Add Vehicle", command=self.add_vehicle).pack(pady=5)
        tk.Button(self.main_frame, text="Edit Vehicles", command=self.edit_vehicle).pack(pady=5)
        tk.Button(self.main_frame, text="View All Cars", command=self.view_cars).pack(pady=5)
        tk.Button(self.main_frame, text="Check Inbox 📥", command=self.view_inbox).pack(pady=5)
        tk.Button(self.main_frame, text="View My Reviews 💬", command=self.view_reviews).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=10)

    def guest_dashboard(self):
        self.clear_frame()
        user = SessionManager().get_user()
        tk.Label(self.main_frame, text=f"Welcome, {user.name} (Guest)", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="Browse Cars", command=self.view_cars).pack(pady=5)
        tk.Button(self.main_frame, text="Book a Car", command=self.book_car).pack(pady=5)
        tk.Button(self.main_frame, text="Send Message to Host", command=self.send_message_to_host).pack(pady=5)
        tk.Button(self.main_frame, text="Leave a Review", command=self.leave_review).pack(pady=5)
        tk.Button(self.main_frame, text="Pay for Rental", command=self.make_payment).pack(pady=5)
        tk.Button(self.main_frame, text="Rental History", command=self.view_rental_history).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_vehicle(self):
        from app.main_gui.vehicle_forms import show_add_vehicle_form
        show_add_vehicle_form(self.root, self)

    def edit_vehicle(self):
        from app.main_gui.vehicle_forms import show_edit_vehicle_form
        show_edit_vehicle_form(self.root, self)

    def view_cars(self):
        from app.main_gui.guest_features import show_available_cars
        show_available_cars(self.root, self)

    def book_car(self):
        from app.main_gui.guest_features import show_booking_form
        show_booking_form(self.root, self)

    def send_message_to_host(self):
        from app.main_gui.guest_features import send_message_to_host_gui
        send_message_to_host_gui(self.root, self)

    def leave_review(self):
        from app.main_gui.guest_features import leave_review_gui
        leave_review_gui(self.root, self)

    def make_payment(self):
        from app.main_gui.guest_features import show_payment_interface
        show_payment_interface(self.root, self)

    def view_rental_history(self):
        from app.main_gui.guest_features import view_rental_history_gui
        view_rental_history_gui(self.root, self)

    def view_inbox(self):
        from app.main_gui.host_features import view_inbox_gui
        view_inbox_gui(self.root, self)

    def view_reviews(self):
        from app.main_gui.host_features import view_reviews_gui
        view_reviews_gui(self.root, self)

    def logout(self):
        self.auth_service.logout_user()
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = DriveShareGUI(root)
    root.mainloop()








