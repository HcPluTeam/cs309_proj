import pymysql
class course:
    name = ''
    dep_code = ''
    num_code = ''
    score = 0
    lab_score=0
    require = ''
    season = 0
    def __init__(self):
        pass
    def setById(self,db,code):
        db = pymysql.connect(host='47.98.40.83', port=3306, user='root', passwd='sustc@123SUSTC', db='hcpnb',
                               charset='utf8')
        print("course_id=",code)
        flag=True
        cursor = db.cursor()
        sql = "select `2019pre_coursecode`,c.course_name,`2019pre_score`,`2019pre_labscore`,`2019pre_courseneed`,`2019pre_season` from `2019pre` join course c on `2019pre`.`2019pre_coursecode` = c.course_code where c.course_code='%s';"%code
        try:
            cursor.execute(sql)
            print(2)
            res= cursor.fetchall()
            print("res=",res)
            for row in res:
                self.dep_code,self.num_code = self.__seperatecode__(row[0])
                self.name = row[1]
                self.score = int(row[2])
                self.lab_score = int(row[3])
                self.require = row[4]
                self.season = row[5]
        except Exception as e:
            print("error=",e)
            flag=False
        return flag
    def __seperatecode__(self,code):
        dep_code=''
        num_code=''
        flag=True
        for i in range(len(code)):
            if((code[i]<'a' or code[i]>'z' )and(code[i]<'A' or code[i]>'Z' ) ):
                flag=False
            if(flag):
                dep_code += code[i]
            else:
                num_code += code[i]
        return [dep_code,num_code]

