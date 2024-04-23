class TheaterError(ValueError):
    def __init__(self, message: str, details: list[str]):
        super().__init__(message)
        self.details = details
