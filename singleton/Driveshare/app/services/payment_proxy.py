from app.patterns.singleton import SessionManager

class PaymentProxy:
    """
    Proxy class for handling rental payment simulation.
    """

    def pay(self, amount, recipient_email):
        user = SessionManager().get_user()
        if not user:
            print("[PaymentProxy] No user logged in.")
            return False

        if user.balance < amount:
            print("[PaymentProxy] Payment failed. Insufficient balance.")
            return False

        user.balance -= amount

        # Simulated notification
        print(f"[PaymentProxy] ${amount:.2f} paid to {recipient_email} by {user.email}")
        return True

