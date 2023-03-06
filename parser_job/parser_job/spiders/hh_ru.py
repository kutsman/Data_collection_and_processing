import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem
import re

class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = ['https://hh.ru/search/vacancy?area=1586&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=Java&ored_clusters=true&page=0']
    #start_urls = ['https://hh.ru/search/vacancy?text=Java&salary=&area=1&ored_clusters=true&enable_snippets=true'
                  #'&page=0']    

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()  # здесь ищем кнопку далее
        if next_page is None:                                                 # если мы попали на страницу и у нее нет кнопки далее, т.е. она последняя пишем ""
          print(f'\n++++++++++++++++++++\nParsing last page...\n++++++++++++++++++++')
        else:
          yield response.follow(next_page, callback=self.parse)               # иначе идем на следующую

        vacancy_links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall() # находим список ссылок на вакансии
        for vacancy_link in vacancy_links:
            yield response.follow(vacancy_link, callback=self.vacancy_parse) # тут проваливаемся в ссылку и парсим функцией vacancy_parse

        print(f'\n######################\n{response.url}\n######################\n')

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.css("div.vacancy-title h1::text").get() # название вакансии
        vacancy_link = response.url                                     # ссылка на вакансию
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall() # необработанный список ЗП с текстом и цифрами
        #print(f'\n**********************\n{vacancy_name}\n{vacancy_link}\n{vacancy_salary}\n**********************\n')

        vacancy_len = len(vacancy_salary) # использовал для проверки

        if vacancy_salary[0] == 'з/п не указана':                       # отсеиваем вакансии без ЗП, они указаны на HH.RU как "з/п не указана"
            salary_min = None
            salary_max = None
        else:
            
            vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall()
            
            # при длине списка ЗП ниже 5 мы оставляем указание ЗП по типу: "от ...." и "до ...."
            if len(vacancy_salary) < 5:

              if vacancy_salary[0] == 'до':
                  salary_min = None
                  salary_max = int(vacancy_salary[1].replace(u'\xa0', u''))
              else:                                                       # подразумеваем здесь условие vacancy_salary[0] == 'от', удаляем "\xa0"
                  salary_min = int(vacancy_salary[1].replace(u'\xa0', u'')) 
                  salary_max = None 
                          
            else: 
                salary_min = int(vacancy_salary[1].replace(u'\xa0', u''))  # при длине списка больше 5, сюда попадут ЗП формата: от 100000 до 500000 и тому подобному
                salary_max = int(vacancy_salary[3].replace(u'\xa0', u''))               


        yield ParserJobItem(
            name=vacancy_name,
            #salary=vacancy_salary, # использовал для проверки
            salary_min=salary_min,
            salary_max=salary_max,
            vacancy_link=vacancy_link
            #vacancy_len=vacancy_len # использовал для проверки

            )
            
