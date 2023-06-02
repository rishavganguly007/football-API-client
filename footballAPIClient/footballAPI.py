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
        url = f"{self.base_url}/{path}"
        headers = self.get_headers()

        try:
            # preparing the query parameter
            params = {}
            if id:
                self.parameter_validator.validate_type_int(id, "id")
                params["id"] = id
            if name:
                self.parameter_validator.validate_type_str(name, 'name')
                params["name"] = name
            if code:
                self.parameter_validator.validate_type_str(code, "code")
                params["code"] = code
            if search:
                self.parameter_validator.validate_type_str(search, "search")
                params["search"] = search
            if season:
                self.parameter_validator.validate_type_int(season, "season")
                params['season'] = season
            if team:
                self.parameter_validator.validate_type_int(team, "team")
                params['team'] = team
            if type:
                self.parameter_validator.validate_type_str(type, "type")
                params['type'] = type
            if current:
                self.parameter_validator.validate_type_str(current, "current")
                params['current'] = current
            if last:
                self.parameter_validator.validate_type_int(last, "last")
                params['last'] = last
            if league:
                self.parameter_validator.validate_type_int(league, "league")
                params['league'] = league
            if venue:
                self.parameter_validator.validate_type_str(venue, "venue")
                params["venue"] = venue
            if date:
                self.parameter_validator.validate_type_str(date, "date")
                params["date"] = date
            if country:
                self.parameter_validator.validate_type_str(country, "country")
                params['country'] = country
            if city:
                self.parameter_validator.validate_type_str(city, "city")
                params['city'] = city
            if ids:
                self.parameter_validator.validate_type_str(ids, "ids")
                params["ids"] = ids
            if live:
                self.parameter_validator.validate_type_str(live, "live")
                params["live"] = live
            if next_:
                self.parameter_validator.validate_type_int(next_, "next")
                params["next"] = next_

            if from_:
                self.parameter_validator.validate_type_str(from_, "from")
                params["from"] = from_

            if to:
                self.parameter_validator.validate_type_str(to, "to")
                params["to"] = to

            if round_:
                self.parameter_validator.validate_type_str(round_, "round")
                params["round"] = round_

            if status:
                self.parameter_validator.validate_type_str(status, "status`")
                params["status"] = status

            if timezone:
                self.parameter_validator.validate_type_str(timezone, "timezone")
                params["timezone"] = timezone

            if h2h:
                self.parameter_validator.validate_type_str(h2h, "h2h")
                params["h2h"] = h2h

            if fixture:
                self.parameter_validator.validate_type_int(fixture, "fixture")
                params["fixture"] = fixture

            if player:
                self.parameter_validator.validate_type_int(player, "player")
                params["player"] = player

            if page:
                self.parameter_validator.validate_type_int(page, "page")
                params["page"] = page

            if coach:
                self.parameter_validator.validate_type_int(coach, "coach")
                params["coach"] = coach

            if bet:
                self.parameter_validator.validate_type_int(bet, "bet")
                params["bet"] = bet

            response_data = self._send_requests('GET', url, headers, params=params)
            return response_data
        except Exception as e:
            print(e)
            raise

    def get_countries(self, name: str = None, code: str = None, search: str = None):

        try:
            if search:
                self.parameter_validator.validate_search_field(search)
            return self._get("countries", name, code, search)
        except Exception as e:
            raise

    def get_timezone(self):
        # might need to add exceptions
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

        try:
            if code:
                self.parameter_validator.validate_code_field(code)


            if search:
                self.parameter_validator.validate_search_field(search)
            if season:
                self.parameter_validator.validate_season_field(season)
            if type:
                self.parameter_validator.validate_type_field(type)
            if current:
                self.parameter_validator.validate_current_field(current)
            if last:
                self.parameter_validator.validate_last_field(last)
            return self._get("leagues", id, name, country, code, season, team, type, current, search, last)

        except Exception as e:
            raise

    def get_leagues_seasons(self):
        return self._get("leagues/seasons")

    def get_teams_information(self, id: int = None,
                              name: str = None,
                              league: int = None,
                              season: int = None,
                              country: str = None,
                              code: str = None,
                              venue: str = None,
                              search: str = None):

        try:
            if season:
                self.parameter_validator.validate_season_field(season)
            if search:
                self.parameter_validator.validate_search_field(search)
            if code:
                self.parameter_validator.validate_team_code_field(code)
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
        except Exception as e:
            raise

    def team_statistics(self, league: int,
                        season: int,
                        team: int,
                        date: str= None):
        """
        TO-DO:  date should be of format: 'YYYY-MM-DD'
                season of 4 character, 'YYYY'
        -- create a helper dir to handle all this things
        """
        try:
            if season:
                self.parameter_validator.validate_season_field(season)
            if date:
                self.parameter_validator.validate_date_field(date)

            return self._get('teams/statistics', league=league, season=season, team=team, date=date)
        except Exception as e:
            raise

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

        try:
            if search:
                self.parameter_validator.validate_search_field(search)

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
        except Exception as e:
            raise

    def get_standings(self,
                      season: int,
                      league: int = None,
                      team: str = None):
        try:
            if season:
                self.parameter_validator.validate_season_field(season)
            return self._get('standings',
                             league=league,
                             season=season,
                             team=team)
        except Exception as e:
            raise

    def get_fixtures(self,
                     id: str = None,
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

        try:
            if ids:
                self.parameter_validator.validate_ids_field(ids)
            if live:
                self.parameter_validator.validate_live_field(live)
            if date:
                self.parameter_validator.validate_date_field(date)
            if season:
                self.parameter_validator.validate_season_field(season)
            if last:
                self.parameter_validator.validate_last_field(last)
            if next_:
                self.parameter_validator.validate_next_field(next_)
            if from_:
                self.parameter_validator.validate_date_field(from_)
            if to:
                self.parameter_validator.validate_date_field(to)
            if status:
                self.parameter_validator.validate_status_field(status)

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
                   current: str  # Enum: "true" "false"
                   ):

        try:
            self.parameter_validator.validate_season_field(season)
            if current:
                self.parameter_validator.validate_current_field(current)
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
                         season: int = None,  # format: 4 chars- YYYY
                         last: int = None,
                         next_: int = None,
                         from_: str = None,  # format: YYYY-MM-DD
                         to: str = None,  # format: YYYY-MM-DD
                         venue: int = None,
                         status: str= None,
                         timezone: str = None):

        try:
            self.parameter_validator.validate_h2h_field(h2h)
            if season:
                self.parameter_validator.validate_season_field(season)
            if from_:
                self.parameter_validator.validate_date_field(from_)
            if to:
                self.parameter_validator.validate_date_field(to)
            if status:
                self.parameter_validator.validate_status_field(status)
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
        try:
            missing_params = self.parameter_validator.check_missing_params(league, season, fixture,
                                                                           team, player, date, timezone)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            if season:
                self.parameter_validator.validate_season_field(season)
            if date:
                self.parameter_validator.validate_date_field(date)
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
        return self._get('predictions', fixture=fixture)

    def get_coachs(self,
                   id: int = None,
                   team: int = None,
                   search: str = None  # chars >= 3
                   ):

        try:
            missing_params = self.parameter_validator.check_missing_params(id, search, team)
            if missing_params:
                raise MissingParametersError("At least one of the optional parameters is required.")

            if search:
                self.parameter_validator.validate_search_field(search)

            return self._get('coachs', id=id, search=search, team=team)
        except Exception as e:
            raise

    def get_player_seasons(self, player: int = None):

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
        try:
            self.parameter_validator.check_missing_params(id, team, league, season, search)
            self.parameter_validator.validate_player_fields(id=id, team=team, league=league, season=season,
                                                            search=search, page=page)
            if season:
                self.parameter_validator.validate_season_field(season)
            if search:
                self.parameter_validator.validate_player_search_field(search)
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

        try:
            self.parameter_validator.validate_season_field(season)
            return self._get('players/topscorers', league=league, season=season)
        except Exception as e:
            raise

    def get_player_top_assist(self, league: int,
                              season: int
                              ):

        try:
            self.parameter_validator.validate_season_field(season)
            return self._get('players/topassists', league=league, season=season)
        except Exception as e:
            raise

    def get_player_top_yellow_cards(self, league: int,
                                    season: int
                                    ):
        try:
            self.parameter_validator.validate_season_field(season)
            return self._get('players/topyellowcards', league=league, season=season)
        except Exception as e:
            raise

    def get_player_top_red_cards(self, league: int,
                                 season: int
                                 ):
        try:
            self.parameter_validator.validate_season_field(season)
            return self._get('players/topredcards', league=league, season=season)
        except Exception as e:
            raise

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
            if search:
                self.parameter_validator.validate_search_field(search)
            return self._get('odds/bets', id=id, search=search)
        except MissingParametersError as e:
            print(f" Missing Parameter error")
            raise
