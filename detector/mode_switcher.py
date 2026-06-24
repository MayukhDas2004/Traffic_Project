class ModeSwitcher:

    def select_mode(self, status):

        if status == "HEALTHY":
            return "COOPERATIVE_MARL"

        elif status == "DEGRADED":
            return "DIGITAL_TWIN"

        elif status == "FAILED":
            return "INDEPENDENT_AGENT"

        return "UNKNOWN"