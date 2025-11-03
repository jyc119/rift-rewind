import boto3
import json
import io
import matplotlib.pyplot as plt
from collections import defaultdict

# --- AWS Config ---
s3 = boto3.client("s3", region_name="us-east-1")
BUCKET = "rift-rewind-bucket"

# --- Load player data from S3 ---
def load_player_data(summoner_name):
    """Download processed JSON data from S3."""
    key = f"processed/{summoner_name}/summary.json"
    response = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(response["Body"].read().decode("utf-8"))

# --- Plot Champion Win/Loss Summary ---
def plot_winloss_chart(role, role_data):
    champ_stats = defaultdict(lambda: {"matches": 0, "wins": 0, "losses": 0})

    # Aggregate stats
    for match in role_data["matches"]:
        champ = match["championName"]
        champ_stats[champ]["matches"] += 1
        # Replace this logic later with actual win/loss field
        if match["kda"] > 2.5:
            champ_stats[champ]["wins"] += 1
        else:
            champ_stats[champ]["losses"] += 1

    # Sort by most played
    champs_sorted = sorted(champ_stats.items(), key=lambda x: x[1]["matches"], reverse=True)
    y_labels = [c for c, _ in champs_sorted]
    y_pos = range(len(champs_sorted))

    WIN_COLOR = "#3b82f6"
    LOSS_COLOR = "#ef4444"

    plt.figure(figsize=(7, 4))
    for i, (champ, stats) in enumerate(champs_sorted):
        wins = stats["wins"]
        losses = stats["losses"]
        total = wins + losses
        winrate = (wins / total * 100) if total > 0 else 0

        plt.barh(i, wins, color=WIN_COLOR)
        plt.barh(i, losses, left=wins, color=LOSS_COLOR)
        plt.text(wins / 2, i, f"{wins}W", va="center", ha="center", color="white", fontsize=9)
        plt.text(wins + losses / 2, i, f"{losses}L", va="center", ha="center", color="white", fontsize=9)
        plt.text(wins + losses + 0.3, i, f"{winrate:.0f}%", va="center", ha="left", color="gray")

    plt.yticks(y_pos, y_labels)
    plt.gca().invert_yaxis()
    plt.xlabel("Games")
    plt.title(f"{role} – Champion Win/Loss Summary")
    plt.tight_layout()

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

# --- Plot KDA per Match Chart ---
def plot_kda_chart(role, role_data):
    champ_kdas = defaultdict(list)

    for match in role_data["matches"]:
        champ_kdas[match["championName"]].append(match["kda"])

    plt.figure(figsize=(7, 4))
    for champ, kdas in champ_kdas.items():
        plt.plot(range(1, len(kdas)+1), kdas, marker="o", label=champ)

    plt.title(f"{role} – KDA per Match")
    plt.xlabel("Match #")
    plt.ylabel("KDA")
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf

# --- Upload helper ---
def upload_chart_to_s3(buffer, key):
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=buffer.getvalue(),
        ContentType="image/png"
    )

# --- Main function ---
def main():
    summoner_name = "MonsterMKE"
    data = load_player_data(summoner_name)

    for role, role_data in data.items():
        winloss_buf = plot_winloss_chart(role, role_data)
        kda_buf = plot_kda_chart(role, role_data)

        upload_chart_to_s3(winloss_buf, f"charts/{summoner_name}/{role}_winloss.png")
        upload_chart_to_s3(kda_buf, f"charts/{summoner_name}/{role}_kda.png")

        print(f"✅ Uploaded charts for {role}")

if __name__ == "__main__":
    main()
