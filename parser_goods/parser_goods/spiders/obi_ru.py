import scrapy
from scrapy.http import HtmlResponse
from parser_goods.items import ParserGoodsItem
from scrapy.loader import ItemLoader


class ObiRuSpider(scrapy.Spider):
    name = "obi_ru"
    allowed_domains = ["obi.ru"]
    start_urls = ["https://obi.ru/sad-i-dosug/sadovaja-tehnika/gazonokosilki"]

    def parse(self, response: HtmlResponse):
        good_links = response.xpath("//ul[contains(@showitemsqty,'4')]/li/a/@href").getall()

        for good_link in good_links:  # использовал good_links[0:2] тестил на 1-2 товаре
            yield response.follow(good_link, callback=self.good_parse)
        print(f'\n###############\n{response.url}\n###############')
        # pass

        # тут можно вставить поиск следующей страницу и ее парсинг
        next_page = response.xpath("")
    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ParserGoodsItem(), response=response)

        loader.add_xpath('name', "//article/h1/text()")
        loader.add_xpath('company', "//h4[contains(@itemprop,'brand')]/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price',
                         "//article/div/div/div/div[contains(@aria-label,'Product price:')]/div/div/div/div/span/text()")
        loader.add_xpath('photo', "//div[contains(@aria-label, 'Draggable area')]/div/picture/source[1]/@srcset[1]")
        yield loader.load_item()

        '''
        # сначала проверял через вариант с yield Items без ItemLoader
        good_name = response.xpath("//article/h1/text()").getall()[0]
        good_company = response.xpath("//h4[contains(@itemprop,'brand')]/text()").get()
        good_link = response.url
        good_price = response.xpath(
            "//article/div/div/div/div[contains(@aria-label,'Product price:')]/div/div/div/div/span/text()").getall()[
            0].replace('\xa0', '').replace('₽', '')
        good_photo = response.xpath("//div[contains(@aria-label, 'Draggable area')]/div/picture/source[1]/@srcset[1]").getall()
        #print(f'***************\n{good_photo[0]}\n*****************')
        #print(f'***************\n{good_photo[0].split("?")}\n*****************')
        print(f'***************\n{good_photo[0].split("?")[0]}\n*****************')
        photos = []
        for i in good_photo:
            image = i.split("?")[0]
            photos.append(image)
        yield ParserGoodsItem(
            name=good_name,
            company=good_company,
            price=good_price,
            link=good_link,
            photo=photos

        )
        '''
