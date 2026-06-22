import random


class FailureInjector:

    def __init__(self,
                 packet_loss=0.0,
                 delay_probability=0.0):

        self.packet_loss = packet_loss
        self.delay_probability = delay_probability

    def transmit(self, message):

        # Packet loss
        if random.random() < self.packet_loss:
            return None

        # Delay
        if random.random() < self.delay_probability:
            print("DELAYED:", message)

        return message