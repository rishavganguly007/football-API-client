import re
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
    def validate_player_fields(id, team, league, season, search):
        field_pairs = [
            ("search", ['league', 'team']),
            ("season", ['league', 'season', 'id']),
            ("team", ['season']),
            ("league", ['season']),
            ("id", ['season'])
        ]

        for field, required_fields in field_pairs:
            field_value = locals().get(field, 'None')
            if field_value is not None and all(
                    locals().get(required_field) is None for required_field in required_fields):
                required_field_names = ", ".join(required_fields)
                raise ValueError(f"'{field}' requires at least one of the other fields: {required_field_names}.")



    @staticmethod
    def validate_player_page_field(page, **kwargs):
        if page and all(value is None for value in kwargs.values()):
            raise ValueError("Page requires at least one of the other fields.")

    @staticmethod
    def validate_search_field(search: str):
        if len(search) < 3:
            raise ValueError(" Search field must have at least 3 characters")

    @staticmethod
    def validate_code_field(code: str):
        if len(code) is not 2:
            raise ValueError(" code field must have 2 characters")

    @staticmethod
    def validate_season_field(season: int):
        pattern = r'^\d{4}$'  # Regex pattern for matching "YYYY" format
        if not re.match(pattern, str(season)):
            raise ValueError("Invalid season format. Expected format: YYYY (year).")
