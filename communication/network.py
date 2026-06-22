class CommunicationNetwork:

    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        msgs = self.messages.copy()
        self.messages.clear()
        return msgs