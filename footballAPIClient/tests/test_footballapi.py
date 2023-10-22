
import pytest
from footballAPIClient.Exceptions.MissingParametersError import MissingParametersError
from footballAPIClient.footballAPI import FootballAPI
from footballAPIClient._constants import RAPID_API


@pytest.fixture
def status_mock_fixture(requests_mock):
    mock_response = {
        "requests": {
            "limit_day": 10,  # maximum number of requests allowed per day
            "current": 6  # current number of requests made today
        }
    }
    # Use return to be able to access requests_mock attributes
    return requests_mock.get("/v3/status", json={"status": "OK", "errors":None, "response": mock_response})

@pytest.fixture
def api(status_mock_fixture):
    return FootballAPI(RAPID_API, api_key="test-key")

def test_get_countries(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/countries", json={
        "countries": [
            {"name": "England", "code": "ENG"},
            {"name": "Spain", "code": "ESP"}
        ]
    })
    countries = api.get_countries()
    assert isinstance(countries, dict)
    assert "countries" in countries

def test_get_timezone(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/timezone", json={
        "timezone": "Europe/London"
    })
    timezone = api.get_timezone()
    assert isinstance(timezone, dict)
    assert "timezone" in timezone

def test_get_leagues(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 1, "name": "La Liga", "country": "Spain"},
            {"id": 2, "name": 100, "country": "England"}
        ]
    })
    leagues = api.get_leagues()
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_leagues_with_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(id=2, name="La Liga", country="England")
    assert isinstance(leagues, dict)
    assert "leagues" in leagues


def test_get_leagues_with_invalid_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": 100, "country": "England"}
        ]
    })
    with pytest.raises(TypeError):
        api.get_leagues(id="A string", name=100, country="England")

def test_get_leagues_with_code(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(code="GB")
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_leagues_with_season(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(season=2019)
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_leagues_with_search(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(search="La Liga")
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_leagues_with_type(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(type=0)
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_leagues_with_current(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(current='false')
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_leagues_with_last(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/leagues", json={
        "leagues": [
            {"id": 2, "name": "La Liga", "country": "England"}
        ]
    })
    leagues = api.get_leagues(last=True)
    assert isinstance(leagues, dict)
    assert "leagues" in leagues

def test_get_teams_seasons(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams/seasons", json={
        "seasons": [
            {"year": 2019},
            {"year": 2020}
        ]
    })
    seasons = api.get_teams_seasons(team=1)
    assert isinstance(seasons, dict)
    assert "seasons" in seasons

def test_get_team_statistics(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams/statistics", json={
        "statistics": [
            {"team": "Liverpool", "league": 100, "season": 2019},
            {"team": "Real Madrid", "league": "La Liga", "season": 2020}
        ]
    })
    statistics = api.get_team_statistics(league=100, season=2019, team=1)
    assert isinstance(statistics, dict)
    assert "statistics" in statistics

def test_get_team_statistics_with_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams/statistics", json={
        "statistics": [
            {"team": "Liverpool", "league": 100, "season": 2019},
        ]
    })
    statistics = api.get_team_statistics(team=2, league=100, season=2019)
    assert isinstance(statistics, dict)
    assert "statistics" in statistics

def test_get_team_statistics_with_invalid_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams/statistics", json={
        "statistics": [
            {"team": "Liverpool", "league": 100, "season": 2019},
        ]
    })
    with pytest.raises(TypeError):
        api.get_team_statistics(team="It is a string", league=100, season=2019)


def test_get_teams_information(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams", json={
        "teams": [
            {"id": 1, "name": "Liverpool", "country": "England"},
            {"id": 2, "name": "Real Madrid", "country": "Spain"}
        ]
    })
    teams = api.get_teams_information(id=1, name="Liverpool", country="England", season=2019)
    assert isinstance(teams, dict)
    assert "teams" in teams

def test_get_teams_information_with_invalid_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams", json={
        "teams": [
            {"id": 1, "name": 100, "country": "England"},
            {"id": 2, "name": "Real Madrid", "country": "Spain"}
        ]
    })
    with pytest.raises(TypeError):
        api.get_teams_information(id=1, name=100, country="England", season=2019)

def test_get_teams_information_with_no_params(api, status_mock_fixture, requests_mock):
    with pytest.raises(MissingParametersError):
        api.get_teams_information()

def test_get_teams_information_with_search(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams", json={
        "teams": [
            {"id": 1, "name": "Liverpool", "country": "England"},
        ]
    })
    teams = api.get_teams_information(search="Liverpool")
    assert isinstance(teams, dict)
    assert "teams" in teams

def test_get_teams_information_with_team_id(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/teams", json={
        "teams": [
            {"id": 1, "name": "Liverpool", "country": "England"},
        ]
    })
    teams = api.get_teams_information(code="AUD")
    assert isinstance(teams, dict)
    assert "teams" in teams

def test_get_countries_with_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/countries", json={
        "countries": [
            {"name": "United Kingdom", "code": "GB"},
        ]
    })
    countries = api.get_countries(name="United Kingdom", code="GB")
    assert isinstance(countries, dict)
    assert "countries" in countries

def test_get_country_with_code(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/countries", json={
        "countries": [
            {"name": "United Kingdom", "code": "GB"},
        ]
    })
    countries = api.get_countries(code="GB")
    assert isinstance(countries, dict)
    assert "countries" in countries

def test_get_countries_with_search(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/countries", json={
        "countries": [
            {"name": "United Kingdom", "code": "GB"},
        ]
    })
    countries = api.get_countries(search="United Kingdom")
    assert isinstance(countries, dict)
    assert "countries" in countries


def test_get_countries_with_no_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/countries", json={
        "countries": []
    })
    countries = api.get_countries()
    assert isinstance(countries, dict)
    assert "countries" in countries

def test_get_timezone_with_no_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/timezone", json={
        "timezone": "Europe/London"
    })
    timezones = api.get_timezone()
    assert isinstance(timezones, dict)
    assert "timezone" in timezones


def test_get_venues(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/venues?id=1&country=England", json={
        "venues": [
            {"name": "Wembley", "city": "London"},
            {"name": "Camp Nou", "city": "Barcelona"}
        ]
    })
    venues = api.get_venues(country="England", id=1)
    assert isinstance(venues, dict)
    assert "venues" in venues

def test_get_standings(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/standings", json={
        "standings": [
            {"team": "Barcelona", "points": 75},
            {"team": "Real Madrid", "points": 70}
        ]
    })
    standings = api.get_standings(league=1, season=2021)
    assert isinstance(standings, dict)
    assert "standings" in standings

def test_get_fixtures(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures", json={
        "fixtures": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
            {"homeTeam": "Real Madrid", "awayTeam": "Barcelona"}
        ]
    })
    fixtures = api.get_fixtures(league=1, season=2021)
    assert isinstance(fixtures, dict)
    assert "fixtures" in fixtures

def test_get_fixtures_with_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures", json={
        "fixtures": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
        ]
    })
    fixtures = api.get_fixtures(league=1, season=2021, team=1)
    assert isinstance(fixtures, dict)
    assert "fixtures" in fixtures


def test_get_fixtures_with_live(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures", json={
        "fixtures": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
        ]
    })
    fixtures = api.get_fixtures(league=1, season=2021, live="01-01-2021")
    assert isinstance(fixtures, dict)
    assert "fixtures" in fixtures

def test_get_fixtures_with_date(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures", json={
        "fixtures": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
        ]
    })
    fixtures = api.get_fixtures(league=1, season=2021, date="2023-01-01")
    assert isinstance(fixtures, dict)
    assert "fixtures" in fixtures

def test_get_fixtures_with_round(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures", json={
        "fixtures": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
        ]
    })
    fixtures = api.get_fixtures(league=1, season=2021, round_="one")
    assert isinstance(fixtures, dict)
    assert "fixtures" in fixtures

def test_get_fixtures_with_next(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures", json={
        "fixtures": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
        ]
    })
    fixtures = api.get_fixtures(league=1, season=2021, next_=100)
    assert isinstance(fixtures, dict)
    assert "fixtures" in fixtures

def test_get_fixtures_no_params(api, status_mock_fixture, requests_mock):
    with pytest.raises(MissingParametersError):
        api.get_fixtures()

def test_get_rounds(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures/rounds", json={
        "rounds": [
            {"name": "Round 1", "league": 1, "season": 2021},
            {"name": "Round 2", "league": 1, "season": 2021}
        ]
    })
    rounds = api.get_rounds(league=1, season=2021)
    assert isinstance(rounds, dict)
    assert "rounds" in rounds

def test_get_rounds_with_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures/rounds", json={
        "rounds": [
            {"name": "Round 1", "league": 1, "season": 2021},
        ]
    })
    rounds = api.get_rounds(league=1, season=2021, current='true')
    assert isinstance(rounds, dict)
    assert "rounds" in rounds

def test_get_rounds_no_params(api, status_mock_fixture, requests_mock):
    with pytest.raises(TypeError):
        api.get_rounds()

def test_get_head_to_head(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures/headtohead", json={
        "head2head": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
            {"homeTeam": "Real Madrid", "awayTeam": "Barcelona"}
        ]
    })
    head_to_head = api.get_head_to_head(h2h="100-101", league=1, season=2021)
    assert isinstance(head_to_head, dict)
    assert "head2head" in head_to_head

def test_get_head_to_head_with_all_params(api, status_mock_fixture, requests_mock):
    requests_mock.get("/v3/fixtures/headtohead", json={
        "head2head": [
            {"homeTeam": "Barcelona", "awayTeam": "Real Madrid"},
        ]
    })
    head_to_head = api.get_head_to_head(h2h="100-101", league=1, season=2021, last=100, next_=100, from_="2023-07-01", to="2023-07-01", status="NS-PST-FT", venue="paris")
    assert isinstance(head_to_head, dict)
    assert "head2head" in head_to_head


def test_get_player_top_red_cards(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/players/topredcards', json={
        "cards": [
            {"player": "Lionel Messi", "team": "Barcelona", "red_cards": 5},
            {"player": "Cristiano Ronaldo", "team": "Real Madrid", "red_cards": 3}
        ]
    })
    cards = api.get_player_top_red_cards(league=1, season=2021)
    assert isinstance(cards, dict)
    assert "cards" in cards

def test_get_player_top_red_cards_failure(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/players/topredcards', status_code=404)
    with pytest.raises(TypeError):
        api.get_player_top_red_cards(league=1)

def test_get_transfers(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/transfers', json={
        "transfers": [
            {"player": "Lionel Messi", "from_team": "Barcelona", "to_team": "Paris Saint-Germain"},
            {"player": "Cristiano Ronaldo", "from_team": "Real Madrid", "to_team": "Manchester United"}
        ]
    })
    transfers = api.get_transfers(player=100, team=101)
    assert  isinstance(transfers, dict)
    assert "transfers" in transfers

def test_get_transfers_failure(api, status_mock_fixture, requests_mock):
    requests_mock.get('https://api.football.com/transfers', status_code=404)
    with pytest.raises(MissingParametersError):
        api.get_transfers()

def test_get_trophies(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/trophies', json={
        "trophies": [
            {"team": "Barcelona", "competition": "La Liga", "year": 2020},
            {"team": "Real Madrid", "competition": "Champions League", "year": 2019}
        ]
    })
    trophies = api.get_trophies(player=1, coach=100)
    assert isinstance(trophies, dict)
    assert "trophies" in trophies

def test_get_trophies_failure(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/trophies', status_code=404)
    with pytest.raises(TypeError):
        api.get_trophies(team_id=1)

def test_get_sidelined(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/sidelined', json={
        "sidelined": [
            {"player": "Lionel Messi", "team": "Barcelona", "injury": "ankle sprain"},
            {"player": "Cristiano Ronaldo", "team": "Real Madrid", "injury": "hamstring strain"}
        ]
    })
    sidelined = api.get_sidelined(player=1, coach=100)
    assert isinstance(sidelined, dict)
    assert "sidelined" in sidelined

def test_get_sidelined_failure(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/sidelined', status_code=404)
    with pytest.raises(MissingParametersError):
        api.get_sidelined()

def test_get_in_play_odds(api, status_mock_fixture, requests_mock):
    requests_mock.get('/v3/odds/live', json={
        "odds": [
            {"home_team": "Barcelona", "away_team": "Real Madrid", "odds": "1.5"},
            {"home_team": "Real Madrid", "away_team": "Barcelona", "odds": "2.0"}
        ]
    })
    odds = api.get_in_play_odds(fixture=1, league=1, bet=1000)
    assert isinstance(odds, dict)
    assert "odds" in odds

def test_get_in_play_odds_failure(api, status_mock_fixture, requests_mock):
    requests_mock.get('https://api.football.com/in-play-odds', status_code=404)
    with pytest.raises(MissingParametersError):
        api.get_in_play_odds()