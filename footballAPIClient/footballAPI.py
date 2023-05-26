import http.client
import requests


class FootballAPI:
    def __init__(self,
                 api_key: str = None):
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
             season: str = None,
             team: str = None,
             type: str = None,
             current: str = None,
             search: str = None,
             last: str = None):
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
        return self._get("leagues", id, name, country, code, season, team, type, current, search, last)

    def get_leagues_seasons(self):
        # TO-DO: only send the Responses
        return self._get("leagues/seasons")