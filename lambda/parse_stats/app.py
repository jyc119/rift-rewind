import json
import os
import boto3
import collections
from statistics import mean

s3 = boto3.client("s3")

# Environment variables (set in Lambda or .env)
BUCKET = os.getenv("S3_BUCKET", "rift-rewind-bucket")
PREFIX_RAW = os.getenv("RAW_PREFIX", "match/MonsterMKE/")
PREFIX_PROCESSED = os.getenv("PROCESSED_PREFIX", "processed/MonsterMKE/")
SUMMONER_NAME = os.getenv("SUMMONER_NAME", "Monster")
PUID = "HdWsPi1r1hpcj_yBMpwelFAOrkO2UteG3JT5PpTyaaiUmdqo_2mUO0k84wMhMBdIhEXcYvntrNyMtw"

def load_matches():
    """Load all raw match JSONs from S3"""
    objs = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX_RAW)
    matches = []
    for item in objs.get("Contents", []):
        body = s3.get_object(Bucket=BUCKET, Key=item["Key"])["Body"].read()
        matches.append(json.loads(body))
    return matches


def extract_stats(matches):
    """Extract only the essential stats for our summoner"""
    """
    return a hashmap of role to player data
    """
    # player = next(
    #     (p for p in match["info"]["participants"] if p["summonerName"].lower() == SUMMONER_NAME.lower()),
    #     None
    # )

    roleToData = collections.defaultdict(list)

    for match in matches:
        for participant in match["info"]["participants"]:
            if participant["puuid"] == PUID:
                # print(participant["individualPosition"])
                roleToData[participant["individualPosition"]].append(participant)

    # print(len(roleToData))
    # print(len(roleToData["TOP"]))
    # print(len(roleToData["JUNGLE"]))
    # print(len(roleToData["MIDDLE"]))
    # print(len(roleToData["BOTTOM"]))
    # print(len(roleToData["UTILITY"]))

    return roleToData
    
    # return {
    #     "kills": player["kills"],
    #     "deaths": player["deaths"],
    #     "assists": player["assists"],
    #     "visionScore": player.get("visionScore", 0),
    #     "win": player["win"]
    # }

# def aggregate(matches):
#     """Compute winrate, avg KDA, and avg vision score"""
#     valid = [m for m in matches if m]
#     if not valid:
#         print("not valid to aggregate")
#         return {}

#     wins = sum(1 for m in valid if m["win"])
#     kills = [m["kills"] for m in valid]
#     deaths = [m["deaths"] for m in valid]
#     assists = [m["assists"] for m in valid]
#     vision = [m["visionScore"] for m in valid]

#     print(len(valid))
#     print(round(100 * wins / len(valid), 1))
#     print(round((mean(kills) + mean(assists)) / max(1, mean(deaths)), 2))
#     print(round(mean(vision), 1))

#     return {
#         "total_matches": len(valid),
#         "winrate": round(100 * wins / len(valid), 1),
#         "avg_kda": round((mean(kills) + mean(assists)) / max(1, mean(deaths)), 2),
#         "avg_vision": round(mean(vision), 1)
#     }

def aggregate(matches):
    """Compute winrate, avg KDA, and avg vision score"""
    valid = [m for m in matches if m]
    if not valid:
        print("not valid to aggregate")
        return {}

    wins = sum(1 for m in valid if m["win"])
    kills = [m["kills"] for m in valid]
    deaths = [m["deaths"] for m in valid]
    assists = [m["assists"] for m in valid]
    vision = [m["visionScore"] for m in valid]

    print(len(valid))
    print(round(100 * wins / len(valid), 1))
    print(round((mean(kills) + mean(assists)) / max(1, mean(deaths)), 2))
    print(round(mean(vision), 1))

    return {
        "total_matches": len(valid),
        "winrate": round(100 * wins / len(valid), 1),
        "avg_kda": round((mean(kills) + mean(assists)) / max(1, mean(deaths)), 2),
        "avg_vision": round(mean(vision), 1)
    }


def save_to_s3(data):
    """Save processed stats to S3"""
    key = f"{PREFIX_PROCESSED}summary.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
        Metadata={
            "phase": "processed",
            "player": SUMMONER_NAME,
            "type": "summary"
        },
        Tagging="rift-rewind-hackathon=2025"
    )
    print(f"✅ Saved summary to s3://{BUCKET}/{key}")

def lambda_handler(event=None, context=None):
    """Main Lambda entry point"""
    print("🔍 Loading matches...")
    raw_matches = load_matches()

    print(f"Loaded {len(raw_matches)} matches from S3.")

    extract_stats(raw_matches)

    # parsed = [extract_stats(m) for m in raw_matches]
    # result = aggregate(parsed)

    # if result == {}:
    #     print("ERROR")
    #     return {}
    # save_to_s3(result)

    # return {"statusCode": 200, "body": json.dumps(result)}

if __name__ == "__main__":
    lambda_handler()
