import pymysql
class Course:
    name = ''
    dep_code = ''
    num_code = ''
    score = 0
    lab_score=0
    require = ''
    season = 0
    code=''
    def __init__(self):
        pass
    def setById(self,db,code):
        db = pymysql.connect(host='47.98.40.83', port=3306, user='root', passwd='sustc@123SUSTC', db='Test',
                               charset='utf8')
        self.code=code;
        flag=True
        cursor = db.cursor()
        sql = "select `pre2019coursecode`,c.course_name,`pre2019score`,`pre2019labscore`,`pre2019courseneed`,`pre2019season` from `pre2019` join course c on `pre2019`.`pre2019coursecode` = c.course_code where c.course_code='%s';"%code
        try:
            cursor.execute(sql)
            res= cursor.fetchall()
            if not res:return False
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
    def getDic(self):
        dic={}
        dic["code"]=self.code;
        dic["dep_code"]=self.dep_code;
        dic["num_code"]=self.num_code
        dic["score"]=self.score
        dic["name"]=self.name
        dic["lab_score"]=self.lab_score
        dic["require"]=self.require
        dic["season"]=self.season
        return dic
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

