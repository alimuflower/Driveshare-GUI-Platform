import hashlib
import re

class Host:
    """
    Represents a Host in the DriveShare system.
    Hosts can list cars and manage availability.
    """
    def __init__(self, email, password, name, security_answers):
        if not self._is_valid_email(email):
            raise ValueError("Invalid email. Must be Gmail, Yahoo, or Outlook.")
        if not self._is_valid_password(password):
            raise ValueError("Password must be at least 8 characters long.")

        self.email = email
        self.name = name
        self.role = "host"
        self.password_hash = self._hash_password(password)
        self.security_answers = security_answers  # list of 3 answers
        self.balance = 1000  # default balance for simulation
        self.rental_history = []  # list to store rental records
        self.reviews = []  # list to store reviews
        self.loyalty_points = 0  # for discounts

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password_attempt):
        return self.password_hash == self._hash_password(password_attempt)

    def validate_security_answers(self, answers):
        return self.security_answers == answers

    def add_loyalty_points(self, points):
        self.loyalty_points += points

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def _is_valid_email(self, email):
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        return any(email.endswith("@" + domain) for domain in allowed_domains)

    def _is_valid_password(self, password):
        return len(password) >= 8

    def __repr__(self):
        return f"<Host {self.email} | Balance: ${self.balance} | Loyalty: {self.loyalty_points} pts>"

    def __str__(self):
        return f"{self.name} ({self.email})"



