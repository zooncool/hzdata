import scrapy
import logging
from scrapy_splash import SplashRequest
from urllib.parse import urlparse, parse_qs
from hzdata import settings
from hzdata.items import Building
import hashlib


class BuildingSpider(scrapy.Spider):

    name = "building"
    SPIDER_HOST = settings.TARGET_URL
    start_urls = [SPIDER_HOST + "nowonsale.jsp", SPIDER_HOST + "presale.jsp"]
    # 可售ks,不可售bks,已收签约ysqy,现房已签约xfqy,已办证ybz
    SALE_STATE_CONSTENT = {"ks": 0, "ysqy": 1, "xfqy": 2, "ybz": 3, "bks": 4}

    def parse(self, response):
        for href in response.xpath("//div[@class='answer']//tr/td[3]/a/@href").extract():
            yield response.follow(href, self.parse_property)

        for href in response.xpath("//div[@class='paging']/a/@href").extract():
            yield response.follow(href, self.parse)

    def parse_property(self, response):
        property_name = response.xpath("//div[@class='Salestable']//tr[1]/td[1]/text()").extract_first()
        open_date = response.xpath("//div[@class='Salestable']//tr[6]/td[1]/text()").extract_first()
        project_code = parse_qs(urlparse(str(response.url)).query)['ProjectCode'][0]
        for building in response.xpath("//div[@class='Salestable']//tr[8]//tr/td[6]/a/@href").extract():
            building = self.SPIDER_HOST + building
            request = SplashRequest(building, self.parse_building, args={'wait': 0.5})
            request.meta['property_name'] = property_name
            request.meta['open_date'] = open_date
            request.meta['project_code'] = project_code
            yield request

    def parse_building(self, response):
        property_name = response.meta['property_name']
        project_code = response.meta['project_code']
        building_name = response.xpath("//table[@class='tablelw']//tr[1]/td[3]/text()").extract_first()
        building_name = str(building_name).replace("楼幢名称：", "")
        building_code = parse_qs(urlparse(str(response.url)).query)['buildingcode'][0]
        open_date = response.meta['open_date']
        house_id_dict = {}
        for house in response.xpath("//table[2]//td"):
            sale_state_image = house.xpath("div[2]/img/@src").extract_first()
            if sale_state_image is not None:
                sale_state = str(sale_state_image).split('/')[4].split(".")[0]
            house_id = house.xpath("div[2]/@onclick").extract_first()
            if house_id is not None:
                house_id = str(house_id).split("(")[1].split(")")[0].split(",")[0]
                house_id_dict[house_id] = sale_state
        house_id_dict = sorted(house_id_dict.items(), key=lambda it: it[0])
        houses_temp = ""
        for k, v in house_id_dict:
            houses_temp += k + "|" + v + ","
        houses = houses_temp
        logging.info(houses_temp)
        m = hashlib.md5()
        m.update(houses.encode("utf-8"))
        digest = m.hexdigest()
        item = Building()
        item['project_code'] = project_code
        item['property_name'] = property_name
        item['building_code'] = building_code
        item['building_name'] = building_name
        item['open_date'] = open_date
        item['houses'] = houses
        item['digest'] = digest
        return item
