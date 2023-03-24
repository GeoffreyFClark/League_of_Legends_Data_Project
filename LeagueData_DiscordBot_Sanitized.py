import requests
import json
import discord
import requests
from bs4 import BeautifulSoup

# Replace API_KEY with your own Riot Games API key
API_KEY = ""
# https://developer.riotgames.com/

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'SUCCESSFULLY logged in as {client.user}')

# # Define the base URL for the Riot Games API
BASE_URL = "https://na1.api.riotgames.com"
BASE_URL2 = "https://americas.api.riotgames.com"

# Define the endpoints for the Riot Games API
SUMMONER_ENDPOINT = "/lol/summoner/v4/summoners/by-name/"
MATCH_HISTORY_ENDPOINT = "/lol/match/v5/matches/"
MATCH_ENDPOINT = "/lol/match/v5/matches/by-puuid/"
LIVE_MATCH_ENDPOINT = "/lol/spectator/v4/active-games/by-summoner/"

# Define the function to get Summoner Data
def get_summoner_data(summoner_name):
    url = BASE_URL + SUMMONER_ENDPOINT + summoner_name  + "?api_key=" + API_KEY
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Define the function to get Match Data
def get_match_data(puuid):
    url = BASE_URL2 + f"/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Define the function to get Live Match Data
def get_live_match_data(summoner_id):
    url = BASE_URL + LIVE_MATCH_ENDPOINT + summoner_id + "?api_key=" + API_KEY
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Define the function to get Match History
def get_match_history(match_id):
    url = BASE_URL2 + MATCH_HISTORY_ENDPOINT + match_id  + "?api_key=" + API_KEY
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$summoner'):
        summoner_name = message.content[10:]
        summoner_data = get_summoner_data(summoner_name)
        await message.channel.send("Summoner Data: " + json.dumps(summoner_data, indent=4))
    if message.content.startswith('$matchids'):
        summoner_name = message.content[10:]
        summoner_data = get_summoner_data(summoner_name)
        matchids = get_match_data(summoner_data["puuid"])
        await message.channel.send(f"{summoner_name} match IDs: " + json.dumps(matchids, indent=4))
    if message.content.startswith('$match history'):
        summoner_name = message.content[15:]
        summoner_data = get_summoner_data(summoner_name)
        matchids = get_match_data(summoner_data["puuid"])
        result_str = ""
        print(matchids)
        for i, match_id in enumerate(matchids[0:4], start=1):
            print(i, match_id)
            match_data = get_match_history(match_id)
            gameMode = match_data["info"]["gameMode"]
            property_names = ["championName",
                         "win",
                         "champLevel",
                         "kills",
                         "deaths",
                         "assists",
                         "spell1Casts",
                         "spell2Casts",
                         "spell3Casts",
                         "spell4Casts",
                         "summoner1Casts",
                         "summoner2Casts",
                         "wardsKilled",
                         "wardsPlaced",
                         "totalDamageDealt",
                         "totalDamageDealtToChampions",
                         "damageDealtToObjectives",
                         "totalDamageTaken",
                         "dragonKills",
                         "baronKills",
                         "timePlayed",
                         "totalTimeSpentDead",
                        
            ]
            result_str += f"\nMatches ago: {i}\ngameMode: {gameMode}\n"
            for participant in match_data["info"]["participants"]:
                if participant["summonerName"].lower() == summoner_name.lower():
                    for property_name in property_names:
                        try:
                            result_str += f"{property_name}: {participant[property_name]}\n"
                        except:
                            result_str += f"Missing: {property_name}\n"
        await message.channel.send(f"{summoner_name}'s Match History: \n{''.join(result_str)}")


    if message.content.startswith('$mh pings'):
        summoner_name = message.content[10:]
        summoner_data = get_summoner_data(summoner_name)
        matchids = get_match_data(summoner_data["puuid"])
        print(matchids)
        result_str = ""
        for i, match_id in enumerate(matchids[0:5], start=1):
            print(i, match_id)
            match_data = get_match_history(match_id)
            gameMode = match_data["info"]["gameMode"]
            result_str += f"\nMatches ago: {i}\n"
            for participant in match_data["info"]["participants"]:
                if participant["summonerName"].lower() == summoner_name.lower():
                    property_names = [
                    "championName",
                    "win",
                    "champLevel",
                    "kills",
                    "deaths",
                    "assists",
                    "allInPings",
                    "assistMePings",
                    "baitPings",
                    "basicPings",
                    "commandPings",
                    "dangerPings",
                    "enemyMissingPings",
                    "enemyVisionPings",
                    "getBackPings",
                    "holdPings",
                    "needVisionPings",
                    "onMyWayPings",
                    "pushPings",
                    "visionClearedPings"
                    ]
                    for property_name in property_names:
                        try:
                            result_str += f"{property_name}: {participant[property_name]}\n"
                        except:
                            result_str += f"Missing: {property_name}\n"
        await message.channel.send(f"{summoner_name}'s Match History Pings: \n{''.join(result_str)}")

    if message.content.startswith('$mh2'):
        summoner_name = message.content[5:]
        summoner_data = get_summoner_data(summoner_name)
        matchids = get_match_data(summoner_data["puuid"])
        result_str = ""
        print(matchids)
        property_names = [  "alliedJungleMonsterKills",
                            "buffsStolen",
                            "dodgeSkillShotsSmallWindow",
                            "skillshotsDodged",
                            "killParticipation",
                            "maxLevelLeadLaneOpponent",
                            "pickKillWithAlly",
                            "soloKills",
                            "visionScoreAdvantageLaneOpponent",
                            "teamRiftHeraldKills",
                            "teamBaronKills",
                            "scuttleCrabKills",
                            "enemyJungleMonsterKills",
                            "moreEnemyJungleThanOpponent",
                            "laningPhaseGoldExpAdvantage",
                            ]
        for i, match_id in enumerate(matchids[0:4], start=1):
            result_str += f"\nMatches ago: {i}\n"
            print(i, match_id)
            match_data = get_match_history(match_id)
            challenges = "challenges"
            for participant in match_data["info"]["participants"]:
                if participant["summonerName"].lower() == summoner_name.lower():
                    for property_name in property_names:    
                        try:
                            intermediary = participant[challenges][property_name]
                            if isinstance(intermediary, (float)):
                                intermediary = f"{intermediary:.2f}"
                            result_str += f"{property_name}: {intermediary}\n"
                        except:
                            result_str += f"Missing: {property_name}\n"
                    totalHeal = participant["totalHeal"]
                    totalHealsOnTeammates = participant["totalHealsOnTeammates"]
                    totalDamageShieldedOnTeammates = participant["totalDamageShieldedOnTeammates"]
                    result_str += f"totalHeal: {totalHeal}\n"
                    result_str += f"totalHeal: {totalHealsOnTeammates}\n"
                    result_str += f"totalHeal: {totalDamageShieldedOnTeammates}\n"
        await message.channel.send(f"{summoner_name}'s Match History DataSet(2):\n{''.join(result_str)}")


    # if message.content.startswith('$livematch'):
    #     summoner_name = message.content[11:]
    #     summoner_data = get_summoner_data(summoner_name)
    #     live_match_data = get_live_match_data(summoner_data["id"])
    #     await message.channel.send(f"{summoner_name}'s Live Match Data: " + json.dumps(live_match_data["participants"], indent=4))
    if message.content.startswith('$rank'):
        summoner_name = message.content[6:]
        summoner_data = get_summoner_data(summoner_name)
        url = BASE_URL + "/lol/league/v4/entries/by-summoner/" + summoner_data["id"] + "?api_key=" + API_KEY
        headers = {"X-Riot-Token": API_KEY}
        rank = requests.get(url, headers=headers)
        rank_data = rank.json()
        result_str = ""
        property_names = [  "tier",
                            "rank",
                            "leaguePoints",
                            "wins",
                            "losses",
                            "inactive",
                            "freshBlood",
                            "hotStreak"
                        ]
        for queue_data in rank_data:
            if queue_data["queueType"] == "RANKED_SOLO_5x5":
                for property_name in property_names:
                        try:
                            result_str += f"{property_name}: {queue_data[property_name]}\n"
                        except:
                            result_str += f"Missing: {property_name}\n"
        await message.channel.send(f"{summoner_name} RANKED_SOLO/DUO:\n{result_str}")

client.run("DISCORD BOT TOKEN HERE")
