import feedparser
import requests
import os

# ゲーム別に複数のRSSを設定可能に
game_feeds = {
    "VALORANT": [
        "https://game8.jp/feeds/feed_345.xml",
        "https://www.reddit.com/r/VALORANT/.rss",
        "https://rsshub.app/twitter/user/PlayVALORANT"
    ],
    "APEX": [
        "https://www.ea.com/ja-jp/games/apex-legends/news",
        "https://www.reddit.com/r/apexlegends/.rss",
        "https://rsshub.app/twitter/user/playapex"
    ],
    "TARKOV": [
        "https://www.escapefromtarkov.com/news",
        "https://www.reddit.com/r/EscapefromTarkov/.rss"
    ],
    "LOL": [
        "https://www.leagueoflegends.com/ja-jp/news/",
        "https://rsshub.app/twitter/user/LoLJPOfficial"
    ],
    "OVERWATCH": [
        "https://overwatch.blizzard.com/ja-jp/news/",
        "https://rsshub.app/twitter/user/PlayOverwatch"
    ],
    "DBD": [
        "https://deadbydaylight.com/news/rss",
        "https://rsshub.app/twitter/user/DeadByBHVR_JP"
    ],
    "MONHUN": [
        "https://rsshub.app/twitter/user/MH_official_JP"
    ],
    "MAHJONG_SOUL": [
        "https://rsshub.app/twitter/user/MahjongSoul_JP"
    ],
    "SF6": [
        "https://rsshub.app/twitter/user/StreetFighterJA"
    ]
}

NOTIFIED_FILE = "notified_urls.txt"

def send_discord(webhook_url, game, title, url):
    if not webhook_url:
        return
    data = {
        "content": f"📰 **[{game}]** {title}\n{url}"
    }
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(webhook_url, json=data, headers=headers, timeout=10)
    except Exception as e:
        print(f"Error sending to Discord for {game}: {e}")

def load_notified():
    try:
        with open(NOTIFIED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def save_notified(item_id):
    with open(NOTIFIED_FILE, "a", encoding="utf-8") as f:
        f.write(item_id + "\n")

def main():
    notified = load_notified()

    for game, rss_list in game_feeds.items():
        webhook = os.environ.get(f"HOOK_{game.upper()}")
        if not webhook:
            print(f"[Skip] {game} のWebhookが未設定です。")
            continue

        for rss_url in rss_list:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:5]:  # 最新5件をチェック
                unique_id = getattr(entry, "id", None) or f"{entry.title}|{entry.link}"
                if unique_id in notified:
                    continue
                send_discord(webhook, game, entry.title, entry.link)
                save_notified(unique_id)

if __name__ == "__main__":
    main()
