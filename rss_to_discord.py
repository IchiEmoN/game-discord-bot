import feedparser
import os
import requests
from datetime import datetime

# ゲーム別複数RSS候補URL
game_feeds = {
    "VALORANT": [
        "https://game8.jp/feeds/feed_345.xml",
        "https://www.reddit.com/r/VALORANT/.rss",
        "https://www.riotgames.com/en/rss/news"
    ],
    "APEX": [
        "https://store.steampowered.com/feeds/news/app/1172470",
        "https://www.reddit.com/r/apexlegends/.rss"
    ],
    "TARKOV": [
        "https://www.escapefromtarkov.com/news/rss",
        "https://www.reddit.com/r/EscapefromTarkov/.rss",
        "https://steamcommunity.com/app/629910/discussions/rss/"
    ],
    "LOL": [
        "https://www.leagueoflegends.com/ja-jp/news/feed/",
        "https://www.reddit.com/r/leagueoflegends/.rss",
        "https://na.leagueoflegends.com/en/rss/news/"
    ],
    "OVERWATCH": [
        "https://www.reddit.com/r/Overwatch/.rss",
        "https://www.blizzard.com/en-us/news/rss/"
    ],
    "DBD": [
        "https://deadbydaylight.com/news/rss",
        "https://www.reddit.com/r/deadbydaylight/.rss"
    ],
    "MONHUN": [
        "https://rsshub.app/twitter/user/MH_official_JP",
        "https://www.reddit.com/r/MonsterHunter/.rss"
    ],
    "MAHJONG_SOUL": [
        "https://rsshub.app/twitter/user/MahjongSoul_JP",
        "https://www.reddit.com/r/mahjongsoul/.rss"
    ],
    "SF6": [
        "https://rsshub.app/twitter/user/StreetFighterJA",
        "https://www.reddit.com/r/StreetFighter/.rss"
    ],
}

NOTIFIED_FILE = "notified_urls.txt"

def load_notified():
    try:
        with open(NOTIFIED_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def save_notified(url):
    with open(NOTIFIED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def send_discord(webhook_url, game, title, url):
    if not webhook_url:
        print(f"[Warning] Webhook URL not set for {game}")
        return
    data = {
        "content": f"📰 **[{game}]** {title}\n{url}"
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
        if response.status_code != 204:
            print(f"[Error] Discord送信失敗: {response.status_code} {response.text}")
    except Exception as e:
        print(f"[Error] Discord送信例外: {e}")

def main():
    notified = load_notified()

    for game, rss_urls in game_feeds.items():
        webhook = os.environ.get(f"HOOK_{game.upper()}")
        if not webhook:
            print(f"[Skip] {game} のWebhookが設定されていません。")
            continue

        for rss_url in rss_urls:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:5]:  # 各RSS最新5件だけ処理
                link = entry.link
                if link not in notified:
                    title = entry.title
                    send_discord(webhook, game, title, link)
                    save_notified(link)

if __name__ == "__main__":
    main()
