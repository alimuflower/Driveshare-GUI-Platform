
class MessagingService:
    def __init__(self):
        self.messages = {}

    def send_message(self, guest_email, host_email, content):
        if host_email not in self.messages:
            self.messages[host_email] = []
        self.messages[host_email].append((guest_email, content))

    def get_messages_for_host(self, host_email):
        return self.messages.get(host_email, [])
