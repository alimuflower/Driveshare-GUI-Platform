from app.models.host import Host
from app.models.guest import Guest
from app.patterns.singleton import SessionManager

# Chain of Responsibility Base
class RecoveryHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, correct_answer, attempt):
        if self.check(correct_answer, attempt):
            if self.next_handler:
                return self.next_handler.handle_chain()
            return True
        return False

    def check(self, correct, attempt):
        return correct.strip().lower() == attempt.strip().lower()

    def handle_chain(self):
        raise NotImplementedError()


class SecurityQuestionHandler(RecoveryHandler):
    def __init__(self, question_text, correct_answer, next_handler=None):
        super().__init__(next_handler)
        self.question_text = question_text
        self.correct_answer = correct_answer

    def handle_chain(self):
        print(f"[Security Question] {self.question_text}")
        attempt = input("Answer: ")
        return self.handle(self.correct_answer, attempt)


class AuthService:
    """
    Handles user registration, login, logout, and password recovery.
    """
    def __init__(self):
        self.users = []  # In-memory user store
        self.session = SessionManager()

    def register_user(self, email, password, name, security_answers, role="guest"):
        """
        Register a new user as host or guest.
        """
        if any(user.email == email for user in self.users):
            print("[AuthService] A user with this email already exists.")
            return

        if not self._valid_email_domain(email):
            print("[AuthService] Invalid registration: Email must be gmail, yahoo, or outlook.")
            return

        if len(password) < 8:
            print("[AuthService] Invalid registration: Password must be at least 8 characters.")
            return

        role = role.lower()
        if role == "host":
            user = Host(email, password, name, security_answers)
        elif role == "guest":
            user = Guest(email, password, name, security_answers)
        else:
            print("[AuthService] Invalid role. Must be 'host' or 'guest'.")
            return

        self.users.append(user)
        print(f"[AuthService] User '{email}' registered successfully as a {role}.")

    def login_user(self, email, password):
        """
        Log a user into the system.
        """
        for user in self.users:
            if user.email == email and user.check_password(password):
                self.session.set_user(user)
                print(f"[AuthService] Login successful. Welcome, {user.name}!")
                return True

        print("[AuthService] Login failed. Invalid credentials.")
        return False

    def logout_user(self):
        """
        Log out the currently logged-in user.
        """
        current_user = self.session.get_user()
        if current_user:
            print(f"[AuthService] User '{current_user.email}' has been logged out.")
        self.session.logout()

    def recover_password(self, email):
        """
        Initiates password recovery using security questions.
        """
        user = self.get_user_by_email(email)
        if not user:
            print("[AuthService] No user found with that email.")
            return False

        q1 = SecurityQuestionHandler("What is your favorite color?", user.security_answers[0])
        q2 = SecurityQuestionHandler("What is your pet's name?", user.security_answers[1])
        q3 = SecurityQuestionHandler("What city were you born in?", user.security_answers[2])

        q1.next_handler = q2
        q2.next_handler = q3

        print("[AuthService] Answer the following security questions:")
        if q1.handle_chain():
            print("[AuthService] Identity confirmed. You may now reset your password.")
            return True
        else:
            print("[AuthService] Security answers incorrect. Password recovery failed.")
            return False

    def get_user_by_email(self, email):
        """
        Returns a user object by email, if found.
        """
        return next((user for user in self.users if user.email == email), None)

    def _valid_email_domain(self, email):
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        return any(email.endswith("@" + domain) for domain in allowed_domains)




