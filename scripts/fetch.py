
import feedparser
import json
from datetime import datetime
import os

RSS_URL = "https://news.google.com/rss/search?q=nghỉ+LỄ+OR+%22ĐƯỢC+NGHỈ+KHÔNG+%C4%90I+L%C3%80M%22+OR+%22B%E1%BB%99+N%E1%BB%99i+v%E1%BB%A5%22+nghỉ&hl=vi&gl=VN&ceid=VN:vi"

def fetch_and_save():
    feed = feedparser.parse(RSS_URL)
    
    data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "title": feed.feed.get("title", ""),
        "items": []
    }
    
    for entry in feed.entries:
        item = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "pubDate": entry.get("published", ""),
            "source": entry.get("source", {}).get("title", "") if entry.get("source") else "",
            "sourceUrl": entry.get("source", {}).get("href", "") if entry.get("source") else ""
        }
        data["items"].append(item)
    
    os.makedirs("data", exist_ok=True)
    with open("data/holidays.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Đã cập nhật {len(data['items'])} bài viết")

if __name__ == "__main__":
    fetch_and_save()
