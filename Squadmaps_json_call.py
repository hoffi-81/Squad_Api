import requests

BASE_URL = "https://raw.githubusercontent.com/mahtoid/SquadMaps/refs/heads/master/scripts/finished.json"


# Make the request to the API
asset_names = ""

for unit_name in factions_long:
     response = requests.get(BASE_URL, params={"unitName": unit_name})
     if asset_names == "":
          asset_names = [[asset["name"] for asset in response.json().get("assets", [])]]
     else:
          asset_names.append([asset["name"] for asset in response.json().get("assets", [])])

if __name__ == "__main__":
     print(asset_names)