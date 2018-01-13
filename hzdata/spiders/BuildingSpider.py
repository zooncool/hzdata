import scrapy
import logging
from scrapy_splash import SplashRequest
from urllib.parse import urlparse, parse_qs
import hashlib
import json

class BuildingSpider(scrapy.Spider):
    name = "building"
    SPIDER_HOST = "http://x.x.x.x/web/"
    start_urls = [SPIDER_HOST + "nowonsale.jsp", SPIDER_HOST + "presale.jsp"]

    def parse(self, response):
        # follow links to project
        #  pages
        for href in response.xpath("//div[@class='answer']//tr/td[3]/a/@href").extract():
            yield response.follow(href, self.parse_property)

        # follow pagination links
        # for href in response.xpath("//div[@class='paging']/a/@href").extract():
        #     # self.logger.info("page url is %s", href)
        #     yield response.follow(href, self.parse)

    def parse_property(self, response):
        property_name = response.xpath("//div[@class='Salestable']//tr[1]/td[1]/text()").extract_first()
        open_time = response.xpath("//div[@class='Salestable']//tr[6]/td[1]/text()").extract_first()
        project_code = parse_qs(urlparse(str(response.url)).query)['ProjectCode'][0]
        for building in response.xpath("//div[@class='Salestable']//tr[8]//tr/td[6]/a/@href").extract():
            building = self.SPIDER_HOST + building
            request = SplashRequest(building, self.parse_building, args={'wait': 0.5})
            request.meta['property_name'] = property_name
            request.meta['open_time'] = open_time
            request.meta['project_code'] = project_code
            yield request

    def parse_building(self, response):
        property_name = response.meta['property_name']
        open_time = response.meta['open_time']
        project_code = response.meta['project_code']
        building_name = response.xpath("//table[@class='tablelw']//tr[1]/td[3]/text()").extract_first()
        building_code = parse_qs(urlparse(str(response.url)).query)['buildingcode'][0]
        house_id_dict = {}
        for house in response.xpath("//table[2]//td"):
            house_name = house.xpath("div[1]/text()").extract_first()
            sale_state_image = house.xpath("div[2]/img/@src").extract_first()
            if sale_state_image is not None:
                sale_state = str(sale_state_image).split('/')[4].split(".")[0]
            house_id = house.xpath("div[2]/@onclick").extract_first()
            if house_id is not None:
                house_id = str(house_id).split("(")[1].split(")")[0].split(",")[0]
                house_id_dict[house_id] = sale_state
        print( sorted(house_id_dict.items(), key=lambda item: item[0]))
        # for house_temp in house_id_dict:
        #     logging.info(house_temp)
        # logging.info(house_id_dict)
        # md5 = hashlib.md5(house_id_dict)
        # logging.info("property_name=%s,building name=%s,open_time=%s,project_code=%s,building_code=%s,md5=%s",
        #              property_name, building_name, open_time, project_code, building_code, md5)
