import os
import json
import requests

RIOT_API_KEY = os.environ["RIOT_API_KEY"]

ROUTING_REGIONS = ["americas", "europe", "asia"]  # you can extend later

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    name = body.get("gameName")
    tagline = body.get("tagLine")

    if not name or not tagline:
        return response(400, {"message": "Missing gameName or tagLine"})

    for region in ROUTING_REGIONS:
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
        r = requests.get(url, headers={"X-Riot-Token": RIOT_API_KEY})

        if r.status_code == 200:
            data = r.json()
            return response(200, {
                "valid": True,
                "puuid": data["puuid"],
                "gameName": data["gameName"],
                "tagLine": data["tagLine"],
                "routingRegion": region
            })

        if r.status_code not in (404, 403):
            return response(r.status_code, {"message": r.text})

    return response(404, {"valid": False, "message": "Player not found"})

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
