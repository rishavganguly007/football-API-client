import http.client
import requests

from footballAPIClient.Exceptions.MissingParametersError import MissingParametersError
from footballAPIClient.helpers.ParameterValidator import ParameterValidator


class FootballAPI:
    def __init__(self,
                 api_key: str = None):
        self.parameter_validator = ParameterValidator()
        self.base_url: str = "http://v3.football.api-sports.io"
        self.api_key = api_key

    def get_headers(self):
        headers = {}
        if self.api_key:
            headers['x-apisports-key'] = self.api_key
            return headers

    def _send_requests(self, method, url, headers, params=None, data=None):

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            # return response.json # use this
            return response.text  # delete lter
        except requests.exceptions.RequestException as e:
            # Handle request exceptions or errors
            print(f"Request error: {e}")
            return None

    def _get(self, path: str, id: str = None,
             name: str = None,
             country: str = None,
             code: str = None,
             season: int = None,
             team: int = None,
             type: str = None,
             current: str = None,
             search: str = None,
             last: str = None,
             league: int = None,
             venue: str = None,
             date: str = None,
             city: str = None,
             ids: str = None,
             live: str = None,
             next_: int = None,
             from_: str = None,
             to: str = None,
             round_: str = None,
             status: str = None,
             timezone: str = None,
             h2h: str = None,
             fixture: int = None,
             player: int = None,
             page: int = None,
             coach: int = None,
             bet: int = None
             ):
        url = f"{self.base_url}/{path}"
        headers = self.get_headers()

        # preparing the query parameter
        params = {}
        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if code:
            params["code"] = code
        if search:
            params["search"] = search
        if season:
            params['season'] = season
        if team:
            params['team'] = team
        if type:
            params['type'] = type
        if current:
            params['current'] = current
        if search:
            params['search'] = search
        if last:
            params['last'] = last
        if league:
            params['league'] = league
        if venue:
            params["venue"] = venue
        if date:
            params["date"] = date
        if country:
            params['country'] = country
        if city:
            params['city'] = city
        if ids:
            params["ids"] = ids

        if live:
            params["live"] = live

        if next_:
            params["next"] = next_

        if from_:
            params["from"] = from_

        if to:
            params["to"] = to

        if round_:
            params["round"] = round_

        if status:
            params["status"] = status

        if timezone:
            params["timezone"] = timezone

        if h2h:
            params["h2h"] = h2h

        if fixture:
            params["fixture"] = fixture

        if player:
            params["player"] = player

        if page:
            params["page"] = page

        if coach:
            params["coach"] = coach

        if bet:
            params["bet"] = bet

        response_data = self._send_requests('GET', url, headers, params=params)
        return response_data

    def get_countries(self, name: str = None, code: str = None, search: str = None):

        return self._get("countries", name, code, search)

    def get_timezone(self, name: str = None, code: str = None, search: str = None):
        # might need to add exceptions
        return self._get("timezone")

    def get_leagues(self, id: int = None,
                    name: str = None,
                    country: str = None,
                    code: str = None,
                    season: str = None,
                    team: str = None,
                    type: str = None,
                    current: str = None,
                    search: str = None,
                    last: str = None):
        # SEARCH: criteria is >= 3 words
        return self._get("leagues", id, name, country, code, season, team, type, current, search, last)

    def get_leagues_seasons(self):
        # TO-DO: only send the Responses
        return self._get("leagues/seasons")

    def get_teams_information(self, id: int = None,
                              name: str = None,
                              league: int = None,
                              season: int = None,
                              country: str = None,
                              code: str = None,
                              venue: str = None,
                              search: str = None):

        missing_params = self.parameter_validator.check_missing_params(id, name, league, season,
                                                                       country, code,
                                                                       venue, search)
        # checks if it has at least one params
        if missing_params:
            raise MissingParametersError("At least one of the optional parameters is required.")

        return self._get(path="teams", id=id, name=name, league=league, country=country,
                         season=season, code=code, venue=venue,
                         search=search
                         )

    def team_statistics(self, league: int,
                        season: int,
                        team: int,
                        date: str):
        """
        TO-DO:  date should be of format: 'YYYY-MM-DD'
                season of 4 character, 'YYYY'
        -- create a helper dir to handle all this things
        """
        return self._get('teams/statistics', league=league, season=season, team=team, date=date)

    def get_teams_seasons(self, team: int):
        return self._get('teams/seasons', team=team)

    def get_teams_country(self):
        return self._get('teams/countries')

    def get_venues(self,
                   id: int = None,
                   name: str = None,
                   city: str = None,
                   country: str = None,
                   search: str = None):

        missing_params = self.parameter_validator.check_missing_params(id, name, city, country,
                                                                       search)

        if missing_params:
            raise MissingParametersError("At least one of the optional parameters is required.")

        return self._get('venues',
                         id=id,
                         name=name,
                         city=city,
                         country=country,
                         search=search)

    def get_standings(self,
                      season: int,
                      league: int = None,
                      team: str = None):
        return self._get('standings',
                         league=league,
                         season=season,
                         team=team)

    def get_fixtures(self,
                     id: str = None,
                     ids: str = None,  # validate: stringsMaximum of 20 fixtures ids, Value: "id-id-id"
                     live: str = None,  # Enum: "all" "id-id"
                     date: str = None,  # YYYY-MM-DD
                     league: int = None,
                     season: int = None,  # int YYYY
                     team: int = None,
                     last: int = None,  # <= 2 chars
                     next_: int = None,  # <= 2 characters
                     from_: str = None,  # stringYYYY-MM-DD
                     to: str = None,  # stringYYYY-MM-DD
                     round_: str = None,
                     status: str = None,  # Enum: "NS" "NS-PST-FT"
                     venue: str = None,
                     timezone: str = None):

        return self._get('fixtures',
                         id=id,
                         ids=ids,
                         live=live,
                         date=date,
                         league=league,
                         season=season,
                         team=team,
                         last=last,
                         next_=next_,
                         from_=from_,
                         to=to,
                         round_=round_,
                         status=status,
                         venue=venue,
                         timezone=timezone
                         )

    def get_rounds(self,
                   league: int,
                   season: int,
                   current: str  # Enum: "true" "false"
                   ):

        return self._get('fixtures/rounds',
                         league=league,
                         season=season,
                         current=current)

    def get_head_to_head(self,
                         h2h: str,  # format: id-id
                         date: str = None,
                         league: int = None,
                         season: int = None,  # format: 4 chars- YYYY
                         last: int = None,
                         next_: int = None,
                         from_: str = None,  # format: YYYY-MM-DD
                         to: str = None,  # format: YYYY-MM-DD
                         venue: int = None,
                         timezone: str = None):
        return self._get('fixtures/headtohead',
                         h2h=h2h,
                         date=date,
                         league=league,
                         season=season,
                         last=last,
                         next_=next_,
                         from_=from_,
                         to=to,
                         venue=venue,
                         timezone=timezone)

    def get_fixture_statistics(self,
                               fixture: int,
                               team: int = None,
                               type: str = None):

        return self._get('fixtures/statistics',
                         fixture=fixture,
                         team=team,
                         type=type)

    def get_fixture_events(self,
                           fixture: int,
                           team: int = None,
                           player: int = None,
                           type: str = None):

        return self._get('fixtures/events',
                         fixture=fixture,
                         team=team,
                         player=player,
                         type=type)

    def get_fixture_lineups(self,
                            fixture: int,
                            team: int = None,
                            player: int = None,
                            type: str = None):

        return self._get('fixtures/lineups',
                         fixture=fixture,
                         team=team,
                         player=player,
                         type=type)

    def get_fixture_player_statistics(self,
                                      fixture: int,
                                      team: int = None):

        return self._get('fixtures/players',
                         fixture=fixture,
                         team=team)

    def get_injuries(self,
                     league: int = None,
                     season: int = None,  # format: 4 chars- YYYY
                     fixture: int = None,
                     team: int = None,
                     player: int = None,
                     date: str = None,
                     timezone: str = None):
        params = {
            'league': league, 'season': season, 'fixture': fixture,
            'team': team, 'player': player, 'date': date, 'timezone': timezone
        }
        missing_params = self.parameter_validator.check_missing_params(league, season, fixture,
                                                                       team, player, date, timezone)

        if missing_params:
            raise MissingParametersError("At least one of the optional parameters is required.")

        return self._get('injuries',
                         league=league,
                         season=season,
                         fixture=fixture,
                         team=team,
                         player=player,
                         date=date,
                         timezone=timezone)

    def get_predictions(self, fixture: int):
        return self._get('predictions', fixture=fixture)

    def get_coachs(self,
                   id: int = None,
                   team: int = None,
                   search: int = None  # chars >= 3
                   ):

        missing_params = self.parameter_validator.check_missing_params(id, search, team)
        # checks if it has at least one params
        if missing_params:
            raise MissingParametersError("At least one of the optional parameters is required.")

        return self._get('coachs', id=id, search=search, team=team)

    def get_player_seasons(self, player: int = None):

        return self._get('players/seasons', player=player)

    def get_player(self,
                   id: int = None,
                   team: int = None,
                   league: int = None,
                   season: int = None,
                   search: str = None,
                   page: int = 1
                   ):
        try:
            self.parameter_validator.check_missing_params(id, team, league, season, search)
            self.parameter_validator.validate_player_fields(id, team, league, season, search)
            self.parameter_validator.validate_player_page_field(page=page, id=id, team=team, league=league,
                                                                season=season, search=search)
            return self._get('players',
                             id=id,
                             team=team,
                             league=league,
                             search=search,
                             season=season,
                             page=page)
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            raise

    def get_players_squads(self, team, player):
        try:
            missing_para = self.parameter_validator.check_missing_params(team, player)
            if missing_para:
                raise MissingParametersError()
            return self._get('players/squads', team=team, player=player)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_player_top_scorers(self, league: int,
                               season: int  # validate: YYYY
                               ):

        return self._get('players/topscorers', league=league, season=season)

    def get_player_top_assist(self, league: int,
                              season: int  # validate: YYYY
                              ):

        return self._get('players/topassists', league=league, season=season)

    def get_player_top_yellow_cards(self, league: int,
                                    season: int  # validate: YYYY
                                    ):
        return self._get('players/topyellowcards', league=league, season=season)

    def get_player_top_red_cards(self, league: int,
                                 season: int  # validate: YYYY
                                 ):
        return self._get('players/topredcards', league=league, season=season)

    def get_transfers(self, player: int = None, team: int = None):

        try:
            missing_para = self.parameter_validator.check_missing_params(team, player)
            if missing_para:
                raise MissingParametersError()
            return self._get('transfers', team=team, player=player)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_trophies(self, player: int = None, coach: int = None):

        try:
            missing_para = self.parameter_validator.check_missing_params(player, coach)
            if missing_para:
                raise MissingParametersError()
            return self._get('trophies', player=player, coach=coach)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_sidelined(self, player: int = None, coach: int = None):

        try:
            missing_para = self.parameter_validator.check_missing_params(player, coach)
            if missing_para:
                raise MissingParametersError()
            return self._get('sidelined', player=player, coach=coach)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_in_play_odds(self, fixture: int = None, league: int = None, bet: int = None):
        try:
            missing_para = self.parameter_validator.check_missing_params(fixture, league, bet)
            if missing_para:
                raise MissingParametersError()
            return self._get('odds/live', fixture=fixture, league=league, bet=bet)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_all_bets_in_play(self, id: str = None, search: str = None):
        try:
            missing_para = self.parameter_validator.check_missing_params(id, search)
            if missing_para:
                raise MissingParametersError()
            return self._get('odds/bets', id=id, search=search)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise


