class FailedLoginException(Exception):
    def __init__(self, message: str):
        self.message = message


class DuplicateReceiverEmailException(Exception):
    def __init__(self, message: str):
        self.message = message
