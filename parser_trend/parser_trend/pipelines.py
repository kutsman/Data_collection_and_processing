# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ParserTrendPipeline:

      def __init__(self):

        mongo_db = MongoClient()
        self.db = mongo_db['news_db']


      def process_item(self, item, spider):

        collection = self.db[spider.name]     
       
        if collection.find_one({'link': item['link']}):
            collection.update_one(
                {'link': item['link']},
                {'$set': {
                    'name': item['name'],
                    'date': item['date'],
                    'time': item['time']
                }
                }
              )
        else:
            collection.insert_one(item)

        return item
