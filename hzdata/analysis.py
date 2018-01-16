import logging
from hzdata.pipelines import HousePipeline


class Analysis(HousePipeline):

    def progress(self):
        sql = """
        SELECT 
          gmt_created,project_code,building_code,houses  
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
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            building_code_temp = 0
            for row in results:
                gmt_created = row[0]
                project_code = row[1]
                building_code = row[2]
                houses = row[3]
                if building_code != building_code_temp:
                    building_code_temp = building_code
                    

                print(gmt_created, project_code, building_code, houses)
        except Exception as error:
            logging.error(error)
        self.connect.close()


a = Analysis()
a.progress()
