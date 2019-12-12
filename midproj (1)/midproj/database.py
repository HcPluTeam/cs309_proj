import pymysql
class database:
	def __init__(self, host='47.98.40.83', port=3306, user='root',
	             passwd='sustc@123SUSTC', db='hcpnb', charset='utf8'):
		self.host = host
		self.port = port
		self.user = user
		self.passwd = passwd
		self.db = db
		self.charset = charset
		self.conn = None
		self.cur = None
	def connect(self):
		try:
			self.conn=pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)
		except:
			return False
		self.cur=self.conn.cursor()
		return True
	#暂时没实现关闭
	def close(self):
		pass
	def execute(self,sql):
		connresult=self.connect()
		if not connresult:
			return False
		try:
			if self.conn and self.cur:
				#操作成功
				row=self.cur.execute(sql)
		except:
			return False
		return row
	def fethall(self,sql):
		res=self.execute(sql)
		if not res:
			return False
		result=self.cur.fetchall()
		return result
	def executesql(self,sql):
		try:
			self.cur.execute(sql)
			self.conn.commit()
			return True
		except:
			self.conn.rollback()
			return False

