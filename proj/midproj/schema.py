from abc import ABCMeta

from midproj.course import Course
class Schema():

    def __init__(self):
        self.id = 0
        self.name = ''
        self.title = ''
        self.major_id = 0
        self.intro1 = ''
        self.intro2 = ''
        self.intro3 = ''
        self.intro6 = ''
        self.enter_must = ''
        self.uni_must = ''
        self.uni_may = ''
        self.pro_abc = ''
        self.pro_core = ''
        self.pro_may = ''
        self.pro_do = ''

    @staticmethod
    def listToString(mylist):
        str=""
        for x in mylist:
            str+=x+"|"
        return str
    @staticmethod
    def stringToList(str):
        if(str==None):return []
        list=str.split("|")
        if(len(list)>0):
            del list[len(list)-1]
        return list
    @staticmethod
    def getJsonSchema(db,dep_code):
        flag=True
        sql = "select `id`,`name` from `major` where dep_code='%s'"%dep_code
        cursor = db.cursor()
        major_name = []
        major_id = []
        name_set = []
        id_set = []
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
        except:
            return ([],[],[],[])
        for x in res:

            major_name.append(x[1])
            major_id.append(x[0])
            new_name = []
            new_id = []
            sql = "select `id`,`name` from `courseSchema` where `major_id`=%d" % int(x[0])
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                res2 = cursor.fetchall()
                for j in res2:
                    new_id.append(j[0])
                    new_name.append(j[1])
                id_set.append(new_id)
                name_set.append(new_name)
            except Exception as e:
                print(e)
                return ([],[],[],[])
        if(not flag):return ([],[],[],[])
        return (major_id,major_name,id_set,name_set)

    def setSchemaById(self,db,schema_id):
        sql = sql = "select `id`,`name`,`major_id`,`intro1`,intro2,intro6,enter_must,uni_must,uni_may,pro_abc,pro_core,pro_may,pro_do,`title`,`intro3` from `courseSchema` where `id`=%d" % int(schema_id)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            res = cursor.fetchall()

            self.id=res[0][0]
            self.name=res[0][1]
            self.major_id=res[0][2]
            self.intro1=res[0][3]
            self.intro2=res[0][4]
            self.intro6=res[0][5]
            self.enter_must=Schema.stringToList(res[0][6])

            self.uni_must=Schema.stringToList(res[0][7])
            self.uni_may=Schema.stringToList(res[0][8])
            self.pro_abc=Schema.stringToList(res[0][9])
            self.pro_core=Schema.stringToList(res[0][10])
            self.pro_may=Schema.stringToList(res[0][11])
            self.pro_do=Schema.stringToList(res[0][12])
            print(res)
            self.title=res[0][13]
            self.intro3 = res[0][14]
            print(res)

        except Exception as e:
            return False
        return True
    def getSchemaInfo(self):
        info={}
        info['id']=self.id
        info['name']=self.name
        info['major_id']=self.major_id
        info['intro1']=self.intro1
        info['intro2']=self.intro2
        info['intro6'] = self.intro6
        info['title'] = self.title
        info['intro3'] = self.intro3
        return info
    def getCourse(self,db):
        course={}
        course['enter_must']=self.getCourseList(db,self.enter_must)
        course['uni_must']=self.getCourseList(db,self.uni_must)
        course['uni_may']=self.getCourseList(db,self.uni_may)
        course['pro_abc']=self.getCourseList(db,self.pro_abc)
        course['pro_core']=self.getCourseList(db,self.pro_core)
        course['pro_may']=self.getCourseList(db,self.pro_may)
        course['pro_do']=self.getCourseList(db,self.pro_do)
        return course
    def setBySchemaInfo(self,info):
        self.id=info['id']
        self.name=info['name']
        self.major_id=info['major_id']
        self.intro1=info['intro1']
        self.intro2=info['intro2']
        self.intro6=info['intro6']
        self.title=info['title']
        self.intro3 = info['intro3']
    def setByCourse(self,course):
        self.enter_must=self.getCourseNameList(course['enter_must'])
        self.uni_must = self.getCourseNameList(course['uni_must'])
        self.uni_may = self.getCourseNameList(course['uni_may'])
        self.pro_abc = self.getCourseNameList(course['pro_abc'])
        self.pro_core = self.getCourseNameList(course['pro_core'])
        self.pro_may = self.getCourseNameList(course['pro_may'])
        self.pro_do = self.getCourseNameList(course['pro_do'])
    def getCourseList(self,db,list):
        res=[]
        for code in list:
            cs=Course()
            cs.setById(db,code);
            res.append(cs.getDic())
        return res
    def getCourseNameList(self,course):
        list=[]
        for cs in course:
            list.append(cs['code'])
        return list
    @staticmethod
    def save(db,myschema):

        if(myschema.id<0):
            res=Schema.add(db,myschema)
        else:res=Schema.update(db,myschema)
        return res;
    @staticmethod
    def delete(db,id):
        print("hre=",id)
        sql = "delete from `courseSchema` where `id`=%d"% int(id)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            return False
        return True
    @staticmethod
    def update(db,schema):
        print("update schema")
        sql = "update `courseSchema` set name='%s',intro1='%s',intro2='%s',intro6='%s',enter_must='%s',uni_must='%s',uni_may='%s',pro_abc='%s',pro_core='%s',pro_may='%s',pro_do='%s',title='%s',intro3='%s' where id=%d" \
              % (schema.name, schema.intro1, schema.intro2, schema.intro6, \
                 schema.listToString(schema.enter_must), schema.listToString(schema.uni_must), schema.listToString(schema.uni_may), schema.listToString(schema.pro_abc), schema.listToString(schema.pro_core),
                 schema.listToString(schema.pro_may),schema.listToString(schema.pro_do),schema.title,schema.intro3,schema.id)
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return False
        return True
    @staticmethod
    def add(db,schema):
        sql = "insert into `courseSchema`(name,major_id,intro1,intro2,intro6,enter_must,uni_must,uni_may,pro_abc,pro_core,pro_may,pro_do,title,intro3)values('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"\
              %(schema.name,schema.major_id,schema.intro1,schema.intro2,schema.intro6, \
                schema.listToString(schema.enter_must), schema.listToString(schema.uni_may),
                schema.listToString(schema.uni_may), schema.listToString(schema.pro_abc),
                schema.listToString(schema.pro_core),
                schema.listToString(schema.pro_may), schema.listToString(schema.pro_do), schema.title,schema.intro3)
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return False
        sql = "SELECT LAST_INSERT_ID();"
        try:
            cursor.execute(sql)
            new_id = cursor.fetchall()
            db.commit()
        except:
            db.rollback()
            return False
        return new_id[0][0]