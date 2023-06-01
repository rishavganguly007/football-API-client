import re
import pycountry

class ParameterValidator:
    @staticmethod
    def check_missing_params(*args):
        if all(param is None for param in args):
            return True
        return False

    @staticmethod
    def validate_type_str(val: str, field_name: str):
        if not isinstance(val, str):
            raise TypeError(f"{field_name} must be an string.")

    @staticmethod
    def validate_type_int(val: int, field_name: str):
        if not isinstance(val, int):
            raise TypeError(f"{field_name} must be an integer.")

    @staticmethod
    def validate_player_fields(**kwargs):
        field_pairs = [
            ("search", ['league', 'team']),
            ("season", ['league', 'id']),
            ("team", ['season']),
            ("league", ['season']),
            ("id", ['season']),
            ("page", ['search', 'season', 'team', 'league', 'id'])
        ]

        for field, required_fields in field_pairs:
            field_value = kwargs.get(field)
            if field_value is not None and all(
                    kwargs.get(required_field) is None for required_field in required_fields):
                required_field_names = ", ".join(required_fields)
                raise ValueError(f"'{field}' requires at least one of the other fields: {required_field_names}.")

    @staticmethod
    def validate_search_field(search: str):
        if len(search) < 3:
            raise ValueError(" Search field must have at least 3 characters")

    @staticmethod
    def validate_code_field(code: str):
        if pycountry.countries.get(alpha_2 = code) is None:
            raise LookupError(f"{code} is not a valid country code")

    @staticmethod
    def validate_season_field(season: int):
        pattern = r'^\d{4}$'  # Regex pattern for matching "YYYY" format
        if not re.match(pattern, str(season)):
            raise ValueError("Invalid season format. Expected format: YYYY (year).")
        return


    @staticmethod
    def validate_type_field(field: str):
        allowed_vals = {"league", "cup"}
        if field not in allowed_vals:
            raise ValueError(f"allowed values : league, cup")

        return

    @staticmethod
    def validate_current_field(field: str):
        allowed_vals = {"true", "false"}
        if field not in allowed_vals:
            raise ValueError(f"allowed values : true, false")
        return

    @staticmethod
    def validate_last_field(current: int):
        if len(str(current)) <= 2:
            raise ValueError("The last field cannot exceed 2 characters in length.")
        return

