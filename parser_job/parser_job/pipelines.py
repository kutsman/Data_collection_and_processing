# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ParserJobPipeline:

    def __init__(self):        

      mongo_db = MongoClient()
      self.db = mongo_db['vacancy_db']
      
    def process_item(self, item, spider):

      collection = self.db[spider.name]

      if collection.find_one({'vacancy_link': item['vacancy_link']}):
        collection.update_one(
            {'vacancy_link': item['vacancy_link']}, 
            {'$set': {
                'name': item['name'],                          
                'salary_min': item['salary_min'], 
                'salary_max': item['salary_max']                        
                }
              }
              )
      else:
          collection.insert_one(item)



      #collection.insert_one(item)
      return item
      
      #print(f'\n**********************\n{item}\n{spider}\n**********************\n')
      #return item
