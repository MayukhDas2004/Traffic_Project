class FailureDetector:

    def detect(self,
               packet_lost=False,
               delayed=False):

        if packet_lost:
            return "FAILED"

        if delayed:
            return "DEGRADED"

        return "HEALTHY"