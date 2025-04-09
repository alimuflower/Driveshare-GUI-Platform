import tkinter as tk
from tkinter import messagebox
from app.patterns.singleton import SessionManager


def view_inbox_gui(root, app):
    user = SessionManager().get_user()
    app.clear_frame()
    tk.Label(app.main_frame, text="Inbox", font=("Helvetica", 14)).pack(pady=10)

    messages = app.messaging_service.get_messages_for_host(user.email)
    if not messages:
        tk.Label(app.main_frame, text="No messages found.").pack()
    else:
        for m in messages:
            tk.Label(app.main_frame, text=f"From: {m[0]}").pack()
            tk.Label(app.main_frame, text=f"Message: {m[1]}", wraplength=400, justify="left").pack(pady=5)

    tk.Button(app.main_frame, text="Back", command=app.host_dashboard).pack(pady=10)


def view_reviews_gui(root, app):
    user = SessionManager().get_user()
    app.clear_frame()
    tk.Label(app.main_frame, text="My Reviews", font=("Helvetica", 14)).pack(pady=10)

    reviews = app.review_service.get_reviews_for_host(user.email)
    if not reviews:
        tk.Label(app.main_frame, text="No reviews found.").pack()
    else:
        for r in reviews:
            tk.Label(app.main_frame, text=f"From: {r['guest']}").pack()
            tk.Label(app.main_frame, text=f"Car: {r['car']}").pack()
            tk.Label(app.main_frame, text=f"Rating: {r['rating']} ⭐").pack()
            tk.Label(app.main_frame, text=f"Comment: {r['comment']}", wraplength=400, justify="left").pack(pady=5)

    tk.Button(app.main_frame, text="Back", command=app.host_dashboard).pack(pady=10)

