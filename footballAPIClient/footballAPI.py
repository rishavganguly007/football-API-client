import os
from http.client import HTTPException

import requests
import logging

from footballAPIClient.Exceptions.MissingParametersError import MissingParametersError
from footballAPIClient.Exceptions.ApiKeyMissingError import ApiKeyMissingError
from footballAPIClient.helpers.ParameterValidator import ParameterValidator
from footballAPIClient.Exceptions.APILimitExceededError import APILimitExceededError
from footballAPIClient._constants import RAPID_API, FOOTBALL_API, FOOTBALL_API_URI, RAPID_API_URI


class FootballAPI:
    """
    Python Binding (API wrapper) for the Football API. (https://www.api-football.com/documentation-v3)
    You can use our API client to access all API endpoints, which can get information about Football Leagues & Cups.
    """

    def __init__(self,
                 account_type: str,
                 api_key: str = None
                 ):

        """

        :param account_type: Indicates weather the account is used from Rapid-API or from dashboard.
        it consists of values: rapid-api, and api-sports
        :param api_key: It uses API keys to allow access to the API. You can register a new API
        key in rapidapi or directly on the dashboard.

        """

        self._logger = logging.getLogger(__name__)
        self._parameter_validator = ParameterValidator()
        self._api_key = api_key
        self._max_credit = None
        self._available_credit = None
        try:
            self._parameter_validator.validate_account_header_type(account_type)
            self.account_type = account_type
            if self.account_type.lower() == RAPID_API:
                self._base_url = RAPID_API_URI
            elif self.account_type.lower() == FOOTBALL_API:
                self._base_url: str = FOOTBALL_API_URI

            if self._api_key is None:
                self._api_key = os.environ["API_KEY"]

            self._update_credit()
        except Exception as e:
            if isinstance(e, KeyError):
                raise ApiKeyMissingError("No API_KEY set as environment variable or provided.")
            else:
                raise

    def _update_credit(self):
        self._logger.info("Updating credits")
        data = self.get_status()
        self._max_credit = data["response"]["requests"]["limit_day"]
        current_used_credit = data["response"]["requests"]["current"] + 1  # as a fail-safe situation added 1
        self._available_credit = self._max_credit - current_used_credit
        self._logger.info(f"{self._available_credit} credit(s) available.")

    def _get_headers(self):
        headers = {}

        if self.account_type.lower() == RAPID_API:
            headers['x-apisports-host'] = "v3.football.api-sports.io"
            headers['x-apisports-key'] = self._api_key

        elif self.account_type.lower() == FOOTBALL_API:
            headers['x-apisports-key'] = self._api_key
        return headers

    @property
    def max_credits(self):
        return self._max_credit

    @property
    def available_credits(self):
        return self._available_credit

    def _send_requests(self, method, url, headers, params=None, data=None):

        try:

            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=data
            )
            status_code = response.status_code
            self._logger.log(level=logging.INFO, msg="Request Successful: {}".format(status_code))
            if response.status_code != 200:
                raise HTTPException(response.status_code, response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle request exceptions or errors
            print(f"Request error: {e}")
            return None

    def _get(self, path: str, id: int = None,
             name: str = None,
             country: str = None,
             code: str = None,
             season: int = None,
             team: int = None,
             type: str = None,
             current: str = None,
             search: str = None,
             last: int = None,
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
        url = f"{self._base_url}/{path}"
        headers = self._get_headers()

        try:
            # preparing the query parameter
            params = {}
            if id:
                self._parameter_validator.validate_type_int(id, "id")
                params["id"] = id
            if name:
                self._parameter_validator.validate_type_str(name, 'name')
                params["name"] = name
            if code:
                self._parameter_validator.validate_type_str(code, "code")
                params["code"] = code
            if search:
                self._parameter_validator.validate_type_str(search, "search")
                params["search"] = search
            if season:
                self._parameter_validator.validate_type_int(season, "season")
                params['season'] = season
            if team:
                self._parameter_validator.validate_type_int(team, "team")
                params['team'] = team
            if type:
                self._parameter_validator.validate_type_str(type, "type")
                params['type'] = type
            if current:
                self._parameter_validator.validate_type_str(current, "current")
                params['current'] = current
            if last:
                self._parameter_validator.validate_type_int(last, "last")
                params['last'] = last
            if league:
                self._parameter_validator.validate_type_int(league, "league")
                params['league'] = league
            if venue:
                self._parameter_validator.validate_type_str(venue, "venue")
                params["venue"] = venue
            if date:
                self._parameter_validator.validate_type_str(date, "date")
                params["date"] = date
            if country:
                self._parameter_validator.validate_type_str(country, "country")
                params['country'] = country
            if city:
                self._parameter_validator.validate_type_str(city, "city")
                params['city'] = city
            if ids:
                self._parameter_validator.validate_type_str(ids, "ids")
                params["ids"] = ids
            if live:
                self._parameter_validator.validate_type_str(live, "live")
                params["live"] = live
            if next_:
                self._parameter_validator.validate_type_int(next_, "next")
                params["next"] = next_

            if from_:
                self._parameter_validator.validate_type_str(from_, "from")
                params["from"] = from_

            if to:
                self._parameter_validator.validate_type_str(to, "to")
                params["to"] = to

            if round_:
                self._parameter_validator.validate_type_str(round_, "round")
                params["round"] = round_

            if status:
                self._parameter_validator.validate_type_str(status, "status`")
                params["status"] = status

            if timezone:
                self._parameter_validator.validate_type_str(timezone, "timezone")
                params["timezone"] = timezone

            if h2h:
                self._parameter_validator.validate_type_str(h2h, "h2h")
                params["h2h"] = h2h

            if fixture:
                self._parameter_validator.validate_type_int(fixture, "fixture")
                params["fixture"] = fixture

            if player:
                self._parameter_validator.validate_type_int(player, "player")
                params["player"] = player

            if page:
                self._parameter_validator.validate_type_int(page, "page")
                params["page"] = page

            if coach:
                self._parameter_validator.validate_type_int(coach, "coach")
                params["coach"] = coach

            if bet:
                self._parameter_validator.validate_type_int(bet, "bet")
                params["bet"] = bet

            if path == 'status':
                response_data = self._send_requests('GET', url, headers, params=params)
                return response_data

            if self._available_credit <= 0:
                self._logger.info(f"API limit exceed the daily quota of {self._max_credit}. Please try next "
                                  f"day.")
                raise APILimitExceededError(f"API limit exceed the daily quota of {self._max_credit}. Please try next "
                                            f"day.")

            response_data = self._send_requests('GET', url, headers, params=params)
            self._update_credit()
            return response_data
        except Exception as e:
            raise

    def get_status(self):
        """
        It allows you to:
        - To follow your consumption in real time
        - Check the status of our servers
        Note: This call does not count against the daily quota.
        :return: Returns the status json schema
        """
        return self._get('status')

    def get_countries(self, name: str = None, code: str = None, search: str = None):
        """
        Get the list of available countries for the leagues endpoint.

        :param name: The name of the country
        :param code: The Alpha2 code of the country
        :param search: The name of the country
        :return: Returns the Country json schema
        """
        try:
            if search:
                self._parameter_validator.validate_search_field(search)
            if code:
                self._parameter_validator.validate_code_field(code)
            return self._get("countries", name=name, code=code, search=search)
        except Exception as e:
            raise

    def get_timezone(self):
        """
        Get the list of available timezone to be used in the fixtures endpoint.

        :return: Returns the timezone json schema
        """
        try:
            return self._get("timezone")
        except Exception as e:
            raise

    def get_leagues(self, id: int = None,
                    name: str = None,
                    country: str = None,
                    code: str = None,
                    season: int = None,
                    team: str = None,
                    type: str = None,
                    current: str = None,
                    search: str = None,
                    last: int = None):

        """
        Get the list of available leagues and cups.

        :param id: The id of the league
        :param name: The name of the league
        :param country: The country name of the league
        :param code: The Alpha2 code of the country
        :param season: The season of the league
        :param team: The id of the team
        :param type: The type of the league. Enum: "league" "cup"
        :param current: The state of the league. Enum: "true" "false"
        :param search: The name or the country of the league
        :param last: The X last leagues/cups added in the API
        :return: Returns the Leagues json schema
        """

        try:
            if code:
                self._parameter_validator.validate_code_field(code)

            if search:
                self._parameter_validator.validate_search_field(search)
            if season:
                self._parameter_validator.validate_season_field(season)
            if type:
                self._parameter_validator.validate_type_field(type)
            if current:
                self._parameter_validator.validate_current_field(current)
            if last:
                self._parameter_validator.validate_last_field(last)
            return self._get("leagues", id=id, name=name, country=country, code=code,
                             season=season, team=team, type=type, current=current,
                             search=search, last=last)

        except Exception as e:
            raise

    def get_leagues_seasons(self):

        """
        Get the list of available seasons.
        :return: Returns Season json schema
        """

        return self._get("leagues/seasons")

    def get_teams_information(self, id: int = None,
                              name: str = None,
                              league: int = None,
                              season: int = None,
                              country: str = None,
                              code: str = None,
                              venue: str = None,
                              search: str = None):

        """
        Get the list of available teams.

        :param id: The id of the team
        :param name: The name of the team
        :param league: The id of the league
        :param season: The season of the league
        :param country: The country name of the team
        :param code: The code of the team
        :param venue: The id of the venue
        :param search: The name or the country name of the team
        :return: Returns the Teams json schema
        """

        try:
            if season:
                self._parameter_validator.validate_season_field(season)
            if search:
                self._parameter_validator.validate_search_field(search)
            if code:
                self._parameter_validator.validate_team_code_field(code)
            missing_params = self._parameter_validator.check_missing_params(id, name, league, season,
                                                                            country, code,
                                                                            venue, search)
            # checks if it has at least one params
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            return self._get(path="teams", id=id, name=name, league=league, country=country,
                             season=season, code=code, venue=venue,
                             search=search
                             )
        except Exception as e:
            raise

    def get_team_statistics(self, league: int,
                            season: int,
                            team: int,
                            date: str = None):

        """
        Returns the statistics of a team in relation to a given competition and season.

        :param league: The id of the league
        :param season: The season of the league
        :param team: The id of the team
        :param date: The limit date
        :return: Returns Team statistics json schema
        """

        try:
            if season:
                self._parameter_validator.validate_season_field(season)
            if date:
                self._parameter_validator.validate_date_field(date)

            return self._get('teams/statistics', league=league, season=season, team=team, date=date)
        except Exception as e:
            raise

    def get_teams_seasons(self, team: int):

        """
        Get the list of seasons available for a team.

        :param team: The id of the team
        :return: Returns teams seasons json schema
        """

        return self._get('teams/seasons', team=team)

    def get_teams_country(self):

        """
        Get the list of countries available for the teams endpoint.

        :return: Returns team countries json schema
        """

        return self._get('teams/countries')

    def get_venues(self,
                   id: int = None,
                   name: str = None,
                   city: str = None,
                   country: str = None,
                   search: str = None):

        """
        Get the list of available venues.

        :param id: The id of the venue
        :param name: The name of the venue
        :param city: The city of the venue
        :param country: The country name of the venue
        :param search: The name, city or the country of the venue
        :return: Returns Venue json schema
        """

        try:
            if search:
                self._parameter_validator.validate_search_field(search)

            missing_params = self._parameter_validator.check_missing_params(id, name, city, country,
                                                                            search)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            return self._get('venues',
                             id=id,
                             name=name,
                             city=city,
                             country=country,
                             search=search)
        except Exception as e:
            raise

    def get_standings(self,
                      season: int,
                      league: int = None,
                      team: str = None):

        """
        Get the standings for a league or a team.

        :param season: The season of the league
        :param league: The id of the league
        :param team: The id of the team
        :return: Returns the standings json schema
        """

        try:
            if season:
                self._parameter_validator.validate_season_field(season)
            missing_params = self._parameter_validator.check_missing_params(league, team)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            return self._get('standings',
                             league=league,
                             season=season,
                             team=team)
        except Exception as e:
            raise

    def get_fixtures(self,
                     id: int = None,
                     ids: str = None,
                     live: str = None,
                     date: str = None,
                     league: int = None,
                     season: int = None,
                     team: int = None,
                     last: int = None,
                     next_: int = None,
                     from_: str = None,
                     to: str = None,
                     round_: str = None,
                     status: str = None,
                     venue: str = None,
                     timezone: str = None):

        """
        Get the fixtures of league or cup.

        :param id: The id of the fixture
        :param ids: One or more fixture ids. Value: "id-id-id" up to 20 ids
        :param live: All or several leagues ids. Enum: "all" "id-id"
        :param date: A valid date
        :param league: The id of the league
        :param season: The season of the league
        :param team: The id of the team
        :param last: For the X last fixtures
        :param next_: For the X next fixtures
        :param from_: A valid date
        :param to: A valid date
        :param round_: The round of the fixture
        :param status: One or more fixture status short. Enum: "NS" "NS-PST-FT".
        :param venue: The venue id of the fixture
        :param timezone: A valid timezone from the endpoint Timezone
        :return: Returns fixture json schema
        """

        try:
            missing_params = self._parameter_validator.check_missing_params(id, ids, live, date, league, season,
                                                                            team, last, next_, from_,
                                                                            to, round_, status, venue,
                                                                            timezone)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            if id and not self._parameter_validator.check_missing_params(ids, season, live, date, league,
                                                                         team, last, next_, from_,
                                                                         to, round_, status, venue,
                                                                         timezone):
                raise MissingParametersError("The id field must be used alone.")

            if ids:
                self._parameter_validator.validate_ids_field(ids)

            if ids and not self._parameter_validator.check_missing_params(id, season, live, date, league,
                                                                          team, last, next_, from_,
                                                                          to, round_, status, venue,
                                                                          timezone):
                raise MissingParametersError("The ids field must be used alone.")

            if live:
                self._parameter_validator.validate_live_field(live)
            if date:
                self._parameter_validator.validate_date_field(date)
            if season:
                self._parameter_validator.validate_season_field(season)
            if season and self._parameter_validator.check_missing_params(live, date, league,
                                                                         team, last, next_, from_,
                                                                         to, round_, status, venue,
                                                                         timezone):
                raise MissingParametersError("The Season field need another parameter other than id ans ids. ")
            if last:
                self._parameter_validator.validate_last_field(last)
            if next_:
                self._parameter_validator.validate_next_field(next_)
            if from_:
                self._parameter_validator.validate_date_field(from_)
            if to:
                self._parameter_validator.validate_date_field(to)
            if status:
                self._parameter_validator.validate_status_field(status)

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
        except Exception as e:
            raise

    def get_rounds(self,
                   league: int,
                   season: int,
                   current: str
                   ):
        """
        Get the rounds for a league or a cup.

        :param league: The id of the league
        :param season: The season of the league
        :param current: The current round only. Enum: "true" "false"
        :return: Returns Round json schema
        """
        try:
            self._parameter_validator.validate_season_field(season)
            if current:
                self._parameter_validator.validate_current_field(current)
            return self._get('fixtures/rounds',
                             league=league,
                             season=season,
                             current=current)
        except Exception as e:
            raise

    def get_head_to_head(self,
                         h2h: str,  # format: id-id
                         date: str = None,
                         league: int = None,
                         season: int = None,
                         last: int = None,
                         next_: int = None,
                         from_: str = None,
                         to: str = None,
                         venue: int = None,
                         status: str = None,
                         timezone: str = None):

        """
        Get heads to heads between two teams.

        :param h2h: The ids of the teams. Value id-id
        :param date: a valid date
        :param league: The id of the league
        :param season: The season of the league
        :param last: For the X last fixtures
        :param next_: For the X next fixtures
        :param from_: a valid date
        :param to: a valid date
        :param venue: The venue id of the fixture
        :param status: One or more fixture status short. Enum: "NS" "NS-PST-FT"
        :param timezone: A valid timezone from the endpoint Timezone
        :return: Returns Head to head json schema
        """

        try:
            self._parameter_validator.validate_h2h_field(h2h)
            if season:
                self._parameter_validator.validate_season_field(season)
            if from_:
                self._parameter_validator.validate_date_field(from_)
            if to:
                self._parameter_validator.validate_date_field(to)
            if status:
                self._parameter_validator.validate_status_field(status)
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
                             status=status,
                             timezone=timezone)
        except Exception as e:
            raise

    def get_fixture_statistics(self,
                               fixture: int,
                               team: int = None,
                               type: str = None):

        """
        Get the statistics for one fixture.

        :param fixture:
        :param team:
        :param type:
        :return: Returns statistics json schema
        """

        return self._get('fixtures/statistics',
                         fixture=fixture,
                         team=team,
                         type=type)

    def get_fixture_events(self,
                           fixture: int,
                           team: int = None,
                           player: int = None,
                           type: str = None):

        """
        Get the events from a fixture.

        :param fixture: The id of the fixture
        :param team: The id of the team
        :param player: The id of the player
        :param type: The type
        :return: Returns event fixture json schema
        """

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

        """
        Get the lineups for a fixture.

        :param fixture: The id of the fixture
        :param team: The id of the team
        :param player: The id of the player
        :param type: The type
        :return: Returns lineups json schema
        """

        return self._get('fixtures/lineups',
                         fixture=fixture,
                         team=team,
                         player=player,
                         type=type)

    def get_fixture_player_statistics(self,
                                      fixture: int,
                                      team: int = None):

        """
        Get the players statistics from one fixture.

        :param fixture: The id of the fixture
        :param team: The id of the team
        :return: Returns fixture player statistics json schema
        """

        return self._get('fixtures/players',
                         fixture=fixture,
                         team=team)

    def get_injuries(self,
                     league: int = None,
                     season: int = None,
                     fixture: int = None,
                     team: int = None,
                     player: int = None,
                     date: str = None,
                     timezone: str = None):

        """
        Get the list of players not participating in the fixtures

        :param league: The id of the league
        :param season: The season of the league, required with league, team and player parameters
        :param fixture: The id of the fixture
        :param team: The id of the team
        :param player: The id of the player
        :param date: A valid date
        :param timezone: A valid timezone from the endpoint Timezone
        :return: Returns injury json schema
        """

        try:
            missing_params = self._parameter_validator.check_missing_params(league, season, fixture,
                                                                            team, player, date, timezone)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            if season:
                self._parameter_validator.validate_season_field(season)
            if date:
                self._parameter_validator.validate_date_field(date)
            return self._get('injuries',
                             league=league,
                             season=season,
                             fixture=fixture,
                             team=team,
                             player=player,
                             date=date,
                             timezone=timezone)
        except Exception as e:
            raise

    def get_predictions(self, fixture: int):

        """
        Get predictions about a fixture

        :param fixture: The id of the fixture
        :return: Returns the prediction json schema
        """

        return self._get('predictions', fixture=fixture)

    def get_coachs(self,
                   id: int = None,
                   team: int = None,
                   search: str = None
                   ):

        """
        Get all the information about the coachs and their careers.

        :param id: The id of the coach
        :param team: The id of the team
        :param search: The name of the coach
        :return: Returns coach json schema
        """

        try:
            missing_params = self._parameter_validator.check_missing_params(id, search, team)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            if search:
                self._parameter_validator.validate_search_field(search)

            return self._get('coachs', id=id, search=search, team=team)
        except Exception as e:
            raise

    def get_player_seasons(self, player: int = None):

        """
        Get all available seasons for players statistics.

        :param player: The id of the player
        :return: Returns Player season json schema
        """

        try:
            return self._get('players/seasons', player=player)
        except Exception as e:
            raise

    def get_player(self,
                   id: int = None,
                   team: int = None,
                   league: int = None,
                   season: int = None,
                   search: str = None,
                   page: int = 1
                   ):

        """
        Get players statistics.

        :param id: The id of the player
        :param team: The id of the team
        :param league: The id of the league
        :param season: The season of the league
        :param search: The name of the player
        :param page: Use for the pagination. Default: 1
        :return: Returns player json schema
        """

        try:
            self._parameter_validator.check_missing_params(id, team, league, season, search)
            self._parameter_validator.validate_player_fields(id=id, team=team, league=league, season=season,
                                                             search=search, page=page)
            if season:
                self._parameter_validator.validate_season_field(season)
            if search:
                self._parameter_validator.validate_player_search_field(search)
            return self._get('players',
                             id=id,
                             team=team,
                             league=league,
                             search=search,
                             season=season,
                             page=page)

        except Exception as e:
            if e == ValueError:
                print(f"Validation error: {str(e)}")
            raise

    def get_players_squads(self, team, player):

        """
        Return the current squad of a team when the team parameter is used.
        When the player parameter is used the endpoint returns the set of teams associated with the player.

        :param team: The id of the team
        :param player: The id of the player
        :return: Returns players squads json schema
        """

        try:
            missing_para = self._parameter_validator.check_missing_params(team, player)
            if missing_para:
                raise MissingParametersError()
            return self._get('players/squads', team=team, player=player)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_player_top_scorers(self, league: int,
                               season: int  # validate: YYYY
                               ):

        """
        Get the 20 best players for a league or cup.

        :param league: The id of the league
        :param season: The season of the league
        :return: Returns top scorers json schema
        """

        try:
            self._parameter_validator.validate_season_field(season)
            return self._get('players/topscorers', league=league, season=season)
        except Exception as e:
            raise

    def get_player_top_assist(self, league: int,
                              season: int
                              ):

        """
        Get the 20 best players assists for a league or cup.

        :param league: The id of the league
        :param season: The season of the league
        :return: Returns player assists json schema
        """

        try:
            self._parameter_validator.validate_season_field(season)
            return self._get('players/topassists', league=league, season=season)
        except Exception as e:
            raise

    def get_player_top_yellow_cards(self, league: int,
                                    season: int
                                    ):

        """
        Get the 20 players with the most yellow cards for a league or cup.

        :param league: The id of the league
        :param season: The season of the league
        :return: Returns player yellow card json schema
        """

        try:
            self._parameter_validator.validate_season_field(season)
            return self._get('players/topyellowcards', league=league, season=season)
        except Exception as e:
            raise

    def get_player_top_red_cards(self, league: int,
                                 season: int
                                 ):

        """
        Get the 20 players with the most red cards for a league or cup.

        :param league: The id of the league
        :param season: The season of the league
        :return: Returns player red card json schema
        """

        try:
            self._parameter_validator.validate_season_field(season)
            return self._get('players/topredcards', league=league, season=season)
        except Exception as e:
            raise

    def get_transfers(self, player: int = None, team: int = None):

        """
        Get all available transfers for players and teams

        :param player: The id of the player
        :param team: The id of the team
        :return: Returns transfers json schema
        """

        try:
            missing_para = self._parameter_validator.check_missing_params(team, player)
            if missing_para:
                raise MissingParametersError()
            return self._get('transfers', team=team, player=player)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_trophies(self, player: int = None, coach: int = None):

        """
        Get all available trophies for a player or a coach.

        :param player: The id of the player
        :param coach: The id of the coach
        :return: Returns trophies json schema
        """

        try:
            missing_para = self._parameter_validator.check_missing_params(player, coach)
            if missing_para:
                raise MissingParametersError()
            return self._get('trophies', player=player, coach=coach)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_sidelined(self, player: int = None, coach: int = None):

        """
        Get all available sidelined for a player or a coach.

        :param player: The id of the player
        :param coach: The id of the coach
        :return: Returns sidelined json schema
        """

        try:
            missing_para = self._parameter_validator.check_missing_params(player, coach)
            if missing_para:
                raise MissingParametersError()
            return self._get('sidelined', player=player, coach=coach)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_in_play_odds(self, fixture: int = None, league: int = None, bet: int = None):

        """
        This endpoint returns in-play odds for fixtures in progress.

        :param fixture: The id of the fixture
        :param league: The id of the league
        :param bet: The id of the bet
        :return: Returns in-play odd json schema
        """

        try:
            missing_para = self._parameter_validator.check_missing_params(fixture, league, bet)
            if missing_para:
                raise MissingParametersError()
            return self._get('odds/live', fixture=fixture, league=league, bet=bet)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise

    def get_all_bets_in_play(self, id: str = None, search: str = None):

        """
        Get all available bets for in-play odds.

        :param id: The id of the bet name
        :param search: The name of the bet
        :return: Returns in play odds json schema
        """

        try:
            missing_para = self._parameter_validator.check_missing_params(id, search)
            if missing_para:
                raise MissingParametersError()
            if search:
                self._parameter_validator.validate_search_field(search)
            return self._get('odds/bets', id=id, search=search)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise
