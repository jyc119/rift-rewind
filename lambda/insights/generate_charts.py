import boto3
import json
import io
import matplotlib.pyplot as plt

s3 = boto3.client("s3", region_name="us-east-1")

BUCKET = "rift-rewind-bucket"

def load_player_data(summoner_name):
    """Download processed JSON data from S3."""
    key = f"processed/{summoner_name}/summary.json"
    response = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(response["Body"].read().decode("utf-8"))

def plot_winrate_by_champion(data, summoner_name):
    champs = list(data["winRateByChampion"].keys())
    rates = [v * 100 for v in data["winRateByChampion"].values()]

    plt.figure(figsize=(6, 4))
    plt.bar(champs, rates)
    plt.title(f"Win Rate by Champion – {summoner_name}")
    plt.ylabel("Win Rate (%)")
    plt.ylim(0, 100)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

def plot_kda_trend(data, summoner_name):
    kda = data["kdaOverTime"]

    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(kda) + 1), kda, marker="o", linestyle="-")
    plt.title(f"KDA Trend – {summoner_name}")
    plt.xlabel("Match #")
    plt.ylabel("Average KDA")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

def upload_chart_to_s3(buffer, key):
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=buffer.getvalue(),
        ContentType="image/png"
    )

def main():
    summoner_name = "MonsterMKE"
    data = load_player_data(summoner_name)

    winrate_buf = plot_winrate_by_champion(data, summoner_name)
    kda_buf = plot_kda_trend(data, summoner_name)

    # upload_chart_to_s3(winrate_buf, f"processed/charts/{summoner_name}_winrate.png")
    # upload_chart_to_s3(kda_buf, f"processed/charts/{summoner_name}_kda.png")

    # print("✅ Charts generated and uploaded to S3 successfully!")

if __name__ == "__main__":
    main()
