class MissingParametersError(Exception):
    def __init__(self, message="At least one of the optional parameters is required.", params=None):
        super().__init__(message)
        self.params = params

    def __str__(self):
        error_message = super().__str__()
        if self.params:
            error_message += f"\nParameters: {', '.join(self.params)}"
        return error_message