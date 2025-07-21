import feedparser
import requests
import os

# 各ゲームのRSSフィードとWebhook
game_feeds = {
    "VALORANT": {
        "rss": "https://game8.jp/feeds/feed_345.xml",  # Game8のRSS（非公式）
        "webhook": os.environ.get("HOOK_VALORANT")
    },
    "APEX": {
        "rss": "https://store.steampowered.com/feeds/news/app/1172470",  # Steam公式
        "webhook": os.environ.get("HOOK_APEX")
    },
    "TARKOV": {
        "rss": "https://www.escapefromtarkov.com/news/rss",  # 公式RSS対応（存在確認済み）
        "webhook": os.environ.get("HOOK_TARKOV")
    },
    "LOL": {
        "rss": "https://www.reddit.com/r/leagueoflegends/.rss",  # Reddit（英語圏）
        "webhook": os.environ.get("HOOK_LOL")
    },
    "OVERWATCH": {
        "rss": "https://www.reddit.com/r/Overwatch/.rss",  # Reddit
        "webhook": os.environ.get("HOOK_OVERWATCH")
    },
    "DBD": {
        "rss": "https://deadbydaylight.com/news/rss",  # 公式RSS
        "webhook": os.environ.get("HOOK_DBD")
    },
    "MONHUN": {
        "rss": "https://rsshub.app/twitter/user/MH_official_JP",  # RSSHub
        "webhook": os.environ.get("HOOK_MONHUN")
    },
    "MAHJONG_SOUL": {
        "rss": "https://rsshub.app/twitter/user/MahjongSoul_JP",  # RSSHub
        "webhook": os.environ.get("HOOK_MAJAN")
    },
    "SF6": {
        "rss": "https://rsshub.app/twitter/user/StreetFighterJA",  # RSSHub
        "webhook": os.environ.get("HOOK_SF6")
    }
}

NOTIFIED_FILE = "notified_urls.txt"

# Discordに通知を送る関数
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

# 通知済みURLを読み込む
def load_notified():
    try:
        with open(NOTIFIED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

# 通知済みURLを保存する
def save_notified(url):
    with open(NOTIFIED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

# メイン処理
def main():
    notified = load_notified()

    for game, info in game_feeds.items():
        feed = feedparser.parse(info["rss"])
        webhook = info["webhook"]
        if not webhook:
            print(f"No webhook URL for {game}, skipping")
            continue

        for entry in feed.entries[:1]:  # 最新1件のみチェック
            link = entry.link
            if link not in notified:
                title = entry.title
                send_discord(webhook, game, title, link)
                save_notified(link)

if __name__ == "__main__":
    main()
