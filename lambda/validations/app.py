import os
import json
import requests

RIOT_API_KEY = os.environ["RIOT_API_KEY"]

S3_BUCKET = "rift-rewind-bucket"
ROUTING_REGIONS = ["americas", "europe", "asia"]  # you can extend later

s3 = boto3.client("s3")

def save_data_to_s3(match_id, match_data):
    player_name = GAME_NAME+TAG_LINE
    # key = f"raw/{player_name}/{match_id}.json"
    key = f"match/{player_name}/{match_id}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(match_data),
        ContentType="application/json"
    )
    print(f"Saved {match_id} to s3://{S3_BUCKET}/{key}")

def save_matches(puuid, region):
    
    region_mapping = {
        "na1": "americas"
        "euw1": "europe"
        "sg2": "sea"
    }

    REGION_GROUP = region_mapping[region]

    matches_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=30"
    matches_response = requests.get(matches_url, headers=HEADERS)

    if matches_response.status_code != 200:
        raise Exception(f"Match fetch failed: {matches_response.status_code}, {matches_response.text}")

    matches_ids = matches_response.json()
    for match_id in matches_ids:
        match_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        match_data = requests.get(match_url, headers=HEADERS).json()
        save_data_to_s3(match_id, match_data)

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    name = body.get("gameName")
    tagline = body.get("tagLine")
    region = body.get("region")

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
