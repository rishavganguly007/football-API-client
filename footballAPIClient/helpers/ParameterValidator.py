class ParameterValidator:
    @staticmethod
    def check_missing_params(*args):
        if all(param is None for param in args):
            return True
        return False

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
