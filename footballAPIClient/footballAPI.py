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

    def _send_requests(self, method, path, data=None):
        url = f"{self.base_url}/{path}"
        headers = self.get_headers()
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                data = data
            )
            response.raise_for_status()
            return response.json
        except requests.exceptions.RequestException as e:
            # Handle request exceptions or errors
            print(f"Request error: {e}")
            return None

    def get_countries(self, params=None) :

        return self._send_requests('GET', "countries")


