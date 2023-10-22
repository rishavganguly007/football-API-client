import re
from datetime import datetime
import pycountry

from footballAPIClient._constants import RAPID_API
from footballAPIClient._constants import FOOTBALL_API


class ParameterValidator:

    @staticmethod
    def validate_account_header_type(header: str):
        allowed_accounts = {RAPID_API, FOOTBALL_API}

        if header.lower() not in allowed_accounts:
            raise ValueError(f"allowed account types : 'rapid-api', 'api-sports' ")

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
        if len(search) <= 3:
            raise ValueError(" Search field must have at least 3 characters")

    @staticmethod
    def validate_player_search_field(search):
        if len(search) <= 4:
            raise ValueError(" Search field must have at least 4 characters")

    @staticmethod
    def validate_code_field(code: str):
        if pycountry.countries.get(alpha_2=code) is None:
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
            raise ValueError(f"allowed values in current field are : 'true', 'false'")
        return

    @staticmethod
    def validate_last_field(last: int):
        if len(str(last)) <= 2:
            raise ValueError("The last field cannot exceed 2 characters in length.")
        return

    @staticmethod
    def validate_team_code_field(code):
        if len(code) != 3:
            raise ValueError("Not a valid team code")
        return

    @staticmethod
    def validate_date_field(date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: 'YYYY-MM-DD'.")

    @staticmethod
    def validate_ids_field(ids: str):
        pattern = r'^\d{1,}(?:-\d{1,}){0,19}$'  # pattern to check format: id-id-id up to 20 ids
        if not re.match(pattern, ids):
            raise ValueError(f"not a valid ids format. format: 'id-id-id' with a maximum of 20 ids")

    @staticmethod
    def validate_live_field(live: str):
        pattern1 = r'all$'  # pattern to check "all"
        pattern2 = r'^\d{1,}(?:-\d{1,}){0,19}$'  # pattern to check: "id-id-id"
        print(re.match(pattern1, live))
        if not (re.match(pattern1, live) or re.match(pattern2, live)):
            raise ValueError(f"live has values 'all' or 'id-id-id'")

    @staticmethod
    def validate_next_field(next_: int):
        if len(str(next_)) <= 2:
            raise ValueError("The next field cannot exceed 2 characters in length.")
        return

    @staticmethod
    def validate_status_field(status: str):
        allowed_fixture_status = [
            'TBD',
            'NS',
            '1H',
            'HT',
            '2H',
            'ET',
            'BT',
            'P',
            'SUSP',
            'INT',
            'FT',
            'AET',
            'PEN',
            'PST',
            'CANC',
            'ABD',
            'AWD',
            'WO',
            'LIVE'
        ]
        # pattern to check strings like TBD, TBD-LIVE, etc.
        pattern = r'^({})(?:-({}))*$'.format('|'.join(allowed_fixture_status), '|'.join(allowed_fixture_status))

        if not re.match(pattern, status):
            raise ValueError(f"Incorrect status value provided. ")
        return

    @staticmethod
    def validate_h2h_field(h2h: str):
        pattern = r'^\d{1,}-\d{1,}'  # regex to match the format: id-id

        if not re.match(pattern, h2h):
            raise ValueError(f"Incorrect h2h value.")
        return

    @staticmethod
    def validate_fixture_events_type_field(field: str):
        _allowed_vals = {"goal", "card", "subst"}

        if field.lower() not in _allowed_vals:
            raise ValueError(f"The Type field must be one of: goal, card, subst.")

    @staticmethod
    def validate_fixture_statistics_type_field(field: str):
        _allowed_vals = {
            "shots on goal",
            "shots off goal",
            "shots insidebox",
            "shots outsidebox",
            "total shots",
            "blocked shots",
            "fouls",
            "corner kicks",
            "offsides",
            "ball possession",
            "yellow cards",
            "red cards",
            "goalkeeper saves",
            "total passes",
            "passes accurate",
            "passes %"
        }
        if field.lower() not in _allowed_vals:
            raise ValueError(f" The Type field must be one of: {_allowed_vals}")

    @staticmethod
    def validate_fixture_lineups_type_field(field: str):
        _allowed_vals = {"coach", "formation", "startxi", "substitutes"}

        if field.lower() not in _allowed_vals:
            raise ValueError(f"The Type field must be one of: coach, formation, startxi, substitutes.")

