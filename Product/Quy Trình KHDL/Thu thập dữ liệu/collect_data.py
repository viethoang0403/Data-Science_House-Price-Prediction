import datetime
import scrapy
import json

class collect_data(scrapy.Spider):
    name='Get_Data'

    def __init__(self):
        self.page_count = 1
        self.num_page = 800 #Num of page need to get data

    allowed_domains = ["thuephongtro.com"]
    start_urls = ['https://thuephongtro.com/cho-thue-phong-tro-ho-chi-minh?page=1']

    def parse(self, response):
        for i in range(1,21):
            #title
            path = '/html/body/div/main/div/div[3]/div/div[2]/article['+str(i)+']/a/div'
            pathSub = '/html/body/div/main/div/div[3]/div/div[2]/article['+str(i)+']'
            
            name = response.xpath(path).css('h3.title::text').getall()[1].strip()
            DistrictAndCity = response.xpath(path).css('div.post-address span::text').get().strip().split(', ')
            Date = response.xpath(path).css('div:last-of-type > div:first-of-type > span::text').get().strip()
            price = response.xpath(path).css('div:first-of-type > div > span.price::text').get().strip()
            square = response.xpath(path).css('div:first-of-type > div > span.feature-item::text').getall()[1].strip()
            Id = response.xpath(pathSub).css('a::attr(href)').get().strip().split('.')[0].split('-')[-1].strip()
            
            if Date == "Hôm nay":
                Date = datetime.datetime.now().strftime("%d/%m/%Y")
            
                   
            yield {
                'Id': Id,
                'Title': name,
                'Price': price,
                'Square': square,
                'District': DistrictAndCity[0],
                'City': DistrictAndCity[1],
                'Date': Date
            }
            if self.page_count < self.num_page:
                self.page_count += 1
                next_page_url = f'https://thuephongtro.com/cho-thue-phong-tro-ho-chi-minh?page={self.page_count}'
                yield scrapy.Request(next_page_url, callback=self.parse)