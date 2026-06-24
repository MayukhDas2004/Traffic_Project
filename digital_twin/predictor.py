class DigitalTwinPredictor:

    def predict_queue(self, current, previous):

        trend = current - previous

        prediction = current + trend

        prediction *= 1.10

        return max(
            0,
            min(prediction, 2.0)
        )