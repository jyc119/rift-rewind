import boto3
import json
import os

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
s3 = boto3.client("s3")

# Claude 3.5 Sonnet model ID
model_id = "arn:aws:bedrock:us-east-1:029331795967:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0"
PROMPT_PATH = "lambda/insights/prompts/recap_template.txt"

def load_prompt_template():
    with open(PROMPT_PATH, "r") as f:
        return f.read()

def format_prompt(player_data):
    template = load_prompt_template()
    return template.replace("{{player_data}}", json.dumps(player_data, indent=2))

def invoke_bedrock(prompt):
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 420,
            "temperature": 0.7,
            "messages": [{"role": "user", "content": prompt}]
        }),
        contentType="application/json",
        accept="application/json"
    )
    return json.loads(response["body"].read())["content"][0]["text"]

def lambda_handler(event=None, context=None):
    # For now: manually feed test data
    player_data = {
        "summonerName": "Monster",
        "matchesPlayed": 120,
        "avgKDA": 3.8,
        "winRate": 0.62,
        "topChampions": ["Ambessa", "Malphite", "Darius"],
        "visionScore": 10.2,
        "damageShare": 0.27,
        "deathsPerGame": 5.6
    }

    prompt = format_prompt(player_data)
    recap = invoke_bedrock(prompt)

    # Store to S3 (example bucket/path)
    s3.put_object(
        Bucket="rift-rewind-bucket",
        Key=f"recaps/{player_data['summonerName']}.json",
        Body=recap.encode("utf-8"),
        ContentType="application/json"
    )

    print("✅ Recap saved successfully!")
    return {"statusCode": 200, "body": recap}

if __name__ == "__main__":
    lambda_handler()
