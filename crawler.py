import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

START_URL = "http://testphp.vulnweb.com/"
visited_urls = set()
internal_urls = set()

def is_internal(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == "" or parsed.netloc == base_domain

def crawl(url, base_domain):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full_url = urljoin(url, href)
            cleaned_url = urlparse(full_url)._replace(fragment="").geturl()

            if is_internal(cleaned_url, base_domain) and cleaned_url not in visited_urls:
                visited_urls.add(cleaned_url)
                internal_urls.add(cleaned_url)
                print(f"[+] Found: {cleaned_url}")
                crawl(cleaned_url, base_domain)

    except Exception as e:
        print(f"[-] Failed to crawl {url}: {e}")

if __name__ == "__main__":
    domain = urlparse(START_URL).netloc
    crawl(START_URL, domain)

    # Save results
    with open("internal_links.json", "w") as f:
        json.dump(sorted(internal_urls), f, indent=4)

    with open("internal_links.txt", "w") as f:
        for link in sorted(internal_urls):
            f.write(link + "\n")

    print("\n[✓] Done! Links saved to JSON and TXT.")
