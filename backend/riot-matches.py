import requests
import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
S3_BUCKET = "rift-rewind-bucket"

GAME_NAME = "Monster"
TAG_LINE = "MKE"
REGION_GROUP = "europe" 

s3 = boto3.client("s3")

def save_data_to_s3(match_id, match_data):
    player_name = GAME_NAME+TAG_LINE
    key = f"raw/{player_name}/{match_id}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(match_data),
        ContentType="application/json"
    )
    print(f"Saved {match_id} to s3://{S3_BUCKET}/{key}")
    

def main():
    puuid = "HdWsPi1r1hpcj_yBMpwelFAOrkO2UteG3JT5PpTyaaiUmdqo_2mUO0k84wMhMBdIhEXcYvntrNyMtw"
    matches_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5"
    matches_response = requests.get(matches_url, headers=HEADERS)

    if matches_response.status_code != 200:
        raise Exception(f"Match fetch failed: {matches_response.status_code}, {matches_response.text}")

    matches_ids = matches_response.json()
    for match_id in matches_ids:
        match_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        match_data = requests.get(match_url, headers=HEADERS).json()
        save_data_to_s3(match_id, match_data)

if __name__ == "__main__":
    main()

# --- Step 1: Get PUUID from Riot ID ---
# account_url = f"https://{REGION_GROUP}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"
# account_response = requests.get(account_url, headers=HEADERS)

# if account_response.status_code != 200:
#     raise Exception(f"Account lookup failed: {account_response.status_code}, {account_response.text}")

# account_data = account_response.json()
# puuid = account_data["puuid"]

# # --- Step 2: Get Recent Match IDs ---
# matches_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5"
# matches_response = requests.get(matches_url, headers=HEADERS)

# if matches_response.status_code != 200:
#     raise Exception(f"Match fetch failed: {matches_response.status_code}, {matches_response.text}")

# matches = matches_response.json()
# print("Recent matches:", matches)

# # --- Step 3: Fetch One Match Example ---
# if matches:
#     match_id = matches[0]
#     match_url = f"https://{REGION_GROUP}.api.riotgames.com/lol/match/v5/matches/{match_id}"
#     match_data = requests.get(match_url, headers=HEADERS).json()
#     print(f"\nFirst match ({match_id}) details snippet:")
#     print(match_data["info"]["participants"][0])  # print one participant’s stats
