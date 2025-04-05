class SingletonMeta(type):
    """
    A metaclass for creating Singleton classes.
    Ensures only one instance of a class exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SessionManager(metaclass=SingletonMeta):
    """
    Singleton class to manage the current user session.
    """
    def __init__(self):
        self._current_user = None

    def set_user(self, user):
        self._current_user = user
        print(f"[SessionManager] User '{user.email}' is now logged in.")

    def get_user(self):
        return self._current_user

    def is_authenticated(self):
        return self._current_user is not None

    def logout(self):
        if self._current_user:
            print(f"[SessionManager] User '{self._current_user.email}' has been logged out.")
        self._current_user = None



