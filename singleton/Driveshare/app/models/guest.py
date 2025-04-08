import hashlib

class Guest:
    """
    Represents a Guest in the DriveShare system.
    Guests can browse cars, apply discounts, and checkout.
    """
    def __init__(self, email, password, name, security_answers):
        self.email = email
        self.name = name
        self.role = "guest"
        self.password = password
        self.security_answers = security_answers
        self.balance = 1000  # Starting balance
        self.rental_history = []
        self.reviews = []

    #def _hash_password(self, password):
    #    return hashlib.sha256(password.encode()).hexdigest()

    #def check_password(self, password_attempt):
    #    return self.password_hash == self._hash_password(password_attempt)

    def validate_security_answers(self, answers):
        return self.security_answers == answers

    def add_loyalty_points(self, points):
        self.loyalty_points += points

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def __repr__(self):
        return f"<Guest {self.email} | Balance: ${self.balance} | Loyalty: {self.loyalty_points} pts>"

    def __str__(self):
        return f"{self.name} ({self.email})"


