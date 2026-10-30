
import feedparser
import json
import os
from datetime import datetime, timezone, timedelta

RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=ngh%E1%BB%89+L%E1%BB%84"
    "+OR+%22%C4%90%C6%AF%E1%BB%A2C+NGH%E1%BB%88+KH%C3%94NG"
    "+%C4%90I+L%C3%80M%22"
    "+OR+%22B%E1%BB%99+N%E1%BB%99i+v%E1%BB%A5%22+ngh%E1%BB%89"
    "&hl=vi&gl=VN&ceid=VN:vi"
)

OUTPUT_FILE = "data/holidays.json"

def fetch_and_save():
    print("Dang lay tin tuc Google News RSS...")

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        raise RuntimeError(
            "RSS khong co bai viet hoac khong the ket noi. "
            "Khong ghi de file JSON cu."
        )

    now = datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=7))
    )

    data = {
        "updated_at": now.strftime("%Y-%m-%d %H:%M:%S GMT+7"),
        "title": feed.feed.get("title", "Tin tuc nghi le Viet Nam"),
        "total": len(feed.entries),
        "items": []
    }

    for entry in feed.entries:
        source = entry.get("source", {})

        item = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "pubDate": entry.get("published", ""),
            "source": source.get("title", ""),
            "sourceUrl": source.get("href", "")
        }

        data["items"].append(item)

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("================================")
    print(f"Cap nhat thanh cong: {len(data['items'])} bai viet")
    print(f"Thoi gian: {data['updated_at']}")
    print(f"Luu tai: {OUTPUT_FILE}")
    print("================================")


if __name__ == "__main__":
    fetch_and_save()
