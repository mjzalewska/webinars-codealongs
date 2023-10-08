import requests
from bs4 import BeautifulSoup

# check our robots.txt before scraping
url = "https://en.wikipedia.org/wiki/Yellow-throated_miner"


class WikiScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        # a set containing urls already viisted to exclude them from further visiits
        self.visited_url = set()
        # a queue of urls to visit
        self.url_queue = [start_url]
        self.steps = 0
        self.pages_visited = 0

    def __str__(self):
        return f"Scraper: {url}"

    def get_links_from_url(self, url):
        links = []  # for storing links found on a webpage
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features="html.parser")
            for a in soup.select("p a[href^='/wiki/']"):
                link = "https://en.wikipedia.org" + a["href"]
                if link not in self.visited_url:
                    links.append(link)
        except Exception as e:
            print(f"Error retrieving links from {url}: {e}")
        return links

    def has_hitler_been_mentioned(self, url):
        try:
            response = requests.get(url)
            return "Hitler" in response.text
        except Exception as error:
            print(f"Error while checking mention in {url}: {error}")
            return False

    def search_for_hitler(self):
        while self.url_queue:
            current_url = self.url_queue.pop()
            self.visited_url.add(current_url)
            self.pages_visited += 1
            print(f"Checking {current_url} (Steps: {self.steps}, Visited: {self.pages_visited} pages)")

            if self.has_hitler_been_mentioned(current_url):
                print(f"We have found a mention about Hitler after: {self.steps} steps")
                return

            for link in self.get_links_from_url(current_url):
                if link not in self.visited_url:
                    self.url_queue.append(link)

            self.steps += 1


if __name__ == "__main__":
    scraper = WikiScraper(url)
    scraper.search_for_hitler()

    # print(scraper)
