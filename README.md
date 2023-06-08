# <p align="center"> footballAPIClient </p>
A simple wrapper around the football API provided by [**@API-SPORTS**](https://github.com/api-sports).
For full documentation on the API endpoints and subscription details, refer to [API-FOOTBALL](https://www.api-football.com/documentation-v3). Usage of this package requires any level of subscription and an `API-KEY`.

## Installation
```python
pip install footballapiclient
```


## Usage

Create the client
```python
from  footballAPIClient  import  footballAPI

fp  =  footballAPI.FootballAPI("api-sports", api_key="YOUR_API_KEY")
```
Arguments:
<br>
	- `account_type`: Indicates weather the account is used from Rapid-API or from dashboard.  It consists of values: "rapid-api", and "api-sports", passing values other than this will raise an error.
  <br>
	- `api_key`: Valid API key required, or, it must be accessible via `API_KEY` environment variable.

## Examples
Getting the country data by calling the `countries` API.
```python
print(fp.get_countries())
```
<br>

<br>
Arguments:

	name: (optional) The name of the country  
	code:  (optional) The Alpha2 code of the country 
	search:  (optional) The name of the country
	:return: Returns the Country json schema
<br>

Output: 

{
  "get": "countries",
  "parameters": {
    "name": "england"
  }, 
  "errors": [],
  "results": 1,
  "paging": {
    "current": 1,
    "total": 1
  },
  "response": [
    {
      "name": "England",
      "code": "GB",
      "flag": "https://media.api-sports.io/flags/gb.svg"
    }
  ]
}





