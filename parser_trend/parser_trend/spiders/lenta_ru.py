import scrapy
from scrapy.http import HtmlResponse
from parser_trend.items import ParserTrendItem


class LentaRuSpider(scrapy.Spider):
    name = "lenta_ru"
    allowed_domains = ["lenta.ru"]
    start_urls = ["https://lenta.ru/parts/news/"]

    def parse(self, response:HtmlResponse):       
            
        news_links = response.xpath("//li[@class='parts-page__item']/a/@href").getall()

        for news_link in news_links:
            yield response.follow(news_link, callback=self.news_parse)      
        print(f'\n######################\nParsing the current page: {response.url}\n######################\n')

        next_page = response.xpath("//a[@class='loadmore js-loadmore']/@href").get()       
        if next_page != "/parts/news/4/": # ограничиваем глубину страниц для поиска
        # если следующая страница 4, то паук напишет что текущая страница будет последней для парсинга
        # и последняя страница, которую пропарсит паукт будет 3-ей (так как не предыдущей странице, паук
        # понимает какая будет следующая)
          yield response.follow(next_page, callback=self.parse)         
        else:
          print('\n**********************\nThis page is last for parsing\n**********************\n')
        
        #print(f'\n######################\n{next_page}\n######################\n')

    def news_parse(self, response:HtmlResponse):
        news_name=response.xpath("//div[@class='topic-body _news']/h1/span/text()").getall()[0]  
        news_link = response.url
        date_time=response.xpath("//a[contains(@class, 'topic-header__time')]/text()").get().split(",")
        news_time=date_time[0]
        news_date=date_time[1]  
        #pass

        yield ParserTrendItem(
            name=news_name,            
            time=news_time,
            date=news_date,
            link=news_link
                                   
        )