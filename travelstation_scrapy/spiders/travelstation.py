import scrapy
from bs4 import BeautifulSoup
import re
from travelstation_scrapy.items import TravelstationScrapyItem

class TravelstationSpider(scrapy.Spider):
    name = 'travelstation'
    allowed_domains = ['travelstation.tokyo']
    start_urls = [
        'http://travelstation.tokyo/station/hokkaido/',
        'http://travelstation.tokyo/station/tohoku/',
        'http://travelstation.tokyo/station/kanto/',
        'http://travelstation.tokyo/station/koshinetsu/',
        'http://travelstation.tokyo/station/tokai/',
        'http://travelstation.tokyo/station/hokuriku/',
        'http://travelstation.tokyo/station/kinki/',
        'http://travelstation.tokyo/station/chugoku/',
        'http://travelstation.tokyo/station/shikoku/',
        'http://travelstation.tokyo/station/kyushu/',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.select('msearch li.company_page > a'):
            if re.compile(r'JR').match(link.get_text()):
                continue
            yield scrapy.Request(response.urljoin(link.get('href')), self.parse_detail)

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for station in soup.select('a'):
            href = station.get('href')
            if href is None:
                continue
            match = re.compile(r'([a-z]+)\/([a-z]+)\.htm').match(href)
            if match is None:
                continue
            print(match.groups())
            item = TravelstationScrapyItem()
            item['name'] = station.get_text().replace('★', '').replace('◇', '')
            item['roma'] = match.group(2)
            item['company'] = soup.find('h1').get_text()
            yield item
