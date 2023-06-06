# <p align="center"> footballAPIClient </p>
A simple wrapper around the football API provided by [**@API-SPORTS**](https://github.com/api-sports).
For full documentation on the API endpoints and subscription details, refer to [API-FOOTBALL](https://www.api-football.com/documentation-v3). Usage of this package requires any level of subscription and an `API-KEY`.

## Usage

Create the client
```bash
from  footballAPIClient  import  footballAPI

fp  =  footballAPI.FootballAPI("api-sports", api_key="YOUR_API_KEY")
```
Arguments:
<br>
	- `account_type`: Indicates weather the account is used from Rapid-API or from dashboard.  It consists of values: "rapid-api", and "api-sports", passing values other than this will raise an error.
  <br>
	- `api_key`: Valid API key required, or, it must be accessible via `API_KEY` environment variable.
	
