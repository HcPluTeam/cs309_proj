from flask import Flask,request,render_template,flash,redirect,make_response
from database import database
import os
app = Flask(__name__)
db=database()
app.secret_key = 'hcpnb'
def r2(path):
	chapter = ""
	with open(path, 'r', encoding='utf-8') as f:
		while True:
			line = f.readline()
			chapter += line
			if not line:
				break
	return chapter
def readcontent(year,dept):
	chapterlist=[]
	for i in range(1,11):
		try:
			pathi="F:/ooadfiles/midproj/description/"+str(year)+"/"+ str(dept) + '/chapter'+str(i)+'.txt'
			chapteri=r2(pathi)
		except:
			chapteri=""
		chapterlist.append(chapteri)
	return chapterlist
def infocheck(thisstate,thisid):
	if thisstate is None:thisstate='N'
	if thisid is None:thisid='0'
	glousercode=request.cookies.get('usercode') if request.cookies.get('usercode') is not None else '0'
	sql = "select * from user2 where user2.userid='" + thisid+ "' and user2.userauth='" + thisstate + "' and user2.usercode='" + glousercode + "';"
	result =db.fethall(sql)
	return result
@app.route('/')
def index():
	response=make_response(render_template('index.html'))
	response.set_cookie('userid', '0')
	response.set_cookie('usercode', '0')
	response.set_cookie('userauth', 'N')
	return response

@app.route('/logout/')
def logout():
	response = make_response(render_template('logout.html'))
	response.delete_cookie('userid')
	response.delete_cookie('usercode')
	response.delete_cookie('userauth')
	return response

@app.route('/login/',methods=['GET','POST'])
def login():
	glouserid=request.cookies.get('userid') if request.cookies.get('userid') is not None else '0'
	glousercode=request.cookies.get('usercode') if request.cookies.get('usercode') is not None else '0'
	glouserstate=request.cookies.get('userauth') if request.cookies.get('userauth') is not None else 'N'
	sql="select * from user2 where user2.userid='" + glouserid + "' and user2.userauth='"+glouserstate+"' and user2.usercode='"+glousercode+"';"
	result = str(db.fethall(sql))
	if result==False:
		pass
	else:
		if glouserstate=='S':return redirect('/student/'+(glouserid)+"/")
		if glouserstate=='C':return redirect('/checher/'+(glouserid)+"/")
		if glouserstate=='D':return redirect('/dept/'+(glouserid)+"/")
	if request.method=='GET':
		return render_template('login.html')
	else:
		userid = request.form.get('login_userid')
		password = request.form.get('login_usercode')
		if userid is None or password is None or userid == '' or password == '':
			flash(message='input cannot be null',category='danger')
			return render_template('login.html')
		sql = "select * from user2 where user2.userid='" + userid + "';"
		result = str(db.fethall(sql))
		if result == '()':
			flash(message='wrong username or password',category='danger')
			return render_template('login.html')
		else:
			result = result.replace('(', '').replace(')', '').replace("'", "").replace(' ', '').split(',')
			if result[0] == userid and result[1] == password:
				if result[2]=='S':
					response=make_response(redirect('/student/'+userid+"/"))
					response.set_cookie('userauth','S')
					response.set_cookie('usercode',password)
					response.set_cookie('userid',userid)
					return response
				elif result[2]=='C':
					response=make_response(redirect('/checker/' + userid+"/"))
					response.set_cookie('userauth', 'C')
					response.set_cookie('usercode', password)
					response.set_cookie('userid', userid)
					return response
				elif result[2]=='D':
					response=make_response(redirect('/dept/' + userid+"/"))
					response.set_cookie('userauth', 'D')
					response.set_cookie('usercode', password)
					response.set_cookie('userid', userid)
					return response
			else:
				flash(message='wrong username or password',category='danger')
				return render_template('login.html')
@app.route('/student/<thisid>/',methods=['GET'])
def studentview(thisid):
	if request.method=='GET':
		if infocheck('S', thisid) == False:
			return "404 not found!"
		return render_template('studentpage.html',userid=thisid,userauth='student')

@app.route('/dept/<thisid>/',methods=['GET'])
def deptview(thisid):
	if not infocheck('D',thisid): return "404 not found!"
	if request.method=='GET':
		return render_template('deptpage.html',userid=thisid,userauth='dept')

@app.route('/checker/<thisid>/',methods=['GET'])
def checkerview(thisid):
	if not infocheck('C',thisid):return "404 not found!"
	if request.method=='GET':
		return render_template('checkerpage.html',userid=thisid,userauth='checker')

"现在暂时不管谁调用这个modify，只写方法，检验身份应该在一开始就验证"
"makeafile()需要传入的是系，和成员身份。之后处理，如果是POST就交付了，应该记住输入的内容。"
"关于查看输入的内容，是否应该即时显示呢？比如添加一行之后就显示样子"
"如果是GET，那也应该获得原来的那些内容，方便保存"


@app.route('/<character>/<thisid>/query/',methods=['GET','POST'])
#这个用于查询任何系的培养方案.character是角色类型，应该是'student',thisid是id,是'11914001'
def query(character,thisid):
	sql = "select * from dptdet order by dptdet_index"
	result = db.fethall(sql)
	if request.method=='GET':
		return render_template('query.html',character=character,thisid=thisid,result=result,curdpt='',str2=str)
	else:
		dpt=request.form.get("select_dptdept")
		sql="select `2019pre_coursecode`,c.course_name,`2019pre_score`,`2019pre_labscore`,`2019pre_coursetype`,`2019pre_courseneed`,`2019pre_bigdpt`,`2019pre_season` from `2019pre` join course c on `2019pre`.`2019pre_coursecode` = c.course_code where `2019pre_dpt`="+dpt+";"
		dptresult=db.fethall(sql)
		try:
			sql="select * from dptdet where dptdet_index="+dpt+";"
			curdpt=db.fethall(sql)[0][1]
		except:
			curdpt=''
		return render_template('query.html',character=character,thisid=thisid,dptresult=dptresult,result=result,curdpt=curdpt)
@app.route('/student/<thisid>/havelearned/',methods=['GET'])
def havelearned(thisid):
	try:
		sql = "select userdept from user2 where userid='" + thisid + "';"
		dept = db.fethall(sql)[0][0]
		sql="select c.course_code,c.course_name,p.2019pre_score,p.2019pre_labscore,p.2019pre_coursetype from studentlearn s join course c on s.courseid = c.course_index join 2019pre p on c.course_code = p.2019pre_coursecode where s.studentid='"+thisid+"' and p.2019pre_dpt="+dept+";"
		courseresult=db.fethall(sql)
		return render_template('havelearned.html',courseresult=courseresult,dept=dept)
	except:
		return "Something Error Happened"

@app.route('/<character>/<thisid>/modify/',methods=['GET','POST'])
def modify(character,thisid):
	try:
		sql="select userdept from user2 where userid='"+thisid+"';"
		dept=db.fethall(sql)[0][0]
		sql="select `2019pre_coursecode`,c.course_name,`2019pre_score`,`2019pre_labscore`,`2019pre_coursetype`,`2019pre_courseneed`,`2019pre_bigdpt`,`2019pre_season` from `2019pre` join course c on `2019pre`.`2019pre_coursecode` = c.course_code where `2019pre_dpt`="+dept+" order by field(`2019pre_coursetype`,'E','EA','EB','EC','C','CA','CB','CC','O','OA','OB','OC','P') ;"
		course=db.fethall(sql)
		sql = "select `2019pre_coursecode`,c.course_name,`2019pre_score`,`2019pre_labscore`,`2019pre_coursetype`,`2019pre_courseneed`,`2019pre_bigdpt`,`2019pre_season` from `2019pre` join course c on `2019pre`.`2019pre_coursecode` = c.course_code where `2019pre_dpt`=" + dept + " and `2019pre_labscore`!=-1 order by field(`2019pre_coursetype`,'E','EA','EB','EC','C','CA','CB','CC','O','OA','OB','OC','P') ;"
		labcourse = db.fethall(sql)
		sql="select dptdet_name from dptdet where dptdet_index="+dept+";"
		deptname=db.fethall(sql)[0][0]
	except:
		return "Something Error Happened"
	if request.method=='GET':
		#测试用
		#chapterlist=readcontent(2019,dept)
		sql="select content from yearsdeptsch where years=2019 and dept="+dept+";"
		result=db.fethall(sql)
		chapterlist=[]
		for i in result:
			if i[0] is None:chapterlist.append('')
			else:chapterlist.append(i[0])
		return render_template('modify.html',character=character,thisid=thisid,course=course,labcourse=labcourse,deptname=deptname,chapterlist=chapterlist)
	else:return "successpost"
@app.route('/<character>/<thisid>/check/',methods=['GET','POST'])
def check(character,thisid):
	if request.method == 'GET':
		return render_template('check.html')
	else:return

@app.route('/help/',methods=['GET'])
def help():
	return render_template('help.html')
@app.route('/checker/<thisid>/addingcourse/',methods=['GET','POST'])
def addingcourse(thisid):
	if request.method=='GET':
		return render_template('addingcourse.html',thisid=thisid)
	else:
		coursename=request.form.get("course_name")
		coursecode=request.form.get("course_code")
		if coursename=='' or coursecode=='':
			flash("输入不能为空","danger")
			return render_template('addingcourse.html', thisid=thisid)
		print(coursename,' ',coursecode)
		sql="insert into course (course_name,course_code) values ('"+coursename+"','"+coursecode+"');"
		flag=db.executesql(sql)
		if flag==True:
			flash("添加成功!", "success")
		else:
			flash("添加失败!","danger")
		return render_template('addingcourse.html',thisid=thisid)
@app.route('/dept/<thisid>/addingpre/delete/<deptid>/<code>')
def delete(thisid,deptid,code):
	sql="delete from 2019pre where 2019pre_dpt="+deptid+" and 2019pre_coursecode='"+code+"';"
	f=db.executesql(sql)
	if f:
		flash("删除成功!","success")
	else:
		flash("删除失败!","danger")
	rtz="/dept/"+str(thisid)+"/addingpre/"
	return redirect(rtz)
@app.route('/dept/<thisid>/addingpre/',methods=['GET','POST'])
def addingpre(thisid):
	#先假定这个人可以正确操作这个系统
	sql = "select userdept from user2 where userid='" + thisid + "';"
	dept = db.fethall(sql)[0][0]
	sql = "select dptdet_name from dptdet where dptdet_index=" + dept + ";"
	deptname = db.fethall(sql)[0][0]
	sql = "select `2019pre_coursecode`,c.course_name,`2019pre_score`,`2019pre_labscore`,`2019pre_coursetype`,`2019pre_courseneed`,`2019pre_bigdpt`,`2019pre_season` from `2019pre` join course c on `2019pre`.`2019pre_coursecode` = c.course_code where `2019pre_dpt`=" + dept + " order by field(`2019pre_coursetype`,'E','EA','EB','EC','C','CA','CB','CC','O','OA','OB','OC','P') ;"
	course = db.fethall(sql)

	if request.method=='GET':
		return render_template("addingpre.html",deptname=deptname,dept=dept,thisid=thisid,course=course)
	else:
		t1=request.form.get("t1")
		t2 = request.form.get("t2")
		t3 = request.form.get("t3")
		t4= request.form.get("t4")
		t5 = request.form.get("t5")
		t6 = request.form.get("t6")
		t8=request.form.get("t8")
		if t1=="" or t2=="" or t3=="" or t4=="" or t5=="" or t6=="" or t8=="":
			flash("输入不能为空", "danger")
			return render_template('addingpre.html', deptname=deptname,dept=dept,thisid=thisid,course=course)
		sql="insert into 2019pre (2019pre_coursecode,2019pre_score,2019pre_labscore,2019pre_coursetype,2019pre_courseneed,2019pre_bigdpt,2019pre_dpt,2019pre_season)"
		sql+="values('"+t1+"',"+t2+","+t3+",'"+t4+"','"+t5+"','"+t6+"',"+dept+",'"+t8+"');"
		flag=db.executesql(sql)
		if flag==True:
			flash("添加成功!", "success")
		else:
			flash("添加失败!","danger")
		return render_template("addingpre.html",deptname=deptname,dept=dept,thisid=thisid,course=course)

@app.route('/dept/<thisid>/submitcontent/',methods=['GET','POST'])
def submitcontent(thisid):
	try:
		years = 2019
		sql = "select userdept from user2 where userid='" + thisid + "';"
		dept = db.fethall(sql)[0][0]
		sql = "select dptdet_name from dptdet where dptdet_index=" + dept + ";"
		deptname = db.fethall(sql)[0][0]
		sql = "select content from yearsdeptsch where years="+str(years)+" and dept=" + dept + ";"
		result = db.fethall(sql)
		chapterlist = []
		for i in result:
			if i[0] is None:
				chapterlist.append('')
			else:
				chapterlist.append(i[0])
	except:
		return "Something Error Happened!"
	if request.method=='GET':
		if request.args.get('t1') is not None:
			flag = True
			list = []
			list.append([])
			for i in range(1, 11):
				str1 = 't' + str(i)
				d=request.args.get(str1)
				if d is None :d=''
				list.append(d)
				print(d)
			for i in range(1, 11):
				sql = "update yearsdeptsch set content='" + list[i] + "' where years=" + str(
					years) + " and dept=" + str(dept) + " and part=" + str(i) + ";"
				flag = flag & (db.executesql(sql))
			if flag:
				flash("上传成功", 'success')
			else:
				flash('上传失败', 'danger')
		sql = "select content from yearsdeptsch where years=" + str(years) + " and dept=" + dept + ";"
		result = db.fethall(sql)
		chapterlist = []
		for i in result:
			if i[0] is None:
				chapterlist.append('')
			else:
				chapterlist.append(i[0])
		return render_template('submitcontent.html',deptname=deptname,chapterlist=chapterlist)
	else:
		return "successpost"
@app.route('/login_help/',methods=['GET'])
def login_help():
	flash("账户注册、忘记密码，请发邮件联系11711715@mail.sustech.edu.cn","info")
	return redirect('/login/')
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=6657)

