import feedparser
import requests
import os

game_feeds = {
    "VALORANT": {
        "rss": "https://playvalorant.com/ja-jp/news/",
        "webhook": os.environ.get("HOOK_VALORANT")
    },
    "APEX": {
        "rss": "https://www.ea.com/ja-jp/games/apex-legends/news",
        "webhook": os.environ.get("HOOK_APEX")
    },
    "TARKOV": {
        "rss": "https://www.escapefromtarkov.com/news",
        "webhook": os.environ.get("HOOK_TARKOV")
    },
    "LOL": {
        "rss": "https://www.leagueoflegends.com/ja-jp/news/",
        "webhook": os.environ.get("HOOK_LOL")
    },
    "OVERWATCH": {
        "rss": "https://overwatch.blizzard.com/ja-jp/news/",
        "webhook": os.environ.get("HOOK_OVERWATCH")
    },
    "DBD": {
        "rss": "https://deadbydaylight.com/news/rss",
        "webhook": os.environ.get("HOOK_DBD")
    },
    "MONHUN": {
        "rss": "https://nitter.net/MH_official_JP/rss",
        "webhook": os.environ.get("HOOK_MONHUN")
    },
    "MAHJONG_SOUL": {
        "rss": "https://nitter.net/MahjongSoul_JP/rss",
        "webhook": os.environ.get("HOOK_MAJAN")
    },
    "SF6": {
        "rss": "https://nitter.net/StreetFighterJA/rss",
        "webhook": os.environ.get("HOOK_SF6")
    }
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
        print(f"Error sending to Discord: {e}")

def load_notified():
    try:
        with open(NOTIFIED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def save_notified(url):
    with open(NOTIFIED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def main():
    notified = load_notified()

    # 🎯 テスト通知（毎回送られる）
    for game, info in game_feeds.items():
        if info["webhook"]:
            send_discord(info["webhook"], game, "✅ 通知Botが正常に起動しました（テスト）", "https://example.com")
    
    # 📡 通常のRSSチェック
    for game, info in game_feeds.items():
        feed = feedparser.parse(info["rss"])
        webhook = info["webhook"]
        if not webhook:
            print(f"No webhook URL for {game}, skipping")
            continue
        for entry in feed.entries[:1]:  # 最新1件だけ通知
            link = entry.link
            if link not in notified:
                title = entry.title
                send_discord(webhook, game, title, link)
                save_notified(link)

if __name__ == "__main__":
    main()
