import requests

REGION = "europe" #global
PLATFORM = "euw1"


API_KEY = "RIOT API KEY HERE"  # only lasts 24 hours (development api key)
HEADERS = {"X-Riot-Token": API_KEY}


def get_puuid(summoner_name, tagline): # returns puuid from the in-game name and tag - needed for most requests, but most players only know their in-game stuff
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagline}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()["puuid"]


def get_summoner_profile(puuid):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    if res.status_code != 200:
        print(f"Error {res.status_code}: {res.text}")
        return None
    return res.json()

def get_ranked_stats(puuid):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def get_tft_ranked_stats(puuid):
    url = f"https://{PLATFORM}.api.riotgames.com/tft/league/v1/by-puuid/{puuid}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def get_match_ids(puuid, count=10):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()


def get_match_details(match_id):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def get_match_tags(match_data, puuid):
    participants = match_data["info"]["participants"]
    participant = next(p for p in participants if p["puuid"] == puuid)

    tags = []
    
    TAG_WEIGHTS = {
    "💰 Midas": 2,
    "🥊 Punching Bag": -3,
    "⚔️ Executioner": 3,
    "🛡️ Protector": 1,
    "🌌 Omnipresent": 2,
    "🧽 Bullet Sponge": -2,
    "🌾 Farmer": 1,
    "♾️ Infinity": 2,
    "💤 AFK": 0,
    "🎓 Strategist": 3,
    "🔪 Slayer": 2,
    "🔮 Omniscient": 0,
    "👾 Predator": 2,
    "📖 Fundamentos": 2,
    "🏴‍☠️ Yonko": 4,
    "🦝 Swiper": 2,
    "🪽 Guardian Angel": 2,
    "⬆️ Solo Levelling": 4,
    "💥 Zenkai Boost": 1,
    "⚰️ Return By Death": 1,
    "😈 Majin": 0,
    "💂 Warden": 0,
    "💼 Counter‑Intelligence": 1,
    "☀️ 5th Gear": 5,
    "💣 Atomic": 3,
    "🪬 Preserver": 2,
    "🌪️ Windshitter": -4,
    "🐒 Solo Bolo": 2,
    "🦥 Sloth": -1,
    "🐛 Hungry": 0,
    "🤝 Brother": 2,
    "👴 Unc": 1,
    "🔫 John Wick": 1,
    "🦧 Baussy": 1,

}

    # Midas (Most gold on the team)
    team_id = participant["teamId"]
    team_participants = [p for p in participants if p["teamId"] == team_id]
    max_gold = max(p["goldEarned"] for p in team_participants)
    if participant["goldEarned"] == max_gold:
        tags.append("💰 Midas")

    # Punching Bag (More deaths than kills and assists)
    if participant["deaths"] > (participant["kills"] + participant["assists"]):
        tags.append("🥊 Punching Bag")

    # Executioner (Highest kills on the team)
    max_kills = max(p["kills"] for p in team_participants)
    if participant["kills"] == max_kills and max_kills > 5:
        tags.append("⚔️ Executioner")

    # Protector (Most damage taken)
    max_damage_taken = max(p["totalDamageTaken"] for p in team_participants)
    if participant["totalDamageTaken"] == max_damage_taken:
        tags.append("🛡️ Protector")

    # Omnipresent (Kill Participation > 70%)
    team_kills = sum(p["kills"] for p in team_participants)
    kp = (participant["kills"] + participant["assists"]) / team_kills if team_kills else 0
    if kp >= 0.7:
        tags.append("🌌 Omnipresent")

    # Bullet Sponge (More deaths than kills and most damage taken)
    if (participant["deaths"] > participant["kills"] and
        participant["totalDamageTaken"] == max_damage_taken):
         tags.append("🧽 Bullet Sponge")

    # Farmer 🌾 (Most CS)
    cs = participant["totalMinionsKilled"] + participant["neutralMinionsKilled"]
    max_cs = max(p["totalMinionsKilled"] + p["neutralMinionsKilled"] for p in team_participants)
    if cs == max_cs:
        tags.append("🌾 Farmer")

    # Infinity ♾️ (No Deaths)
    if participant["deaths"] == 0:
        tags.append("♾️ Infinity")

    # AFK 💤 (Lowest KP + Damage)
    min_kp = min(
    (p["kills"] + p["assists"]) / team_kills if team_kills else 0
    for p in team_participants
)
    min_damage = min(p.get("totalDamageDealtToChampions", 0) for p in team_participants)

    kp = (participant["kills"] + participant["assists"]) / team_kills if team_kills else 0
    damage = participant.get("totalDamageDealtToChampions", 0)

    if kp == min_kp and damage == min_damage:
        tags.append("💤 AFK")

     # Strategist 🎓 (Highest objective + building damage)
    obj_damage = participant.get("damageDealtToObjectives", 0)
    building_damage = participant.get("damageDealtToBuildings", 0)
    total_obj_damage = obj_damage + building_damage

    max_obj_damage = max(
    p.get("damageDealtToObjectives", 0) + p.get("damageDealtToBuildings", 0)
    for p in team_participants
)

    if total_obj_damage == max_obj_damage and total_obj_damage > 0:
     tags.append("🎓 Strategist")

    # Slayer 🔪 (Largest Multikill > 2)
    if participant.get("largestMultiKill", 0) > 2:
        tags.append("🔪 Slayer")

    # Omniscient 🔮 (Highest vision score)
    max_vision = max(p.get("visionScore", 0) for p in team_participants)
    if participant.get("visionScore", 0) == max_vision:
        tags.append("🔮 Omniscient")

    # Predator 👾 (Early jungle kills > 0)
    if participant.get("challenges", {}).get("jungleKillsEarlyJungle", 0) > 0:
        tags.append("👾 Predator")

    # Fundamentos 📖 (Takedowns after level up > 0)
    if participant.get("challenges", {}).get("takedownsAfterGainingLevelAdvantage", 0) > 0:
        tags.append("📖 Fundamentos")

    # Yonko 🏴‍☠️ (> 40% of team damage)
    team_damage = sum(p.get("totalDamageDealtToChampions", 0) for p in team_participants)
    your_damage = participant.get("totalDamageDealtToChampions", 0)

    if team_damage > 0 and (your_damage / team_damage) >= 0.4:
        tags.append("🏴‍☠️ Yonko")

    # Swiper 🦝 (Stole at least one epic monster)
    if participant.get("challenges", {}).get("objectivesStolen", 0) > 0:
        tags.append("🦝 Swiper")

    # Guardian Angel 🪽 (Save ally from death > 0)
    if participant.get("challenges", {}).get("saveAllyFromDeath", 0) > 0:
        tags.append("🪽 Guardian Angel")

    # Solo Levelling ⬆️ (Solo Baron)
    if (participant.get("challenges", {}).get("soloBaronKills", 0))>= 1:
        tags.append("⬆️ Solo Levelling")

    # Zenkai Boost 💥 (Open Nexus and won the game)
    if participant.get("challenges", {}).get("openNexus", 0) > 0 and participant.get("win"):
        tags.append("💥 Zenkai Boost")

    # Return By Death ⚰️ (Most kills and deaths and won the game)
    max_kills = max(p["kills"] for p in team_participants)
    max_deaths = max(p["deaths"] for p in team_participants)

    if (participant["kills"] == max_kills and
    participant["deaths"] == max_deaths and
    participant.get("win")):
        tags.append("⚰️ Return By Death")
    
    # Majin 😈 (survive single digit hp > 2 times)
    if participant.get("challenges", {}).get("survivedSingleDigitHpCount", 0) >= 2:
        tags.append("😈 Majin")

    # Warden 💂 (Guard wards > 1)
    if participant.get("challenges", {}).get("wardsGuarded", 0) > 1:
        tags.append("💂 Warden")

    # Counter-Intelligence 💼 (Destroy the most wards on the team)
    max_wards_killed = max(p.get("wardsKilled", 0) for p in team_participants)
    if participant.get("wardsKilled", 0) == max_wards_killed and max_wards_killed > 0:
        tags.append("💼 Counter‑Intelligence")

    # 5th Gear ☀️ (Pentakill)
    if participant.get("Pentakills", 0) >= 1:
        tags.append("☀️ 5th Gear")

    # Atomic 💣 (Highest damage dealt to champions)
    max_damage_dealt = max(p["totalDamageDealtToChampions"] for p in team_participants)
    if participant["totalDamageDealtToChampions"] == max_damage_dealt:
        tags.append("💣Atomic")

    # Preserver 🪬 (Highest ally shielding and healing)
    shielding = participant.get("totalDamageShieldedOnTeammates", 0)
    healing = participant.get("challenges", {}).get("effectiveHealAndShielding", 0)
    support_value = shielding + healing

    max_support = max(
    p.get("totalDamageShieldedOnTeammates", 0) + 
    p.get("challenges", {}).get("effectiveHealAndShielding", 0)
        for p in team_participants
)

    if support_value == max_support and support_value > 0:
        tags.append("🪬 Preserver")

    # Windshitter (10 or more deaths with <= 1 kills)
    if participant["deaths"] >= 10 and participant["kills"] <= 1:
        tags.append("🌪️ Windshitter")

    # Solo Bolo (Most solo kills)
    max_solo = max(p.get("challenges", {}).get("soloKills", 0) for p in team_participants)
    if participant.get("challenges", {}).get("soloKills", 0) == max_solo and max_solo > 0:
        tags.append("🐒 Solo Bolo")

    # Hungry (most consumables purchased)
    max_consumables = max(p.get("challenges", {}).get("consumablesPurchased", 0) for p in participants)
    if participant.get("challenges", {}).get("consumablesPurchased", 0) == max_consumables and max_consumables > 0:
        tags.append("🐛 Hungry")

    # Brother (Highest immobilizeAndKillWithAlly)
    max_imm = max(p.get("challenges", {}).get("immobilizeAndKillWithAlly", 0) for p in participants)
    if participant.get("challenges", {}).get("immobilizeAndKillWithAlly", 0) == max_imm and max_imm > 0:
        tags.append("🤝 Brother")

    # Unc (longestTimeSpentLiving)
    max_time_alive = max(p.get("challenges", {}).get("longestTimeSpentLiving", 0) for p in participants)
    if participant.get("challenges", {}).get("longestTimeSpentLiving", 0) == max_time_alive and max_time_alive > 0:
        tags.append("👴 Unc")

    # John Wick (largestKillingSpree)
    max_spree = max(p.get("challenges", {}).get("largestKillingSpree", 0) for p in participants)
    if participant.get("challenges", {}).get("largestKillingSpree", 0) == max_spree and max_spree > 0:
        tags.append("🔫 John Wick")

    # Baussy (laningPhaseGoldExpAdvantage = 0 but higher gold overall than the lane opponent when the game ends)
    side_partners = [p for p in participants if p["teamId"] == participant["teamId"] and p["lane"] == participant["lane"]]
    opponents = [p for p in participants if p["teamId"] != participant["teamId"] and p["lane"] == participant["lane"]]
    gold_adv = participant.get("challenges", {}).get("laningPhaseGoldExpAdvantage", 0)

    if gold_adv <= 0 and opponents and side_partners and participant["win"]:  # must have lost lane, have a matchup, and win the game
        total_gold = participant.get("goldEarned", 0)
        opponent_total = opponents[0].get("goldEarned", 0)
        if total_gold > opponent_total:
            tags.append("🦧 Baussy")

    total_score = sum(TAG_WEIGHTS.get(tag, 0) for tag in tags)
    return tags, total_score

def find_team_mvp(match_data, team_id):
    participants = match_data["info"]["participants"]
    team_players = [p for p in participants if p["teamId"] == team_id]

    mvp = None
    best_score = float('-inf')

    for player in team_players:
        tags, score = get_match_tags(match_data, player["puuid"])
        player["mvp_score"] = score
        player["mvp_tags"] = tags
        if score > best_score:
            best_score = score
            mvp = player

    return mvp

def analyze_smurf_profile(puuid, match_history, summoner_profile):
    summoner_level = summoner_profile.get("summonerLevel", 0)
    valid_queues = {400, 420, 430, 440} # Draft, Solo/Duo, Blind, Flex
    total_cs = 0 # these will be updated as it iterates through each game
    total_minutes = 0
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_mvp_score = 0
    carry_tag_count = 0
    matches_played = 0

    carry_tags = {"☀️ 5th Gear", "Atomic 💣", "📖 Fundamentos", "Slayer 🔪", "⚔️ Executioner", "🌾 Farmer", "💰 Midas"} # tags likely associated with high performing players

    for match_data in match_history:
        queue_id = match_data["info"].get("queueId", 0)
        if queue_id not in valid_queues:
            continue

        participants = match_data["info"]["participants"]
        player = next(p for p in participants if p["puuid"] == puuid)

        # Game duration
        duration = match_data["info"]["gameDuration"] / 60
        

        # CS
        cs = player["totalMinionsKilled"] + player["neutralMinionsKilled"]
        total_cs += cs
        total_minutes += duration

        # KDA
        total_kills += player["kills"]
        total_deaths += player["deaths"]
        total_assists += player["assists"]

        # MVP Score
        tags, score = get_match_tags(match_data, puuid)
        total_mvp_score += score

        if any(tag in tags for tag in carry_tags):
            carry_tag_count += 1

        matches_played += 1

    if matches_played == 0:
        return None  # no usable games

    avg_cs_per_min = total_cs / total_minutes
    avg_kda = (total_kills + total_assists) / total_deaths if total_deaths else (total_kills + total_assists)
    avg_mvp_score = total_mvp_score / matches_played
    carry_tag_ratio = carry_tag_count / matches_played

    return {
        "matches": matches_played,
        "avg_cs_per_min": avg_cs_per_min,
        "avg_kda": avg_kda,
        "avg_mvp_score": avg_mvp_score,
        "carry_tag_ratio": carry_tag_ratio,
        "summoner_level": summoner_level
    }

def is_probable_smurf(profile): # editable config for what determines a potential smurf
    return (
        profile["avg_cs_per_min"] >= 7.5 and
        profile["avg_kda"] >= 4 and
        profile["avg_mvp_score"] > 8 and
        profile["carry_tag_ratio"] > 0.4 and
        profile["summoner_level"] < 100
    )
def potential_good_player(profile): # same as above but for a "good player"
    return (
        profile["avg_cs_per_min"] >= 7 and
        profile["avg_kda"] >= 3.5 and
        profile["avg_mvp_score"] > 7 and
        profile["carry_tag_ratio"] > 0.4 and
        profile["summoner_level"] > 180
    )

def display_profile_data(summoner, summoner_name, puuid):
    print("\nSummoner Profile:")
    print(f"Name: {summoner_name}")
    print(f"Level: {summoner['summonerLevel']}")
    print(f"Profile Icon ID: {summoner['profileIconId']}")

    ranked_stats = get_ranked_stats(puuid)
    print("\n📊 League of Legends Ranked:")

    if ranked_stats:
        for queue in ranked_stats:
            queue_type = queue["queueType"].replace("_", " ").title()
            print(f"\n{queue_type}:")
            print(f"  Tier: {queue['tier']} {queue['rank']} ({queue['leaguePoints']} LP)")
            print(f"  Wins: {queue['wins']}, Losses: {queue['losses']}")
            winrate = queue['wins'] / (queue['wins'] + queue['losses']) * 100
            print(f"  Win Rate: {winrate:.1f}%")
    else:
        print("Unranked")
    
    tft_stats = get_tft_ranked_stats(puuid)
    print("\n🎯 Teamfight Tactics Ranked:")

    if tft_stats:
        for queue in tft_stats:
            queue_type = queue["queueType"].replace("_", " ").title()
            print(f"\n{queue_type}:")
            print(f"  Tier: {queue['tier']} {queue['rank']} ({queue['leaguePoints']} LP)")
            print(f"  Wins: {queue['wins']}, Losses: {queue['losses']}")
            winrate = queue['wins'] / (queue['wins'] + queue['losses']) * 100
            print(f"  Win Rate: {winrate:.1f}%")
    else:
        print("Unranked")

def display_match_summary(match_data, puuid):
    participant = next(p for p in match_data["info"]["participants"] if p["puuid"] == puuid)
    cs = participant.get("totalMinionsKilled", 0) + participant.get("neutralMinionsKilled", 0)
    duration = match_data['info']['gameDuration'] / 60
    cs_per_min = cs / duration if duration else 0
    result = "Victory" if participant["win"] else "Defeat"
    tags, score = get_match_tags(match_data, puuid)

    return (
        f"**Champion:** {participant['championName']}\n"
        f"**K/D/A:** {participant['kills']}/{participant['deaths']}/{participant['assists']}\n"
        f"**CS:** {cs} ({cs_per_min:.1f}/min)\n"
        f"**Result:** {result}\n"
        f"**Traits:** {', '.join(tags)}"
    )
     

def display_full_match_players(match_data):
    participants = match_data["info"]["participants"]
    teams = {100: [], 200: []}

    for p in participants:
        tags, score = get_match_tags(match_data, p["puuid"])
        line = (f"{p['summonerName']} | {p['championName']} "
                f"| {p['kills']}/{p['deaths']}/{p['assists']} "
                f"| Traits: {', '.join(tags)} | Score: {score}")
        teams[p["teamId"]].append((score, line))

    print("\n🟦 Team 1 (Blue Side):")
    for _, line in sorted(teams[100], reverse=True):
        print("  " + line)
    mvp_100 = find_team_mvp(match_data, 100)
    if mvp_100:
        print(f"👑 MVP: {mvp_100['summonerName']} ({mvp_100['championName']})")

    print("\n🟥 Team 2 (Red Side):")
    for _, line in sorted(teams[200], reverse=True):
        print("  " + line)
    mvp_200 = find_team_mvp(match_data, 200)
    if mvp_200:
        print(f"👑 MVP: {mvp_200['summonerName']} ({mvp_200['championName']})")
    

if __name__ == "__main__":
    summoner_name = input("Enter your summoner name (case-sensitive): ")
    tagline = input("Enter your tagline (no hashtag): ")
    mvp_count = 0
    total_matches = 0
try:
    puuid = get_puuid(summoner_name, tagline)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("❌ Summoner not found! Please check your summoner name and tagline (no hashtag).")
    elif e.response.status_code == 403:
        print("❌ Invalid or expired API key. Please update your Riot API key.")
    else:
        print(f"❌ Error fetching summoner info")
    exit()
summoner_profile = get_summoner_profile(puuid)
if summoner_profile:
        display_profile_data(summoner_profile, summoner_name, puuid)
else:
     print("⚠️ Failed to retrieve summoner profile.")

match_ids = get_match_ids(puuid, count=10)
match_history = [get_match_details(match_id) for match_id in match_ids]
for match_id in match_ids: # iterate through the matches and display the summary and full match players for each
        match_data = get_match_details(match_id)
        display_match_summary(match_data, puuid)
        display_full_match_players(match_data)
        

smurf_profile = analyze_smurf_profile(puuid, match_history, summoner_profile)
if smurf_profile:
    print("\n📊 Smurf Profile Summary:")
    print(f"Summoner Level: {smurf_profile['summoner_level']}")
    print(f"Matches Analyzed: {smurf_profile['matches']}")
    print(f"Avg CS/Min: {smurf_profile['avg_cs_per_min']:.2f}")
    print(f"Avg KDA: {smurf_profile['avg_kda']:.2f}")
    print(f"Avg MVP Score: {smurf_profile['avg_mvp_score']:.2f}")
    print(f"Carry Tag Ratio: {smurf_profile['carry_tag_ratio']*100:.1f}%")

if is_probable_smurf(smurf_profile):
    print("🚨 This player shows strong signs of smurfing.")
else:
    print("✅ No strong smurf indicators detected.")

