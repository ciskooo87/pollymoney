class BaseStrategy:
    name = "base"

    def generate_signals(self):
        raise NotImplementedError
