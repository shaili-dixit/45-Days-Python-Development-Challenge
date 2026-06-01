"""
Static Web Scraper for News Headlines with Keyword Filtering
Scrapes headlines from mock HTML, extracts title/URL/date, filters by keyword, exports CSV.
"""

import csv
import re
from datetime import datetime
from html.parser import HTMLParser

# ── Mock HTML (simulates a real news page) ────────────────────────────────────
MOCK_HTML = """
<!DOCTYPE html>
<html>
<head><title>TechNews Daily</title></head>
<body>
  <div class="news-container">
    <article class="news-item">
      <h2><a href="/tech/python-ai-2024">Python Dominates AI Development in 2024</a></h2>
      <span class="date">2024-11-01</span>
      <p class="summary">Python continues to lead machine learning and AI frameworks worldwide.</p>
    </article>
    <article class="news-item">
      <h2><a href="/tech/quantum-computing-breakthrough">Quantum Computing Hits 1000 Qubit Milestone</a></h2>
      <span class="date">2024-11-03</span>
      <p class="summary">Researchers achieve record-breaking qubit coherence times.</p>
    </article>
    <article class="news-item">
      <h2><a href="/health/ai-medical-diagnosis">AI System Outperforms Doctors in Early Cancer Detection</a></h2>
      <span class="date">2024-11-05</span>
      <p class="summary">A new AI model achieves 97% accuracy in early cancer diagnosis.</p>
    </article>
    <article class="news-item">
      <h2><a href="/tech/rust-lang-growth">Rust Programming Language Adoption Surges</a></h2>
      <span class="date">2024-11-07</span>
      <p class="summary">System-level language Rust sees rapid growth in enterprise adoption.</p>
    </article>
    <article class="news-item">
      <h2><a href="/science/climate-data-ml">Machine Learning Predicts Climate Change Hotspots</a></h2>
      <span class="date">2024-11-09</span>
      <p class="summary">Satellite data combined with ML models improve climate forecasting.</p>
    </article>
    <article class="news-item">
      <h2><a href="/tech/openai-gpt5">OpenAI Announces GPT-5 with Reasoning Improvements</a></h2>
      <span class="date">2024-11-11</span>
      <p class="summary">The latest model shows significant improvements in math and coding tasks.</p>
    </article>
    <article class="news-item">
      <h2><a href="/business/ev-sales-record">Electric Vehicle Sales Break Global Record</a></h2>
      <span class="date">2024-11-12</span>
      <p class="summary">EV adoption reaches 30% of new car sales globally in October 2024.</p>
    </article>
    <article class="news-item">
      <h2><a href="/tech/cybersecurity-ai">AI Tools Now Detect Zero-Day Exploits Faster</a></h2>
      <span class="date">2024-11-14</span>
      <p class="summary">New AI-powered cybersecurity platforms reduce detection time significantly.</p>
    </article>
    <article class="news-item">
      <h2><a href="/science/space-launch-2024">SpaceX Launches Largest Satellite Constellation</a></h2>
      <span class="date">2024-11-15</span>
      <p class="summary">Starlink V3 adds 300 high-capacity satellites in a single launch.</p>
    </article>
    <article class="news-item">
      <h2><a href="/tech/python-web-frameworks">Django and FastAPI Lead Python Web Framework Rankings</a></h2>
      <span class="date">2024-11-17</span>
      <p class="summary">Annual survey reveals developer preferences in Python web development.</p>
    </article>
  </div>
</body>
</html>
"""


class NewsHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = []
        self._current = {}
        self._in_article = False
        self._in_h2 = False
        self._in_a = False
        self._in_date = False
        self._in_summary = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        if tag == 'article' and 'news-item' in cls:
            self._in_article = True
            self._current = {}
        if self._in_article:
            if tag == 'h2':
                self._in_h2 = True
            if tag == 'a' and self._in_h2:
                self._in_a = True
                self._current['url'] = 'https://technewsdaily.com' + attrs_dict.get('href', '')
            if tag == 'span' and 'date' in cls:
                self._in_date = True
            if tag == 'p' and 'summary' in cls:
                self._in_summary = True

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self._in_a:
            self._current['title'] = data
        if self._in_date:
            self._current['date'] = data
        if self._in_summary:
            self._current['summary'] = data

    def handle_endtag(self, tag):
        if tag == 'a':
            self._in_a = False
        if tag == 'h2':
            self._in_h2 = False
        if tag == 'span':
            self._in_date = False
        if tag == 'p':
            self._in_summary = False
        if tag == 'article' and self._in_article:
            if self._current.get('title'):
                self.articles.append(dict(self._current))
            self._in_article = False
            self._current = {}


def scrape(html):
    parser = NewsHTMLParser()
    parser.feed(html)
    return parser.articles


def filter_by_keyword(articles, keyword):
    if not keyword:
        return articles
    kw = keyword.lower()
    return [
        a for a in articles
        if kw in a.get('title', '').lower()
        or kw in a.get('summary', '').lower()
    ]


def export_to_csv(articles, filename=None):
    if not filename:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"news_export_{ts}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url', 'date', 'summary'])
        writer.writeheader()
        writer.writerows(articles)
    print(f"  ✓ Exported {len(articles)} articles to '{filename}'")
    return filename


def print_articles(articles, title="News Headlines"):
    print(f"\n  {'═'*65}")
    print(f"  {title} ({len(articles)} article(s))")
    print(f"  {'═'*65}")
    if not articles:
        print("  No articles found.")
        return
    for i, a in enumerate(articles, 1):
        print(f"\n  {i}. {a.get('title', 'N/A')}")
        print(f"     URL  : {a.get('url', 'N/A')}")
        print(f"     Date : {a.get('date', 'N/A')}")
        print(f"     {a.get('summary', '')[:80]}")
    print(f"\n  {'═'*65}")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   News Headline Scraper v1.0             ║")
    print("╚══════════════════════════════════════════╝")

    print("\n  Parsing mock HTML page...")
    articles = scrape(MOCK_HTML)
    print_articles(articles, "All Headlines")

    keywords = ['python', 'AI', 'quantum']
    for kw in keywords:
        filtered = filter_by_keyword(articles, kw)
        print_articles(filtered, f"Articles matching '{kw}'")

    export_to_csv(articles)

    # Interactive
    while True:
        kw = input("\n  Filter by keyword (or Enter to skip, 'q' to quit): ").strip()
        if kw.lower() == 'q':
            break
        results = filter_by_keyword(articles, kw) if kw else articles
        print_articles(results, f"Results for '{kw}'" if kw else "All Articles")
        if results:
            save = input("  Export results to CSV? (y/n): ").strip().lower()
            if save == 'y':
                export_to_csv(results)


if __name__ == "__main__":
    main()
