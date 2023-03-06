import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem
import re


class SjRuSpider(scrapy.Spider):
    name = "sj_ru"
    allowed_domains = ["superjob.ru"]
    #start_urls = ["http://superjob.ru/"]

    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']  # ищем по ключевому слову Python, в HH искал по Java
    #start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']
       

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get() # здесь ищем кнопку далее
        if next_page is None:                                                        # если мы попали на страницу и у нее нет кнопки далее, т.е. она последняя пишем ""
          print(f'\n++++++++++++++++++++\nParsing last page...\n++++++++++++++++++++')
        else:                                                             
          yield response.follow(next_page, callback=self.parse)                      # иначе идем на следующую

        vacancy_links= response.css(
            'div.f-test-vacancy-item \
            a[class*=f-test-link][href^="/vakansii"]::attr(href)'
            ).getall()                                                               # находим список ссылок на вакансии благодаря возможности через CSS
                                                                                     # нам нужно условие наличия в классе <a> 'f-test-link', и чтобы ссылка начиналась
                                                                                     # с /vakansii так мы отметем рекламу и обучение, кстати ссылки все не целые...
        
        
        #'http://superjob.ru/'[:-1] + проверял изначально правильность ссылок, так как они не полные
        
        for vacancy_link in vacancy_links:
            yield response.follow(vacancy_link, callback=self.vacancy_parse)

        print(f'\n######################\n{response.url}\n######################\n')

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//div[contains(@class, 'f-test-vacancy-base-info')]/div/div/div/h1/text()").get()
        vacancy_link = response.url
        vacancy_salary = response.xpath("//div[contains(@class, 'f-test-vacancy-base-info')]/div/div/div/span/span/text()").getall()
        #print(f'\n**********************\n{vacancy_name}\n{vacancy_link}\n{vacancy_salary}\n**********************\n')

        vacancy_len = len(vacancy_salary) # использовал для проверки

        if vacancy_salary[0] == 'По договорённости':  # отсеиваем вакансии без ЗП, они указаны на SJ.RU как "По договорённости"
            salary_min = None
            salary_max = None
        else:           
            if len(vacancy_salary) < 5:  # при длине списка ЗП ниже 5 мы оставляем указание ЗП по типу: "от ...." и "до ...."
              if vacancy_salary == 'до':
                  salary_min = None
                  salary_max = int(vacancy_salary[2].replace(u'\xa0', u'').replace(u'₽', u'')) # также удаляем \xa0 и знак ₽ так как он прилипает к цислу
              else:
                  salary_min = int(vacancy_salary[2].replace(u'\xa0', u'').replace(u'₽', u'')) # также удаляем \xa0 и знак ₽ так как он прилипает к цислу
                  salary_max = None                 
            else:
                salary_min = int(vacancy_salary[0].replace(u'\xa0', u'')) # при длине списка больше 5, сюда попадут ЗП формата: от 100000 до 500000 и тому подобному
                salary_max = int(vacancy_salary[4].replace(u'\xa0', u''))               


        yield ParserJobItem(
            name=vacancy_name,
            #salary=vacancy_salary, # использовал для проверки
            salary_min=salary_min,
            salary_max=salary_max,
            vacancy_link=vacancy_link
            #vacancy_links=vacancy_links, # использовал для проверки
            #vacancy_len=vacancy_len # использовал для проверки
            )
            
