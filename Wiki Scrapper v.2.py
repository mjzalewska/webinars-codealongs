########################################################################################################
##  Simple web crawler and scraper which searches for word 'Hitler' on a given page on Wikipedia and  ##
##  its subpages, returning number of nested pages visited and final URL where the word was found.    ##
########################################################################################################


import requests
from bs4 import BeautifulSoup
import sys


# Default URL to be scraped (as example)
URL = 'https://en.wikipedia.org/wiki/Yellow-throated_miner'

# If URL is passed as argument, use it instead
if len(sys.argv) > 1:
    URL = sys.argv[1]


class WikiScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited_urls = set()
        self.url_queue = [start_url]
        self.nesting_level = 1
        self.pages_visited = 1

    def get_links_from_url(self, url):
        """Returns all links from a given url"""
        links = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.select('p a[href^="/wiki/"]'):
                link = 'https://en.wikipedia.org' + a['href']

                if link not in self.visited_urls:
                    links.append(link)

        except Exception as e:
            print(f"Error getting links from {url}: {e}")

        return links

    def has_hitler_been_mentioned(self, url):
        """Returns 'True' if word 'Hitler' is mentioned in the given url, otherwise 'False'"""
        try:
            response = requests.get(url)
            return "hitler" in response.text.lower() or False

        except Exception as e:
            print(f"Error while checking Hitler mention in {url}: {e}")

        return False

    def search_for_hitler(self):
        while self.url_queue:
            current_url = self.url_queue.pop(0)
            self.visited_urls.add(current_url)

            print(f"Checking: {current_url} (Nesting level: {self.nesting_level}, "
                  f"Pages visited: {self.pages_visited})")

            if self.has_hitler_been_mentioned(current_url):
                print(f"We have found a mention about Hitler on nesting level {self.nesting_level} " + \
                      f"after visiting {self.pages_visited} URLs! Final URL was: {current_url}")
                return

            links = self.get_links_from_url(current_url)
            self.nesting_level += 1

            for link in links:
                if link not in self.visited_urls:
                    self.url_queue.append(link)
                    self.visited_urls.add(link)
                    self.pages_visited += 1

                    if self.has_hitler_been_mentioned(link):
                        print(f"We have found a mention about Hitler on nesting level {self.nesting_level} " + \
                              f"after visiting {self.pages_visited} URLs! Final URL was: {current_url}")
                        return

    def __str__(self):
        return f"WikiScraper(start_url='{self.start_url}')"


if __name__ == "__main__":
    scraper = WikiScraper(URL)
    scraper.search_for_hitler()