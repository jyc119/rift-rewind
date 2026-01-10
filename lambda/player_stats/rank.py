import json
import os
import requests

RIOT_API_KEY = os.environ["RIOT_API_KEY"]

HEADERS = {
    "X-Riot-Token": RIOT_API_KEY
}

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        game_name = body.get("gameName")
        tag_line = body.get("tagLine")

        if not game_name or not tag_line:
            return response(400, {"message": "Missing gameName or tagLine"})

        # 1️⃣ Riot ID → PUUID
        account_url = (
            f"https://{DEFAULT_REGION}.api.riotgames.com"
            f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        )

        acc_res = requests.get(account_url, headers=HEADERS)
        if acc_res.status_code != 200:
            return response(acc_res.status_code, {
                "message": "Riot ID not found"
            })

        account = acc_res.json()
        puuid = account["puuid"]

        # 2️⃣ PUUID → Summoner ID (regional endpoint)
        # summoner_url = (
        #     f"https://na1.api.riotgames.com"
        #     f"/lol/summoner/v4/summoners/by-puuid/{puuid}"
        # )

        # sum_res = requests.get(summoner_url, headers=HEADERS)
        # if sum_res.status_code != 200:
        #     return response(sum_res.status_code, {
        #         "message": "Summoner not found"
        #     })

        # summoner = sum_res.json()
        # summoner_id = summoner["id"]

        # 3️⃣ Summoner ID → Rank entries
        rank_url = (
            f"https://na1.api.riotgames.com"
            f"/lol/league/v4/entries/by-puuid/{puuid}"
        )

        rank_res = requests.get(rank_url, headers=HEADERS)
        if rank_res.status_code != 200:
            return response(rank_res.status_code, {
                "message": "Failed to fetch rank info"
            })

        entries = rank_res.json()

        # 4️⃣ Choose best queue
        solo = next((e for e in entries if e["queueType"] == "RANKED_SOLO_5x5"), None)
        flex = next((e for e in entries if e["queueType"] == "RANKED_FLEX_SR"), None)

        chosen = solo or flex

        if not chosen:
        return response(200, {
            "valid": True,
            "gameName": game_name,
            "tagLine": tag_line,
            "rank": {
                "tier": "GOLD",
                "rank": "I"
            },
            "message": "Unranked this season"
        })

        return response(200, {
            "valid": True,
            "gameName": game_name,
            "tagLine": tag_line,
            "rank": {
                "queue": chosen["queueType"],
                "tier": chosen["tier"],
                "rank": chosen["rank"],
                "lp": chosen["leaguePoints"],
                "wins": chosen["wins"],
                "losses": chosen["losses"]
            },
            "message": None
        })

    except Exception as e:
        return response(500, {"message": str(e)})
