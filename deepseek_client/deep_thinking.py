class DeepThinking:
    def __init__(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def is_enabled(self):
        return self.enabled 