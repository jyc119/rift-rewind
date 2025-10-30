import boto3
import json

# Create the Bedrock runtime client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Claude 3.5 Sonnet model ID
model_id = "arn:aws:bedrock:us-east-1:029331795967:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0"

# Sample prompt
prompt = """You are an expert League of Legends analyst.
Summarize this player's season performance:
"This player maintained a 62% win rate with strong consistency and map awareness."
"""

try:
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",  # ✅ required
            "max_tokens": 300,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    print("✅ Success!\n")
    print(result["content"][0]["text"])

except Exception as e:
    print("❌ Failed to invoke model:")
    print(e)
