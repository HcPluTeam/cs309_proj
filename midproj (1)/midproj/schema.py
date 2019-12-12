from abc import ABCMeta

class schema():
    id=0
    name=''
    major_id=0
    intro1=''
    intro2=''
    intro6=''
    enter_must=''
    uni_must=''
    uni_may=''
    pro_abc=''
    pro_core=''
    pro_may=''
    pro_do=''
    def __init__(self):
        pass

    @staticmethod
    def listToString(mylist):
        str=""
        for x in mylist:
            str+=x+"|"
        return str
    @staticmethod
    def stringToList(str):
        list=str.split("|")
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
            sql = "select `id`,`name` from `schema` where `major_id`=%d" % int(x[0])
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
    def querySchema(db,schema_id):
        flag=True
        new_schema = schema()
        print(schema_id)
        sql = sql = "select `id`,`name`,'major_id',`intro1`,intro2,intro6,enter_must,uni_must,uni_may,pro_abc,pro_core,pro_may,pro_do from `schema` where `id`=%d" % int(schema_id)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            new_schema.id=res[0][0]
            new_schema.name=res[0][1]
            new_schema.major_id=res[0][2]
            new_schema.intro1=res[0][3]
            new_schema.intro2=res[0][4]
            new_schema.intro6=res[0][5]
            new_schema.enter_must=schema.stringToList(res[0][6])
            new_schema.uni_must=schema.stringToList(res[0][7])
            new_schema.uni_may=schema.stringToList(res[0][8])
            new_schema.pro_abc=schema.stringToList(res[0][9])
            new_schema.pro_core=schema.stringToList(res[0][10])
            new_schema.pro_may=schema.stringToList(res[0][11])
            new_schema.pro_do=schema.stringToList(res[0][12])
        except Exception as e:
            print(e)
            flag=False
        if(flag):return new_schema
        else:return False
    @staticmethod
    def save(db,myschema):
        if(myschema.id<0):
            schema.add(db,myschema)
        else:schema.update(db,myschema)
    @staticmethod
    def delete(db,id):
        flag = True
        sql = "delete from `schema` where `id`=%d"% schema.id
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            flag = False
        db=db.conn
        return flag
    @staticmethod
    def update(db,schema):
        flag = True
        sql = "update `schema` set name='%s',intro1='%s',intro2='%s',intro6='%s',enter_must='%s',uni_must='%s',uni_may='%s',pro_abc='%s',pro_core='%s',pro_may='%s',pro_do='%s' where id=%d" \
              % (schema.name, schema.intro1, schema.intro2, schema.intro6, \
                 schema.listToString(schema.enter_must), schema.listToString(schema.uni_may), schema.listToString(schema.uni_may), schema.listToString(schema.pro_abc), schema.listToString(schema.pro_core),
                 schema.listToString(schema.pro_may),schema.listToString(schema.pro_do),schema.id)
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            flag=False
        return flag
    @staticmethod
    def add(db,schema):
        flag=True
        sql = "insert into `schema`(name,major_id,intro1,intro2,intro6,enter_must,uni_must,uni_may,pro_abc,pro_core,pro_may,pro_do)values('%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"\
              %(schema.name,schema.major_id,schema.intro1,schema.intro2,schema.intro6, \
                schema.listToString(schema.enter_must), schema.listToString(schema.uni_may),
                schema.listToString(schema.uni_may), schema.listToString(schema.pro_abc),
                schema.listToString(schema.pro_core),
                schema.listToString(schema.pro_may), schema.listToString(schema.pro_do))
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            flag=False
        sql = "SELECT LAST_INSERT_ID();"
        try:
            cursor.execute(sql)
            new_id = cursor.fetchall()
            db.commit()
        except:
            db.rollback()
            flag=False
        if(flag):return new_id[0][0]
        else: return False