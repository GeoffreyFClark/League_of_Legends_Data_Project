import requests
import json
import discord
import requests
from bs4 import BeautifulSoup



# Next 4 lines of code: Web-scraping Template
# Define the URL to scrape
url = "https://www.example.com"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Find the element(s) you want to scrape
heading = soup.find("h1")

# Use the text content of the element
print(heading.text)



intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'SUCCESSFULLY logged in as {client.user}')

# Replace API_KEY with your own Riot Games API key
API_KEY = "RIOTGAMES API KEY HERE"

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
        match_history = []
        print(matchids)
        for i, match_id in enumerate(matchids[0:5], start=1):
            print(i, match_id)
            match_data = get_match_history(match_id)
            for participant in match_data["info"]["participants"]:
                if participant["summonerName"].lower() == summoner_name.lower():
                    try:
                        champion = participant["championName"]
                        win = participant["win"]
                        champLevel = participant["champLevel"]
                        kills = participant["kills"]
                        deaths = participant["deaths"]
                        assists = participant["assists"]
                        spell1 = participant["spell1Casts"]
                        spell2 = participant["spell2Casts"]
                        spell3 = participant["spell3Casts"]
                        spell4 = participant["spell4Casts"]
                        summoner1 = participant["summoner1Casts"]
                        summoner2 = participant["summoner2Casts"]
                        wardsKilled = participant["wardsKilled"]
                        wardsPlaced = participant["wardsPlaced"]
                        totalDamageDealt = participant["totalDamageDealt"]
                        totalDamageDealtToChampions = participant["totalDamageDealtToChampions"]
                        damageDealtToObjectives = participant["damageDealtToObjectives"]
                        totalDamageTaken = participant["totalDamageTaken"]
                        damageTakenOnTeamPercentage = participant["challenges"]["damageTakenOnTeamPercentage"]
                        teamDamagePercentage = participant["challenges"]["teamDamagePercentage"]
                        totalTimeCCDealt = participant["totalTimeCCDealt"]
                        dragonKills = participant["dragonKills"]
                        baronKills = participant["baronKills"]
                        timePlayed = participant["timePlayed"]
                        totalTimeSpentDead = participant["totalTimeSpentDead"]
                        result_str = f"Matches ago: {i}\nChampion:{champion} KDA:{kills}/{deaths}/{assists} \nWin:{win} Champ Level:{champLevel} \nSpell1: {spell1}  Spell2: {spell2}  Spell3: {spell3}  Spell4: {spell4}\nSummoner1: {summoner1}  Summoner2: {summoner2}  WardsPlaced:{wardsPlaced} WardsKilled:{wardsKilled}\nDamageDealt:{totalDamageDealt} DamagetoChampions:{totalDamageDealtToChampions}\nTeamDMGTaken%:{damageTakenOnTeamPercentage*100:.2f}%\nTeamDMG%:{teamDamagePercentage*100:.2f}%\nDamagetoObjectives:{damageDealtToObjectives} TotalDamageTaken:{totalDamageTaken}\nTimeCCdealt:{totalTimeCCDealt} DragonKills:{dragonKills} BaronKills:{baronKills}\nTimePlayed:{timePlayed} TimeSpentDead:{totalTimeSpentDead}"
                        match_history.append(result_str)
                        match_history.append("\n\n")
                    except:
                        await message.channel.send(f"Matches ago: {i}\nError: Missing Match Data")
        print(match_history)
        await message.channel.send(f"{summoner_name}'s Match History: \n\n{''.join(match_history)}")

    if message.content.startswith('$mh pings'):
        summoner_name = message.content[10:]
        summoner_data = get_summoner_data(summoner_name)
        matchids = get_match_data(summoner_data["puuid"])
        match_history = []
        print(matchids)
        for i, match_id in enumerate(matchids[0:5], start=1):
            print(i, match_id)
            match_data = get_match_history(match_id)
            for participant in match_data["info"]["participants"]:
                if participant["summonerName"].lower() == summoner_name.lower():
                    try:
                        champion = participant["championName"]
                        win = participant["win"]
                        champLevel = participant["champLevel"]
                        kills = participant["kills"]
                        deaths = participant["deaths"]
                        assists = participant["assists"]
                        allInPings = participant["allInPings"]
                        assistMePings = participant["assistMePings"]
                        baitPings = participant["baitPings"]
                        basicPings = participant["basicPings"]
                        commandPings = participant["commandPings"]
                        dangerPings = participant["dangerPings"]
                        enemyMissingPings = participant["enemyMissingPings"]
                        enemyVisionPings = participant["enemyVisionPings"]
                        getBackPings = participant["getBackPings"]
                        holdPings = participant["holdPings"]
                        needVisionPings = participant["needVisionPings"]
                        onMyWayPings = participant["onMyWayPings"]
                        pushPings = participant["pushPings"]
                        visionClearedPings = participant["visionClearedPings"]
                        result_str = f"Matches ago: {i}\nChampion: {champion} Role: {role}\nKDA:{kills}/{deaths}/{assists} Win:{win} Champ Level:{champLevel}\nAllinPings:{allInPings} AssistMePings:{assistMePings} BaitPings:{baitPings}\nBasicPings:{basicPings} CommandPings:{commandPings} DangerPings:{dangerPings}\nEnemyMissingPings:{enemyMissingPings} EnemyVisionPings:{enemyVisionPings} GetBackPings:{getBackPings}\nHoldPings:{holdPings} NeedVisionPings:{needVisionPings}\nPushPings:{pushPings} OnMyWayPings:{onMyWayPings} VisionClearedPings:{visionClearedPings}"
                        match_history.append(result_str)
                        match_history.append("\n\n")
                    except:
                        await message.channel.send(f"Matches ago: {i}\nError: Missing Match Data")
        await message.channel.send(f"{summoner_name}'s Match History Pings: \n\n{''.join(match_history)}")

    if message.content.startswith('$mh2'):
        summoner_name = message.content[5:]
        summoner_data = get_summoner_data(summoner_name)
        matchids = get_match_data(summoner_data["puuid"])
        match_history = []
        print(matchids)
        for i, match_id in enumerate(matchids[0:5], start=1):
            print(i, match_id)
            match_data = get_match_history(match_id)
            for participant in match_data["info"]["participants"]:
                if participant["summonerName"].lower() == summoner_name.lower():
                    try:
                        alliedJungleMonsterKills = participant["challenges"]['alliedJungleMonsterKills']
                        buffsStolen = participant["challenges"]["buffsStolen"]
                        dodgeSkillShotsSmallWindow = participant["challenges"]["dodgeSkillShotsSmallWindow"]
                        skillshotsDodged = participant["challenges"]["skillshotsDodged"]
                        killParticipation = participant['challenges']['killParticipation']
                        maxLevelLeadLaneOpponent = participant["challenges"]["maxLevelLeadLaneOpponent"]
                        pickKillWithAlly = participant["challenges"]["pickKillWithAlly"]
                        soloKills = participant["challenges"]["soloKills"]
                        visionScoreAdvantageLaneOpponent = participant["challenges"]["visionScoreAdvantageLaneOpponent"]
                        teamRiftHeraldKills = participant["challenges"]["teamRiftHeraldKills"]
                        teamBaronKills = participant["challenges"]["teamBaronKills"]
                        scuttleCrabKills = participant["challenges"]["scuttleCrabKills"]
                        enemyJungleMonsterKills = participant["challenges"]["enemyJungleMonsterKills"]
                        moreEnemyJungleThanOpponent = participant["challenges"]["moreEnemyJungleThanOpponent"]
                        laningPhaseGoldExpAdvantage = participant["challenges"]["laningPhaseGoldExpAdvantage"]
                        totalHeal = participant["totalHeal"]
                        totalHealsOnTeammates = participant["totalHealsOnTeammates"]
                        totalDamageShieldedOnTeammates = participant["totalDamageShieldedOnTeammates"]
                        result_str = f"Matches ago: {i}\nAllyJg_MonsterKills:{alliedJungleMonsterKills:.0f} BuffsStolen:{buffsStolen} \nSkillShotsDodged:{skillshotsDodged} ShotsDodgedSmallWindow:{dodgeSkillShotsSmallWindow}\nKP:{killParticipation*100:.2f}% MaxLvlLeadLane:{maxLevelLeadLaneOpponent} PickKillwAlly:{pickKillWithAlly}\nSoloKills:{soloKills} VisScoreVsLaner:{visionScoreAdvantageLaneOpponent*100:.2f}% TeamRiftKills:{teamRiftHeraldKills}\nTeamBaronKills:{teamBaronKills} ScuttleKills:{scuttleCrabKills} EnemyJunggMonsterKills:{enemyJungleMonsterKills:.0f}.\nEnemyJungKillsvsOpp:{moreEnemyJungleThanOpponent:.0f}, LaneGoldExpAdvtg:{laningPhaseGoldExpAdvantage}\nTotalHeal:{totalHeal} HealsOnTeammates:{totalHealsOnTeammates} DMGShieldedOnTeammates:{totalDamageShieldedOnTeammates}"
                        match_history.append(result_str)
                        match_history.append("\n\n")
                    except:
                        await message.channel.send(f"Matches ago: {i}\nError: Missing Match Data")
        await message.channel.send(f"{summoner_name}'s Match History DataSet(2):\n\n{''.join(match_history)}")

    # LIVE MATCH DATA IN-PROGRESS
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
        missing_data = ""
        if rank_data == []:
            await message.channel.send(f"{summoner_name} is unranked.")
        else:
            for queue_data in rank_data:
                if queue_data["queueType"] == "RANKED_SOLO_5x5":
                    try:
                        tier = queue_data["tier"]
                    except:
                        missing_data += "tier "
                    try:
                        rank = queue_data["rank"]
                    except:
                        missing_data += "rank "
                    try:
                        league_points = queue_data["leaguePoints"]
                    except:
                        missing_data += "league_points "
                    try:
                        summoner_name = queue_data["summonerName"]
                    except:
                        pass
                    try:
                        wins = queue_data["wins"]
                    except:
                        missing_data += "wins "
                    try:
                        losses = queue_data["losses"]
                    except:
                        missing_data += "losses "
                    try:
                        inactive = queue_data["inactive"]
                    except:
                        missing_data += "inactive "
                    try:
                        freshBlood = queue_data["freshBlood"]
                    except:
                        missing_data += "freshBlood "
                    try:
                        hotStreak = queue_data["hotStreak"]
                    except:
                        missing_data += "queue_data "
                    if missing_data != "":
                        await message.channel.send(f"Missing: {missing_data}")
                    result_str = f"{summoner_name}, {queue_data['queueType']}: \n{tier} {rank}, {league_points} LP. \n{wins} Wins, {losses} Losses. \nInactive: {inactive}, Fresh Blood: {freshBlood}, Hot Streak: {hotStreak}."
                    await message.channel.send(result_str)

client.run("DISCORD BOT TOKEN HERE")
