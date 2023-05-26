class ParameterValidator:
    @staticmethod
    def check_missing_params(params):
        missing_params = [param_name for param_name, param_value in params.items() if param_value is None]
        if all(param is None for param in params.values()):
            return True
        return False
