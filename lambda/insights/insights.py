import json
import os
import boto3
import datetime
from statistics import mean
from decimal import Decimal

s3 = boto3.client("s3")
dynamo = boto3.resource("dynamodb")
table = dynamo.Table("rift-rewind-recaps")

BUCKET = os.getenv("S3_BUCKET", "rift-rewind-bucket")
PREFIX_PROCESSED = os.getenv("PREFIX_PROCESSED", "processed/")
PREFIX_INSIGHTS = os.getenv("PREFIX_INSIGHTS", "insights/")
SUMMONER_NAME = os.getenv("SUMMONER_NAME", "MonsterMKE")

def list_processed_summaries():
    response = s3.list_objects_v2(
        Bucket=BUCKET,
        Prefix=f"{PREFIX_PROCESSED}{SUMMONER_NAME}/"
    )

    return [obj["Key"] for obj in response.get("Contents", [])
            if obj["Key"].endswith("summary.json")]

def load_summary(key):
    body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return json.loads(body)

def aggregate_summaries(summaries):
    winrates = [s["winrate"] for s in summaries]
    kdas = [s["avg_kda"] for s in summaries]
    visions = [s["avg_vision"] for s in summaries]
    totals = [s["total_matches"] for s in summaries]

    total_matches = sum(totals)
    avg_winrate = round(mean(winrates), 1)
    avg_kda = round(mean(kdas), 2)
    avg_vision = round(mean(visions), 1)

    return {
        "player": SUMMONER_NAME,
        "total_matches": total_matches,
        "avg_winrate": avg_winrate,
        "avg_kda": avg_kda,
        "avg_vision": avg_vision
    }

def upload_insights(data):
    key = f"{PREFIX_INSIGHTS}{SUMMONER_NAME}/season_summary.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
        Metadata={"phase": "insights", "player": SUMMONER_NAME},
        Tagging="rift-rewind-hackathon-2025"
    )
    print(f"Saved aggregated insights to s3://{BUCKET}/{key}")

def save_to_dynamo(summary):
    item = {
        "playerId": summary["player"],
        "updatedAt": datetime.datetime.now().isoformat(),
        "s3Key": f"insights/{summary['player']}/season_summary.json",
        "winrate": Decimal(str(summary["avg_winrate"])),
        "avgKda": Decimal(str(summary["avg_kda"])),
        "avgVision": Decimal(str(summary["avg_vision"]))
    }

    table.put_item(Item=item)
    print(f"Saved metadata for {summary['player']} to DynamoDB.")

def lambda_handler(event=None, context=None):
    keys = list_processed_summaries()
    if not keys:
        print("No processed summaries found")
        return {"statusCode": 404, "body": "No processed summaries"}

    summaries = [load_summary(k) for k in keys]
    aggregated_data = aggregate_summaries(summaries)
    upload_insights(aggregated_data)
    save_to_dynamo(aggregated_data)

    return {"statusCode": 200, "body": json.dumps(aggregated_data)}

if __name__ == "__main__":
    lambda_handler()