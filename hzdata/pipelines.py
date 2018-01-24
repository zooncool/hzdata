# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
from datetime import *

from hzdata import settings
from hzdata.items import House
from hzdata.items import Building


class HousePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == House:
            try:
                property_name = str(item['property_name'])
                building_name = str(item['building_name'])
                house_name = str(item['house_name'])
                plan_purpose = str(item['plan_purpose'])
                house_purpose = str(item['house_purpose'])
                floor = str(item['floor'])
                floor_height = float(str(item['floor_height'])) if item['floor_height'] is not None else 0
                house_orientation = item['house_orientation']
                house_construction = item['house_construction']
                is_public = 1 if item['is_public'] == "是" else 0
                is_back_moving = 1 if item['is_back_moving'] == "是" else 0
                is_oneself = 1 if item['is_oneself'] == "是" else 0
                is_pre_sell = 1 if item['is_pre_sell'] == "是" else 0
                price = float(str(item['price']).split("\r\n")[0]) if any(char.isdigit() for char in item['price']) else 0
                pre_total_square = float(str(item['pre_total_square'])) if item['pre_total_square'] is not None else 0
                actual_total_square = float(str(item['actual_total_square'])) if item['actual_total_square'] is not None else 0
                pre_inner_square = float(str(item['pre_inner_square'])) if item['pre_inner_square'] is not None else 0
                actual_inner_square = float(str(item['actual_inner_square'])) if item['actual_inner_square'] is not None else 0
                pre_public_square = float(str(item['pre_public_square'])) if item['pre_public_square'] is not None else 0
                actual_public_square = float(str(item['actual_public_square'])) if item['actual_public_square'] is not None else 0
                is_pledge = 1 if item['is_pledge'] == "是" else 0
                is_seal = 1 if item['is_seal'] == "是" else 0
                gmt_created = datetime.now().date()
                self.cursor.execute(
                    """insert into house(gmt_created, property_name, building_name, house_name, plan_purpose, house_purpose, floor, 
                    floor_height, house_orientation, house_construction, is_public, is_back_moving, is_oneself, 
                    is_pre_sell, price, pre_total_square, actual_total_square, pre_inner_square, actual_inner_square, 
                    pre_public_square, actual_public_square, is_pledge, is_seal) 
                    value (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (gmt_created, property_name, building_name, house_name, plan_purpose, house_purpose, floor,
                     floor_height, house_orientation, house_construction, is_public, is_back_moving, is_oneself,
                     is_pre_sell, price, pre_total_square, actual_total_square, pre_inner_square, actual_inner_square,
                     pre_public_square, actual_public_square, is_pledge, is_seal))
                self.connect.commit()
            except Exception as error:
                logging.error(error)
            return item
        elif item.__class__ == Building:
            try:
                project_code = item['project_code']
                building_code = item['building_code']
                property_name = item['property_name']
                building_name = item['building_name']
                open_date = item['open_date']
                houses = item['houses']
                digest = item['digest']
                gmt_created = datetime.now()
                self.cursor.execute(
                    """insert into building(gmt_created, project_code, building_code, property_name, building_name, 
                    open_date, houses, digest) 
                    value (%s, %s,%s,%s,%s,%s,%s,%s)""",
                    (gmt_created, project_code, building_code, property_name, building_name, open_date, houses, digest))
                self.connect.commit()
            except Exception as error:
                logging.error(error)
            return item
        else:
            pass
