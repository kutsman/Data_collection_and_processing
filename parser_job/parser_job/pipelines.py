# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ParserJobPipeline:

    def __init__(self):        

      mongo_db = MongoClient()                                        # подключаем mongo клиента
      self.db = mongo_db['vacancy_db']                                # создает db
      
    def process_item(self, item, spider):

      collection = self.db[spider.name]                               # создаем коллекцию db[с названием имени паука], hh_ru or sj_ru
 
      if collection.find_one({'vacancy_link': item['vacancy_link']}): # условие отсутствия дублирования в коллекции, если ссылка в коллекции уже есть
                                                                      # обновляются все данные, но остается прежний id, если ссылки нет записывается новая вакансия
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
          collection.insert_one(item) # если вакансии в коллекции нет, то просто вставляем ее



      #collection.insert_one(item) # использовал для проверки 
      return item
      
      #print(f'\n**********************\n{item}\n{spider}\n**********************\n') # использовал для проверки
      #return item
