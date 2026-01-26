import os
import json
import requests
import boto3

RIOT_API_KEY = os.environ["RIOT_API_KEY"]
sqs = boto3.client("sqs")
QUEUE_URL = os.environ["INGEST_QUEUE_URL"]

ROUTING_REGIONS = ["americas", "europe", "asia"]  # you can extend later

def euqueue_ingest_job(puuid: str, region: str, name: str, tagline: str):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({
            "puuid": puuid,
            "routingRegion": region,
            "gameName": name,
            "tagLine": tagline
        })
    )

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    name = body.get("gameName")
    tagline = body.get("tagLine")
    region = body.get("region")

    if not name or not tagline or not region:
        return response(400, {"message": "Missing gameName or tagLine"})

    for region1 in ROUTING_REGIONS:
        url = f"https://{region1}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
        r = requests.get(url, headers={"X-Riot-Token": RIOT_API_KEY})

        if r.status_code == 200:
            data = r.json()

            # save_matches(name, tagline, data["puuid"], region)
            euqueue_ingest_job(data["puuid"], region, name, tagline)

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
