# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from urllib.parse import urlparse


from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os

from parser_goods.items import ParserGoodsItem


class ParserGoodsPipeline:
    def process_item(self, item, spider):
        return item


class OBIPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if item['photo']:
            for img in item['photo']:
                try:
                    yield Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, item=ParserGoodsItem): # Задаем item и импортируем выше
        # item['link'].split('/')[...] # разбиваем ссылку на продукт по /, чтобы вычленить название
        len_link = len(item['link'].split('/')) # идем длину получившегося списка
        folder_name = item['link'].split('/')[len_link-1] # берем последнюю часть списка (т.е. название продукта
                                                          # и далее создаем папку с этим названием
        return f'{folder_name}/' + os.path.basename(urlparse(request.url).path) # все файлы с этого продукта пойдут
        # в эту папку + картинку очищаем от лишнего и делаем понятное название.
