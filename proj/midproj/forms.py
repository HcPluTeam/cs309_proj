from midproj import db

class Fornum(db.Model):
	__tablename__ = 'fornum'

	fornumindex =db.Column(db.Integer, primary_key=True)
	fornumhead = db.Column(db.String(10), nullable=False)
	fornumcontent = db.Column(db.Text)
	fornumsender = db.Column(db.String(16), nullable=False)


class Course(db.Model):
	__tablename__ = 'course'

	course_index = db.Column(db.Integer, primary_key=True)
	course_name = db.Column(db.String(45), nullable=False)
	course_code = db.Column(db.String(13), nullable=False, unique=True)
class Department(db.Model):
	__tablename__ = 'department'

	code = db.Column(db.String(10), primary_key=True)
	name = db.Column(db.String(40), nullable=False)
class Dptdet(db.Model):
	__tablename__ = 'dptdet'

	dptdet_index = db.Column(db.Integer, primary_key=True)
	dptdet_name = db.Column(db.String(20), nullable=False, unique=True)
class Major(db.Model):
	__tablename__ = 'major'

	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(80), nullable=False)
	dep_code = db.Column(db.ForeignKey('department.code'), index=True)

	department = db.relationship('Department', primaryjoin='Major.dep_code == Department.code', backref='majors')
class Pre2019(db.Model):
	__tablename__ = 'pre2019'
	__table_args__ = (
		db.Index('2019pre_2019pre_coursecode_2019pre_coursetype_2019pre_dpt_uindex', 'pre2019coursecode', 'pre2019coursetype', 'pre2019dpt'),
	)

	pre2019coursecode = db.Column(db.ForeignKey('course.course_code'), nullable=False)
	pre2019score = db.Column(db.Float, nullable=False)
	pre2019labscore = db.Column(db.Float, nullable=False)
	pre2019coursetype = db.Column(db.String(10), nullable=False)
	pre2019courseneed = db.Column(db.String(90), nullable=False)
	pre2019bigdpt = db.Column(db.String(10), nullable=False)
	pre2019dpt = db.Column(db.ForeignKey('dptdet.dptdet_index'), nullable=False, index=True)
	pre2019season = db.Column(db.String(10), nullable=False)
	pre2019index = db.Column(db.Integer, primary_key=True)

	course = db.relationship('Course', primaryjoin='Pre2019.pre2019coursecode == Course.course_code', backref='pre2019s')
	dptdet = db.relationship('Dptdet', primaryjoin='Pre2019.pre2019dpt == Dptdet.dptdet_index', backref='pre2019s')
class Prefordept(db.Model):
	__tablename__ = 'prefordept'
	__table_args__ = (
		db.Index('uq_index', 'dept', 'coursecode', 'oneortwo', 'year'),
	)

	coursecode = db.Column(db.ForeignKey('course.course_code'), nullable=False, index=True)
	dept = db.Column(db.ForeignKey('dptdet.dptdet_index'), nullable=False)
	oneortwo = db.Column(db.Integer, nullable=False)
	year = db.Column(db.Integer, nullable=False)
	index = db.Column(db.Integer, primary_key=True)

	course = db.relationship('Course', primaryjoin='Prefordept.coursecode == Course.course_code', backref='prefordepts')
	dptdet = db.relationship('Dptdet', primaryjoin='Prefordept.dept == Dptdet.dptdet_index', backref='prefordepts')
class Schema(db.Model):
	__tablename__ = 'schema'

	id = db.Column(db.Integer, primary_key=True, unique=True)
	name = db.Column(db.String(100))
	major_id = db.Column(db.Integer, nullable=False)
	intro1 = db.Column(db.String)
	intro2 = db.Column(db.String)
	intro6 = db.Column(db.String)
	enter_must = db.Column(db.String(700))
	uni_must = db.Column(db.String(700))
	uni_may = db.Column(db.String(700))
	pro_abc = db.Column(db.String(700))
	pro_core = db.Column(db.String(700))
	pro_may = db.Column(db.String(700))
	pro_do = db.Column(db.String(700))
class Studentlearn(db.Model):
	__tablename__ = 'studentlearn'
	__table_args__ = (
		db.Index('studentlearn_studentid_courseid_uindex', 'studentid', 'courseid'),
	)

	index = db.Column(db.Integer, primary_key=True)
	studentid = db.Column(db.ForeignKey('user2.userid'), nullable=False)
	courseid = db.Column(db.ForeignKey('course.course_index'), nullable=False, index=True)

	course = db.relationship('Course', primaryjoin='Studentlearn.courseid == Course.course_index', backref='studentlearns')
	user2 = db.relationship('User2', primaryjoin='Studentlearn.studentid == User2.userid', backref='studentlearns')
class User2(db.Model):
	__tablename__ = 'user2'

	userid = db.Column(db.String(8), primary_key=True)
	usercode = db.Column(db.String(20), nullable=False)
	userauth = db.Column(db.String(10), nullable=False)
	username = db.Column(db.String(20), nullable=False)
	userdept = db.Column(db.String(20), nullable=False)
	def __init__(self,userid):
		self.userid=userid
class Checker(User2):
	def __init__(self,userid):
		User2.__init__(self,userid)
		self.userauth='checker'
		self.observers=[]
	def addobserver(self,observer):
		self.observers.append(observer)
	def notifystr(self,str0):
		for observer in self.observers:
			observer.updatemail(str0)

class Dept(User2):
	def __init__(self,userid):
		User2.__init__(self,userid)
		self.userauth='dept'
		self.mailbox=[]
	def updatemail(self,str0):
		self.mailbox.append(str0)

class Yearsdeptsch(db.Model):
	__tablename__ = 'yearsdeptsch'
	__table_args__ = (
		db.Index('yearsdeptsch_years_content_dept_index', 'years', 'part', 'dept'),
	)

	index = db.Column(db.Integer, primary_key=True)
	years = db.Column(db.Integer, nullable=False)
	dept = db.Column(db.ForeignKey('dptdet.dptdet_index'), nullable=False, index=True)
	part = db.Column(db.Integer, nullable=False)
	content = db.Column(db.Text)

	dptdet = db.relationship('Dptdet', primaryjoin='Yearsdeptsch.dept == Dptdet.dptdet_index', backref='yearsdeptsches')

deptuser={}
checkeruser={}
def initit():
	allchecker=User2.query.filter_by(userauth='checker').with_entities(User2.userid)
	alldept=User2.query.filter_by(userauth='dept').with_entities(User2.userid)
	for i in allchecker:
		checkeruser[i[0]]=(Checker(userid=i[0]))
	for i in alldept:
		deptuser[i[0]]=(Dept(userid=i[0]))
	for i in checkeruser:
		for j in deptuser:
			checkeruser[i].addobserver(deptuser[j])