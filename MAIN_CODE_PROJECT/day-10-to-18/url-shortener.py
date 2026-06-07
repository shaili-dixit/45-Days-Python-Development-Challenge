"""
URL Shortener Simulator with Access Tracking and Persistence
Generates short codes via hashing, stores mappings in JSON, tracks access counts.
"""

import json
import os
import hashlib
import string
import random
from datetime import datetime

DATA_FILE = "url_store.json"
BASE_URL = "https://short.ly/"
CODE_LENGTH = 6


class URLShortener:
    def __init__(self):
        self.urls = {}        # short_code -> {long_url, created, hits, last_accessed}
        self.reverse = {}     # long_url -> short_code
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE) as f:
                    data = json.load(f)
                    self.urls = data.get('urls', {})
                    self.reverse = data.get('reverse', {})
            except:
                pass

    def save(self):
        with open(DATA_FILE, 'w') as f:
            json.dump({'urls': self.urls, 'reverse': self.reverse}, f, indent=2)

    def _generate_code(self, url):
        """Generate a short code using MD5 hash of the URL."""
        hash_bytes = hashlib.md5(url.encode()).hexdigest()
        # Map hex chars to alphanumeric base-62 style
        chars = string.ascii_letters + string.digits
        code = ''.join(chars[int(hash_bytes[i*2:(i*2)+2], 16) % len(chars)]
                       for i in range(CODE_LENGTH))
        return code

    def _resolve_collision(self, base_code, url):
        """If code collision, append random suffix."""
        code = base_code
        attempt = 0
        while code in self.urls and self.urls[code]['long_url'] != url:
            salt = random.choice(string.ascii_lowercase)
            code = base_code[:CODE_LENGTH - 1] + salt
            attempt += 1
            if attempt > 10:
                code = ''.join(random.choices(string.ascii_letters + string.digits, k=CODE_LENGTH))
        return code

    def shorten(self, long_url, custom_code=None):
        """Create a short URL."""
        if not long_url.startswith(('http://', 'https://')):
            long_url = 'https://' + long_url

        # Return existing if already shortened
        if long_url in self.reverse:
            code = self.reverse[long_url]
            print(f"  ↩  Already exists: {BASE_URL}{code}")
            return f"{BASE_URL}{code}"

        if custom_code:
            code = custom_code.strip()
            if code in self.urls:
                print(f"  ✗ Custom code '{code}' already taken.")
                return None
        else:
            code = self._generate_code(long_url)
            code = self._resolve_collision(code, long_url)

        self.urls[code] = {
            'long_url': long_url,
            'short_url': f"{BASE_URL}{code}",
            'created': datetime.now().isoformat(),
            'hits': 0,
            'last_accessed': None,
        }
        self.reverse[long_url] = code
        self.save()
        print(f"  ✓ Shortened: {long_url[:50]}{'...' if len(long_url)>50 else ''}")
        print(f"       → {BASE_URL}{code}")
        return f"{BASE_URL}{code}"

    def resolve(self, short_url):
        """Look up a short URL and return the long URL."""
        code = short_url.replace(BASE_URL, '').strip('/')
        if code not in self.urls:
            print(f"  ✗ Short URL '{short_url}' not found.")
            return None
        entry = self.urls[code]
        entry['hits'] += 1
        entry['last_accessed'] = datetime.now().isoformat()
        self.save()
        print(f"  ↗  Resolving: {BASE_URL}{code}")
        print(f"       → {entry['long_url']}")
        return entry['long_url']

    def delete(self, short_url):
        code = short_url.replace(BASE_URL, '').strip('/')
        if code in self.urls:
            long = self.urls[code]['long_url']
            del self.urls[code]
            self.reverse.pop(long, None)
            self.save()
            print(f"  ✓ Deleted: {BASE_URL}{code}")
        else:
            print(f"  ✗ Not found: {short_url}")

    def stats(self, short_url):
        code = short_url.replace(BASE_URL, '').strip('/')
        if code not in self.urls:
            print(f"  ✗ Not found.")
            return
        e = self.urls[code]
        print(f"\n  Statistics for: {BASE_URL}{code}")
        print(f"  Long URL    : {e['long_url'][:60]}")
        print(f"  Created     : {e['created'][:19]}")
        print(f"  Hits        : {e['hits']}")
        print(f"  Last access : {(e['last_accessed'] or 'Never')[:19]}")

    def top_links(self, n=10):
        ranked = sorted(self.urls.items(), key=lambda x: -x[1]['hits'])[:n]
        print(f"\n  Top {n} Most Accessed Links:")
        print(f"  {'─'*65}")
        print(f"  {'Code':<10} {'Hits':>6}  {'URL'}")
        print(f"  {'─'*65}")
        for code, entry in ranked:
            url_preview = entry['long_url'][:45] + ('...' if len(entry['long_url']) > 45 else '')
            print(f"  {code:<10} {entry['hits']:>6}  {url_preview}")
        print(f"  {'─'*65}")

    def list_all(self):
        if not self.urls:
            print("  No URLs stored.")
            return
        print(f"\n  All Stored URLs ({len(self.urls)}):")
        print(f"  {'─'*70}")
        print(f"  {'Short':<30} {'Hits':>6}  {'Long URL'}")
        print(f"  {'─'*70}")
        for code, entry in sorted(self.urls.items(), key=lambda x: -x[1]['hits']):
            url_preview = entry['long_url'][:38] + ('...' if len(entry['long_url']) > 38 else '')
            print(f"  {BASE_URL+code:<30} {entry['hits']:>6}  {url_preview}")
        print(f"  {'─'*70}")

    def bulk_shorten(self, urls):
        results = {}
        for url in urls:
            short = self.shorten(url)
            if short:
                results[url] = short
        return results


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   URL Shortener Simulator v1.0           ║")
    print("╚══════════════════════════════════════════╝")

    shortener = URLShortener()

    # Demo URLs
    test_urls = [
        "https://www.example.com/very/long/path/to/some/article?id=12345&utm=campaign",
        "https://docs.python.org/3/library/collections.html",
        "https://github.com/python/cpython/blob/main/README.rst",
        "https://stackoverflow.com/questions/tagged/python",
        "https://pypi.org/project/requests/",
    ]

    print("\n  Shortening URLs:")
    shorts = []
    for url in test_urls:
        s = shortener.shorten(url)
        if s:
            shorts.append(s)
        print()

    # Custom code
    shortener.shorten("https://anthropic.com", custom_code="claude")

    print("\n  Resolving short URLs:")
    for s in shorts[:3]:
        shortener.resolve(s)
        shortener.resolve(s)  # Hit twice to track
        print()

    # Simulate access
    for s in shorts:
        for _ in range(random.randint(1, 20)):
            shortener.resolve(s)

    shortener.list_all()
    shortener.top_links(5)

    if shorts:
        shortener.stats(shorts[0])

    # Interactive
    while True:
        print("\n  [1] Shorten  [2] Resolve  [3] Stats  [4] List all  [5] Quit")
        choice = input("  Choice: ").strip()
        if choice == '5':
            break
        elif choice == '1':
            url = input("  Long URL: ").strip()
            custom = input("  Custom code (or Enter to auto): ").strip() or None
            shortener.shorten(url, custom)
        elif choice == '2':
            short = input("  Short URL or code: ").strip()
            if not short.startswith('http'):
                short = BASE_URL + short
            shortener.resolve(short)
        elif choice == '3':
            short = input("  Short URL or code: ").strip()
            if not short.startswith('http'):
                short = BASE_URL + short
            shortener.stats(short)
        elif choice == '4':
            shortener.list_all()

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


if __name__ == "__main__":
    main()
