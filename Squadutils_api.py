import requests
from Battlemetrics_api import factions_long

# Define the base URL and endpoint
BASE_URL = "https://squadutils.org/api/v1/unitAssets"


# Make the request to the API
asset_names = ""

for unit_name in factions_long:
     response = requests.get(BASE_URL, params={"unitName": unit_name})
     if asset_names == "":
          asset_names = [[[asset["name"] for asset in response.json().get("assets", [])], [asset["mapIcon"] for asset in response.json().get("assets", [])]]]
     else:
          asset_names_temp = [[asset["name"] for asset in response.json().get("assets", [])], [asset["mapIcon"] for asset in response.json().get("assets", [])]]
          asset_names.append(asset_names_temp)
          


#mapIcon

if __name__ == "__main__":
     print(asset_names[0][1])
     # print(asset_names)
