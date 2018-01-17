import logging
from hzdata.pipelines import HousePipeline
from datetime import *


class Analysis(HousePipeline):

    def progress(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        analyze_sql = """
        SELECT 
          gmt_created,project_code,building_code,houses,property_name,building_name  
        FROM
          building 
        WHERE building_code IN 
          (SELECT DISTINCT 
            bc 
          FROM
            (SELECT 
              building_code AS bc,
              digest AS MD5,
              COUNT(digest) cnt 
            FROM
              building 
            WHERE gmt_created >= DATE_FORMAT(DATE_ADD(NOW(),INTERVAL 0 DAY),'%Y-%m-%d')
            GROUP BY building_code,digest 
            HAVING COUNT(digest) < 2 
            ORDER BY bc
            ) t) AND gmt_created >= DATE_FORMAT(DATE_ADD(NOW(),INTERVAL 0 DAY),'%Y-%m-%d')
        ORDER BY building_code 
        """
        save_sql = """
        insert into contract(gmt_created,project_code,building_code,property_name,building_name, house_code,new_state, 
                    old_state, contract_date) 
                    value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            self.cursor.execute(analyze_sql)
            buildings_records = self.cursor.fetchall()
            building_code_temp = 0
            record_temp = []
            for record in buildings_records:
                project_code = record[1]
                building_code = record[2]
                houses = record[3]
                property_name = record[4]
                building_name = record[5]
                if building_code != building_code_temp:
                    building_code_temp = building_code
                    record_temp = record
                else:
                    houses_temp = record_temp[3]
                    if houses == "" or houses_temp == "":
                        continue
                    house_list_temp = str(houses_temp).split(",")
                    house_list = str(houses).split(",")
                    for (house_temp, house) in zip(house_list_temp, house_list):
                        if house_temp != house:
                            house_code = str(house).split("|")[0]
                            new_state = str(house).split("|")[1]
                            old_state = str(house_temp).split("|")[1]
                            self.cursor.execute(save_sql, (datetime.now(), project_code, building_code, property_name,
                                                           building_name, house_code, new_state, old_state, yesterday))

                            # print(project_code, building_code, house_code, property_name, building_name, new_state, old_state)
            self.connect.commit()
        except Exception as error:
            logging.error(error)
        self.connect.close()


a = Analysis()
a.progress()
