# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from hzdata import settings
from hzdata.pipelines import HousePipeline
import logging
from datetime import *


class Analysis(HousePipeline):

    def progress(self):
        analyze_day = 0 - int(settings.SPIDER_DAY)
        pre_day = int(analyze_day - 1)
        today = date.today()
        yesterday = today + timedelta(days=(analyze_day-1))
        current_sql = """
        SELECT project_code,building_code,property_name,building_name,houses,digest,gmt_created FROM building 
        where gmt_created = DATE_FORMAT(DATE_ADD(NOW(),INTERVAL %d DAY),'%%Y-%%m-%%d') 
        """ % analyze_day
        previous_sql = """
        SELECT project_code,building_code,property_name,building_name,houses,digest,gmt_created FROM building 
        where gmt_created = DATE_FORMAT(DATE_ADD(NOW(),INTERVAL %d DAY),'%%Y-%%m-%%d') 
        """ % pre_day
        save_sql = """
        insert into contract(gmt_created,project_code,building_code,property_name,building_name,house_code,new_state, 
                    old_state, contract_date) 
                    value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        delete_houses = """
        DELETE FROM house WHERE DATE_FORMAT(gmt_created,'%Y-%m-%d') = DATE_FORMAT(DATE_ADD(NOW(),INTERVAL -3 DAY),
        '%Y-%m-%d')
        """
        try:
            self.cursor.execute(current_sql)
            current_buildings = self.cursor.fetchall()
            self.cursor.execute(previous_sql)
            previous_buildings = self.cursor.fetchall()
            for current_building in current_buildings:
                cur_project_code = current_building[0]
                cur_building_code = current_building[1]
                cur_property_name = current_building[2]
                cur_building_name = current_building[3]
                cur_houses = current_building[4]
                cur_digest = current_building[5]
                for previous_building in previous_buildings:
                    pre_building_code = previous_building[1]
                    pre_houses = previous_building[4]
                    pre_digest = previous_building[5]
                    if cur_building_code == pre_building_code and cur_digest != pre_digest:
                        cur_house_array = str(cur_houses).split(",")
                        pre_house_array = str(pre_houses).split(",")
                        for index, cur_house in enumerate(cur_house_array):
                            if cur_house != pre_house_array[index]:
                                house_code = str(cur_house).split("|")[0]
                                new_state = str(cur_house).split("|")[1]
                                old_state = str(pre_house_array[index]).split("|")[1]
                                self.cursor.execute(save_sql,
                                                (datetime.now(), cur_project_code, cur_building_code,
                                                 cur_property_name, cur_building_name, house_code, new_state,
                                                 old_state, yesterday))
            self.cursor.execute(delete_houses)
            self.connect.commit()
        except Exception as error:
            logging.error(error)
        self.connect.close()


if __name__ == '__main__':
    a = Analysis()
    a.progress()
