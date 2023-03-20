# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst

def photo(value):
    try:
        photos = []
        for i in value:  # беру весь список ссылок на картинки и далее для каждого элемента из списка очищаю длинную ссылку
            image = i.split("?")[0]  # разбиваю по знаку ? и беру получивший 1-й элемент списка,
            photos.append(image)  # таким образом остается красивый путь к картинке и создаю из этих ссылок новый список
        value = photos  # который и передаю в Item
    except:
        return value
    return value


def clean_price(value):
    try:
        value = int(value[0].replace('\xa0', '').replace('₽', '')) # очищаю стоимость и преобразую в число
    except:
        return value
    return value

class ParserGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    company = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    photo = scrapy.Field(input_processor=Compose(photo), output_processor=Compose())
    pass
