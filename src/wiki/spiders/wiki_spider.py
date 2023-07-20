import scrapy

from bs4 import BeautifulSoup
from wiki.items import WikiItem
from collections import Counter

class WikiSpider(scrapy.Spider):
    name = "wiki"

    def start_requests(self):
        urls = [
            "https://en.wikipedia.org/wiki/Special:Random",
            "https://en.wikipedia.org/wiki/Special:Random",
        ]
        for index, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={"url_index": index})

    def parse(self, response, url_index):
        soup = BeautifulSoup(response.text, "lxml")
        main_content = soup.select_one("#content")
        # Sanitize
        body = main_content.text.replace("\n", " ").replace("\t", " ").lower().split(" ")
        result = dict(Counter(body))
        for word, count in result.items():
            # filter empty word
            if len(word.strip()):
                yield WikiItem(
                    word=word,
                    url_index=url_index,
                    url=response.url,
                    count=count
                )

