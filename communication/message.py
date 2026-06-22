class TrafficMessage:
    def __init__(self, sender, queue_length,
                 vehicle_count, phase):

        self.sender = sender
        self.queue_length = queue_length
        self.vehicle_count = vehicle_count
        self.phase = phase

    def __str__(self):
        return (
            f"Sender={self.sender}, "
            f"Queue={self.queue_length}, "
            f"Vehicles={self.vehicle_count}, "
            f"Phase={self.phase}"
        )