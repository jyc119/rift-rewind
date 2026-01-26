import json
import os
import urllib3
import boto3

S3_BUCKET = "rift-rewind-bucket"
RIOT_API_KEY = os.environ["RIOT_API_KEY"]
HEADERS = {"X-Riot-Token": RIOT_API_KEY}

s3 = boto3.client("s3")
http = urllib3.PoolManager()

def save_data_to_s3(match_id, match_data, name, tagline):
    player_name = f"{name}#{tagline}"
    key = f"match/{player_name}/{match_id}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(match_data),
        ContentType="application/json"
    )
    print(f"Saved {match_id} to s3://{S3_BUCKET}/{key}")

def save_matches(name, tagline, puuid, region):
    region_mapping = {
        "na1": "americas",
        "euw1": "europe",
        "sg2": "sea",   # keep if you're using SEA routing; otherwise map to "asia"
    }

    region = (region or "").lower()
    REGION_GROUP = region_mapping.get(region)
    if not REGION_GROUP:
        raise Exception(f"Unsupported routingRegion '{region}'. Add it to region_mapping.")

    matches_url = (
        f"https://{REGION_GROUP}.api.riotgames.com"
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=30"
    )

    matches_response = http.request("GET", matches_url, headers=HEADERS)

    if matches_response.status != 200:
        raise Exception(f"Match ID fetch failed: {matches_response.status}, {matches_response.data[:200]}")

    match_ids = json.loads(matches_response.data.decode("utf-8"))

    for match_id in match_ids:
        match_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        match_resp = http.request("GET", match_url, headers=HEADERS)

        if match_resp.status != 200:
            print(f"Skipping {match_id}: {match_resp.status}")
            continue

        match_data = json.loads(match_resp.data.decode("utf-8"))
        save_data_to_s3(match_id, match_data, name, tagline)

def lambda_handler(event, context):
    for record in event.get("Records", []):
        body = json.loads(record["body"])
        save_matches(
            body["gameName"],
            body["tagLine"],
            body["puuid"],
            body["routingRegion"],
        )

    return {"statusCode": 200, "body": json.dumps({"ok": True})}
