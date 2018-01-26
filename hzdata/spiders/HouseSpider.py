import scrapy
import logging
from scrapy_splash import SplashRequest
from hzdata.items import House
from hzdata import settings
from urllib.parse import urlparse, parse_qs


class HouseSpider(scrapy.Spider):
    name = "house"
    SPIDER_HOST = settings.TARGET_URL
    start_urls = [SPIDER_HOST+"nowonsale.jsp", SPIDER_HOST+"presale.jsp"]

    def parse(self, response):
        for href in response.xpath("//div[@class='answer']//tr/td[3]/a/@href").extract():
            yield response.follow(href, self.parse_property)

        # follow pagination links
        # for href in response.xpath("//div[@class='paging']/a/@href").extract():
        #     yield response.follow(href, self.parse)

    def parse_property(self, response):
        open_date = response.xpath("//div[@class='Salestable']//tr[6]/td[1]/text()").extract_first().strip()
        open_date = str(open_date).replace('\n', '').strip() if open_date is not None else None
        project_code = parse_qs(urlparse(str(response.url)).query)['ProjectCode'][0]
        for building in response.xpath("//div[@class='Salestable']//tr[8]//tr/td[6]/a/@href").extract():
            building = self.SPIDER_HOST + building
            request = SplashRequest(building, self.parse_building, args={'wait': 0.5})
            request.meta['open_date'] = open_date
            request.meta['project_code'] = project_code
            yield request

    def parse_building(self, response):
        project_code = response.meta['project_code']
        building_code = parse_qs(urlparse(str(response.url)).query)['buildingcode'][0]
        open_date = response.meta['open_date']
        for house in response.xpath("//table[2]//td"):
            house_id = house.xpath("div[2]/@onclick").extract_first()
            if house_id is not None:
                house_id = str(house_id).split("(")[1].split(")")[0].split(",")
                house_url = "House.jsp?id="+house_id[0]+"&lcStr="+house_id[1]
                request = response.follow(house_url, self.parse_house)
                request.meta['open_date'] = open_date
                request.meta['project_code'] = project_code
                request.meta['building_code'] = building_code
                request.meta['house_code'] = house_id[0]
                yield request

    def parse_house(self, response):
        item = House()
        project_code = response.meta['project_code']
        building_code = response.meta['building_code']
        house_code = response.meta['house_code']
        property_name = response.xpath("//table[1]//tr[2]/td[1]/text()").extract_first().strip()
        building_name = response.xpath("//table[1]//tr[2]/td[2]/text()").extract_first().strip()
        house_name = response.xpath("//table[1]//tr[3]/td[1]/text()").extract_first().strip()
        plan_purpose = response.xpath("//table[1]//tr[3]/td[2]/text()").extract_first().strip()
        house_purpose = response.xpath("//table[1]//tr[4]/td[1]/text()").extract_first().strip()
        floor = response.xpath("//table[1]//tr[5]/td[1]/text()").extract_first().strip()
        floor_height = response.xpath("//table[1]//tr[5]/td[2]/text()").extract_first().strip()
        house_orientation = response.xpath("//table[1]//tr[6]/td[1]/text()").extract_first().strip()
        house_construction = response.xpath("//table[1]//tr[6]/td[2]/text()").extract_first().strip()
        is_public = response.xpath("//table[1]//tr[7]/td[1]/text()").extract_first().strip()
        is_back_moving = response.xpath("//table[1]//tr[7]/td[2]/text()").extract_first().strip()
        is_oneself = response.xpath("//table[1]//tr[8]/td[1]/text()").extract_first().strip()
        is_pre_sell = response.xpath("//table[1]//tr[8]/td[2]/text()").extract_first().strip()
        price = response.xpath("//table[1]//tr[9]/td[1]/text()").extract_first().strip()
        pre_total_square = response.xpath("//table[1]//tr[11]/td[1]/text()").extract_first().strip()
        actual_total_square = response.xpath("//table[1]//tr[11]/td[2]/text()").extract_first().strip()
        pre_inner_square = response.xpath("//table[1]//tr[12]/td[1]/text()").extract_first().strip()
        actual_inner_square = response.xpath("//table[1]//tr[12]/td[2]/text()").extract_first().strip()
        pre_public_square = response.xpath("//table[1]//tr[13]/td[1]/text()").extract_first().strip()
        actual_public_square = response.xpath("//table[1]//tr[13]/td[2]/text()").extract_first().strip()
        is_pledge = response.xpath("//table[1]//tr[15]/td[1]/text()").extract_first().strip()
        is_seal = response.xpath("//table[1]//tr[15]/td[2]/text()").extract_first().strip()

        item['project_code'] = project_code
        item['building_code'] = building_code
        item['house_code'] = house_code
        item['property_name'] = property_name
        item['building_name'] = building_name
        item['house_name'] = house_name
        item['plan_purpose'] = plan_purpose
        item['house_purpose'] = house_purpose
        item['floor'] = floor
        item['floor_height'] = floor_height
        item['house_orientation'] = house_orientation
        item['house_construction'] = house_construction
        item['is_public'] = is_public
        item['is_back_moving'] = is_back_moving
        item['is_oneself'] = is_oneself
        item['is_pre_sell'] = is_pre_sell
        item['price'] = price
        item['pre_total_square'] = pre_total_square
        item['actual_total_square'] = actual_total_square
        item['pre_inner_square'] = pre_inner_square
        item['actual_inner_square'] = actual_inner_square
        item['pre_public_square'] = pre_public_square
        item['actual_public_square'] = actual_public_square
        item['is_pledge'] = is_pledge
        item['is_seal'] = is_seal
        item['property_name'] = property_name
        return item
