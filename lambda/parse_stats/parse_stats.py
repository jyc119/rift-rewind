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
    """Extract player data grouped by role"""
    roleToData = collections.defaultdict(list)

    for match in matches:
        for participant in match["info"]["participants"]:
            if participant["puuid"] == PUID:
                role = participant["individualPosition"]
                roleToData[role].append(participant)

    return roleToData


def aggregate(matches):
    """Compute aggregated stats for a list of participant data"""
    if not matches:
        return {
            "total_matches": 0,
            "winrate": 0,
            "avg_kda": 0,
            "avg_vision": 0
        }

    wins = sum(1 for m in matches if m["win"])
    kills = [m["kills"] for m in matches]
    deaths = [m["deaths"] for m in matches]
    assists = [m["assists"] for m in matches]
    vision = [m["visionScore"] for m in matches]

    return {
        "total_matches": len(matches),
        "winrate": round(100 * wins / len(matches), 1),
        "avg_kda": round((mean(kills) + mean(assists)) / max(1, mean(deaths)), 2),
        "avg_vision": round(mean(vision), 1)
    }


def build_role_summary(roleToData):
    """Attach per-role aggregate summaries with simplified match data"""
    roleSummary = {}

    for role, playerMatches in roleToData.items():
        summary = aggregate(playerMatches)

        # Extract only the relevant stats for each match
        match_data = []
        for m in playerMatches:
            kills = m.get("kills", 0)
            deaths = m.get("deaths", 0)
            assists = m.get("assists", 0)
            vision = m.get("visionScore", 0)

            # Compute KDA safely
            kda = round((kills + assists) / max(1, deaths), 2)

            match_data.append({
                "kills": kills,
                "deaths": deaths,
                "kda": kda,
                "assists": assists,
                "visionScore": vision
            })

        roleSummary[role] = {
            "matches": match_data,
            "summary": summary
        }

    return roleSummary



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

    print("📊 Extracting stats by role...")
    roleToData = extract_stats(raw_matches)

    print("📈 Aggregating per-role summaries...")
    summary = build_role_summary(roleToData)

    save_to_s3(summary)
    return {"statusCode": 200, "body": json.dumps(summary)}


if __name__ == "__main__":
    lambda_handler()
