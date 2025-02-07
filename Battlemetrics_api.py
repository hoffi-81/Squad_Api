from battlemetrics import Battlemetrics
import asyncio
from dotenv import load_dotenv
import os
import time


load_dotenv()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Instantiate the API wrapper with your token
bmapi = Battlemetrics(os.getenv("AUTH_TOKEN"))



# Retrieve player information
#145690626
#1004031959
player = asyncio.run(bmapi.player.session_history(os.getenv("PLAYER_ID")))

# if player["data"][0]["attributes"]["stop"] == None:
# Get Server ID 
Current_server_ID = player["data"][0]["relationships"]["server"]["data"]["id"]

# Get Server Info
server = asyncio.run(bmapi.server.info(Current_server_ID))

current_map = server["data"]["attributes"]["details"]["map"]

factions_long = [server["data"]["attributes"]["details"]["squad_teamOne"],
               server["data"]["attributes"]["details"]["squad_teamTwo"]]

# Get Faction 
factions_short = [factions_long[0].split("_")[0], 
               factions_long[1].split("_")[0]]

if __name__ == "__main__":
     print(current_map)
     print(factions_long)