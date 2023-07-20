# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from db import Session
from db.models import WordCount


class WikiPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        word_count = WordCount(
            word=adapter["word"],
            url_index=adapter["url_index"],
            url=adapter["url"],
            count=adapter["count"]
        )
        self.session.add(word_count)

    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
