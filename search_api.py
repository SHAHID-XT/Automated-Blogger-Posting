import requests
import os
import random
from datetime import datetime, timedelta
from urllib.parse import urlparse
from dotenv import load_dotenv

class GoogleCustomSearch:
    def __init__(self, used_links_file="used_links.txt"):
        load_dotenv()
        self.api_key = os.getenv("search_api")
        self.cx = os.getenv("CX")
        self.used_links_file = used_links_file
        self.used_links = self._load_used_links()
        
        # Domains to skip
        self.skip_domains = {
            "reddit.com",
            "www.reddit.com",
            "twitter.com",
            "www.twitter.com",
            "facebook.com",
            "www.facebook.com",
            "instagram.com",
            "www.instagram.com",
            "linkedin.com",
            "www.linkedin.com",
            # Add more domains you want to skip here
        }

    def _load_used_links(self):
        if os.path.exists(self.used_links_file):
            with open(self.used_links_file, "r") as f:
                return set(line.strip() for line in f.readlines())
        return set()

    def _save_used_link(self, link):
        with open(self.used_links_file, "a") as f:
            f.write(link + "\n")
        self.used_links.add(link)

    def _get_date_range(self, days=2):
        today = datetime.utcnow()
        past_date = today - timedelta(days=days)
        return past_date.strftime("%Y%m%d"), today.strftime("%Y%m%d")

    def _is_article_url(self, url):
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        domain = parsed.netloc.lower()

        # Skip domains in skip list
        if domain in self.skip_domains:
            return False

        # Skip .gov and .edu domains
        if domain.endswith(".gov") or domain.endswith(".edu"):
            return False

        # Skip URLs without path (likely homepage)
        if not path:
            return False

        # Skip if path is too short (likely category or section page)
        if len(path) < 40:
            return False

        # Check if path contains digits (likely date) or multiple segments
        if any(char.isdigit() for char in path):
            return True
        if path.count("/") >= 1:
            return True

        # Check common page extensions
        if path.endswith(('.html', '.htm', '.php', '.asp')):
            return True

        return False

    def search_one_unique(self, query, days=2):
        start_date, end_date = self._get_date_range(days)
        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?q={query}&cx={self.cx}&key={self.api_key}"
            f"&sort=date:r:{start_date}:{end_date}"
        )
        response = requests.get(url)
        response.raise_for_status()
        items = response.json().get("items", [])

        fresh_items = [item for item in items 
                       if item['link'] not in self.used_links 
                       and self._is_article_url(item['link'])]

        if not fresh_items:
            return None

        selected = random.choice(fresh_items)
        self._save_used_link(selected['link'])
        return selected

if __name__ == "__main__":
    gcs = GoogleCustomSearch()
    keyword = "salman khan"
    result = gcs.search_one_unique(keyword)

    if result:
        print(f"\n📝 {result['title']}\n🔗 {result['link']}")
    else:
        print("✅ No new unique article results available.")
