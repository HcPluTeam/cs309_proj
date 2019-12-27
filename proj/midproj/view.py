from midproj.forms import User2,Course,Checker,Dptdet,Dept,Pre2019,Yearsdeptsch,Studentlearn,Fornum,deptuser,checkeruser,initit
from midproj import db,app
import  xlrd
import pdfkit
from flask import jsonify,	send_from_directory, json
from midproj import mydb
from midproj.schema import Schema as mySchema
from midproj.course import Course as myCourse
from flask import Flask,request,render_template,flash,redirect,make_response,url_for
#安全性处理，这个最后再加入
initit()
def infocheck(thisid,thisauth):

	if request.cookies.get('userid')!=thisid or request.cookies.get('userauth')!=thisauth:
		response=make_response(redirect('/login/'))
		response.set_cookie('userid', '0')
		response.set_cookie('usercode', '0')
		response.set_cookie('userauth', 'N')
		return redirect('/login/')

@app.route('/')
def index():
	response=make_response(render_template('index.html'))
	response.set_cookie('userid', '0')
	response.set_cookie('userauth', 'N')
	return response
@app.route('/fornum/',methods=['GET'])
def fornum():
	if request.method=='GET':
		tofo={}
		rez=Fornum.query.with_entities(Fornum.fornumhead,Fornum.fornumsender,Fornum.fornumcontent)
		for i in rez:
			if i[0] not in tofo.keys():
				tofo[i[0]]=[]
			tofo[i[0]].append((i[1],i[2]))
		print(tofo)
		return render_template('fornum.html',tofo=tofo)
	else:return "Method Not Allowed!"
@app.route('/fornum/new/',methods=['GET','POST'])
def fornumnew():
	if request.method=='GET':
		return render_template('fornumnew.html')
	else:
		name = request.form.get('t0')
		title = request.form.get('t1')
		content = request.form.get('t2')
		print(name,title,content)
		try:
			db.session.add(Fornum(fornumhead=title,fornumsender=name,fornumcontent=content))
			db.session.commit()
			flash('发帖成功!','success')
		except:
			db.session.rollback()
			flash('发帖失败!','danger')
		return redirect('/fornum/')
@app.route('/fornum/reply/',methods=['GET','POST'])
def fornumreply():
	if request.method == 'GET':
		titles=set()
		result=Fornum.query.with_entities(Fornum.fornumhead)
		for i in result:
			titles.add(i[0])
		print(titles)
		return render_template('fornumreply.html',titles=titles)
	else:
		name = request.form.get('t0')
		title = request.form.get('t1')
		content = request.form.get('t2')
		print(name, title, content)
		try:
			db.session.add(Fornum(fornumhead=title, fornumsender=name, fornumcontent=content))
			db.session.commit()
			flash('回复成功!', 'success')
		except:
			db.session.rollback()
			flash('回复失败!', 'danger')
		return redirect('/fornum/')

@app.route('/logout/')
def logout():
	response = make_response(render_template('logout.html'))
	response.delete_cookie('userid')
	response.delete_cookie('userauth')
	return response

@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')
	else:
		userid = request.form.get('login_userid')
		password = request.form.get('login_usercode')
		if userid is None or password is None or userid == '' or password == '':
			flash(message='输入不能为空',category='danger')
			return render_template('login.html')
		result=User2.query.filter_by(userid=userid,usercode=password).with_entities(User2.userauth).first()
		if result is None or result=='':
			flash(message='用户名或密码错误',category='danger')
			return render_template('login.html')
		else:
			newhtml='/'+str(result[0])+'/'+ userid+"/"
			response = make_response(redirect(newhtml))
			response.set_cookie('userauth', str(result[0]))
			response.set_cookie('userid', userid)
			return response
@app.route('/<character>/<thisid>/',methods=['GET'])
def characterview(character,thisid):
	try:
		thisdept=deptuser[str(thisid)]
		print(thisdept.mailbox)
	except:pass
	if request.method=='GET':
		try:
			html=character+'page.html'
			name=User2.query.filter_by(userid=thisid,userauth=character).with_entities(User2.username).first()[0]
			return render_template(html, userid=thisid, userauth=character, name=name)
		except:pass

@app.route('/<character>/<thisid>/query/',methods=['GET','POST'])#还没改
#这个用于查询任何系的培养方案.character是角色类型，应该是'student',thisid是id,是'11914001'
def query(character,thisid):
	result=Dptdet.query.with_entities(Dptdet.dptdet_index,Dptdet.dptdet_name).order_by(Dptdet.dptdet_index)
	if request.method=='GET':
		return render_template('query.html',character=character,thisid=thisid,result=result,curdpt='',str2=str)
	else:
		dpt=request.form.get("select_dptdept")
		k=Pre2019.query.filter_by(pre2019dpt=dpt).join(Course, (Course.course_code == Pre2019.pre2019coursecode)).with_entities(
			Pre2019.pre2019coursecode, Course.course_name, Pre2019.pre2019score, Pre2019.pre2019labscore,
			Pre2019.pre2019coursetype, Pre2019.pre2019courseneed,
			Pre2019.pre2019bigdpt, Pre2019.pre2019season
		)
		try:
			curdpt=Dptdet.query.filter_by(dptdet_index=dpt).with_entities(Dptdet.dptdet_name).first()[0]
		except:
			curdpt=''
		return render_template('query.html',character=character,thisid=thisid,dptresult=k,result=result,curdpt=curdpt)
@app.route('/student/<thisid>/havelearned/',methods=['GET'])#还没改
def havelearned(thisid):
		dept=User2.query.filter_by(userid=thisid).with_entities(User2.userdept).first()[0]
		courseresult = Studentlearn.query.join(Course, (Course.course_index == Studentlearn.courseid)).join(Pre2019,(Pre2019.pre2019coursecode==Course.course_code)).filter(Studentlearn.studentid==thisid,Pre2019.pre2019dpt==dept).with_entities(
			Course.course_code, Course.course_name, Pre2019.pre2019score, Pre2019.pre2019labscore,
			Pre2019.pre2019coursetype)
		return render_template('havelearned.html',courseresult=courseresult,dept=dept)

@app.route('/<character>/<thisid>/modify/',methods=['GET','POST'])
def modify(character,thisid):
	# try:
	dept = User2.query.filter_by(userid=thisid).with_entities(User2.userdept).first()[0]
	course = Pre2019.query.filter_by(pre2019dpt=dept).join(Course, (
				Course.course_code == Pre2019.pre2019coursecode)).with_entities(
		Pre2019.pre2019coursecode, Course.course_name, Pre2019.pre2019score, Pre2019.pre2019labscore,
		Pre2019.pre2019coursetype, Pre2019.pre2019courseneed,
		Pre2019.pre2019bigdpt, Pre2019.pre2019season
	).order_by(Pre2019.pre2019coursetype)
	labcourse = Pre2019.query.filter(Pre2019.pre2019dpt==dept,Pre2019.pre2019labscore!=-1).join(Course, (
				Course.course_code == Pre2019.pre2019coursecode)).with_entities(
		Pre2019.pre2019coursecode, Course.course_name, Pre2019.pre2019score, Pre2019.pre2019labscore,
		Pre2019.pre2019coursetype, Pre2019.pre2019courseneed,
		Pre2019.pre2019bigdpt, Pre2019.pre2019season
	).order_by(Pre2019.pre2019coursetype)
	deptname=Dptdet.query.with_entities(Dptdet.dptdet_name).first()[0]

	if request.method=='GET':
		result=Yearsdeptsch.query.filter_by(years=2019,dept=dept).with_entities(Yearsdeptsch.index,Yearsdeptsch.years,Yearsdeptsch.dept,Yearsdeptsch.part,Yearsdeptsch.content)
		chapterlist=[]
		for i in result:
			if i[4] is None:chapterlist.append('')
			else:chapterlist.append(i[4])
		return render_template('modify.html',character=character,thisid=thisid,course=course,labcourse=labcourse,deptname=deptname,chapterlist=chapterlist)
	else:return "successpost"

@app.route('/checker/<thisid>/addingcourse/',methods=['GET','POST'])
def addingcourse(thisid):
	try:
		thischecker=checkeruser[str(thisid)]
	except:return "Something Error!"
	if request.method=='GET':
		return render_template('addingcourse.html',thisid=thisid)
	else:
		coursename=request.form.get("course_name")
		coursecode=request.form.get("course_code")
		if coursename=='' or coursecode=='':
			flash("输入不能为空","danger")
			return render_template('addingcourse.html', thisid=thisid)
		try:
			db.session.add(Course(course_name=coursename,course_code=coursecode))
			db.session.commit()
			flash("添加成功!", "success")
			thischecker.notifystr('新课程加入，名字是'+coursename+'，课程代号是'+coursecode)
		except:
			db.session.rollback()
			flash("添加失败!","danger")
		return render_template('addingcourse.html', thisid=thisid)
@app.route('/dept/<thisid>/addingpre/help/<twhich>/')
def helpofaddingpre(thisid,twhich):
	if twhich=='t0':flash('有疑问请联系11711715@mail.sustech.edu.cn','info' )
	elif twhich=='t1':flash('请输入课程代号,如CS309','info' )
	elif twhich == 't2':
		flash('请输入学分，这是一个小数', 'info')
	elif twhich == 't3':
		flash('请输入实验学分，这是一个小数，若非实验课则输入-1', 'info')
	elif twhich == 't4':
		flash('输入课程类型时，请输入专业选修课，专业基础课，专业必修课，专业实践课，可以用ABC来代表前三者的特殊类型', 'info')
	elif twhich == 't5':
		flash('输入先修要求时，请使用课程代号,与用&,或用|表示，若无先修则输入None', 'info')
	elif twhich == 't6':
		flash('输入开课的系，如物理', 'info')
	elif twhich == 't8':
		flash('输入开课季节，如 春夏', 'info')
	st2r='/dept/'+str(thisid)+'/addingpre/'
	return redirect(st2r)

@app.route('/dept/<thisid>/addingpre/delete/<deptid>/<code>')
def delete(thisid,deptid,code):
	try:
		fetchone=Pre2019.query.filter_by(pre2019dpt=deptid,pre2019coursecode=code).first()
		db.session.delete(fetchone)
		db.session.submit()
		flash("删除成功!","success")
	except:
		db.session.rollback()
		flash("删除失败!","danger")
	rtz="/dept/"+str(thisid)+"/addingpre/"
	return redirect(rtz)
@app.route('/dept/<thisid>/addingpre/',methods=['GET','POST'])
def addingpre(thisid):
	dept=User2.query.filter_by(userid=thisid).with_entities(User2.userdept).first()[0]
	course=Pre2019.query.filter_by(pre2019dpt=dept).join(Course,(Course.course_code==Pre2019.pre2019coursecode)).with_entities(
		Pre2019.pre2019coursecode,Course.course_name,Pre2019.pre2019score,Pre2019.pre2019labscore,Pre2019.pre2019coursetype,Pre2019.pre2019courseneed,
		Pre2019.pre2019bigdpt,Pre2019.pre2019season
	).order_by(Pre2019.pre2019coursetype,Pre2019.pre2019coursecode)
	deptname = Dptdet.query.filter_by(dptdet_index=dept).with_entities(Dptdet.dptdet_name).first()[0]
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
		if t8!="春" and t8!="夏" and t8!="秋" and t8!="春夏" and t8!="夏秋" and t8!="春秋" and t8!="春夏秋":
			flash("输入的季节应该是春 夏 秋 春夏 夏秋 春秋 春夏秋",'danger')
			return render_template('addingpre.html', deptname=deptname,dept=dept,thisid=thisid,course=course)
		if t4!="专业基础课" and t4!="专业必修课" and t4!="专业实践课" and t4!="专业选修课" and t4!="专业基础课A" and t4!="专业基础课B"\
			and t4 != "专业基础课C" and t4!="专业必修课A" and t4!="专业必修课B" and t4!="专业必修课C" and t4!="专业选修课A" and t4!="专业选修课B" and t4!="专业选修课C":
			flash("输入的课程类型不规范","danger")
			return render_template('addingpre.html', deptname=deptname,dept=dept,thisid=thisid,course=course)
		try:
			db.session.add(Pre2019(pre2019coursecode=t1,pre2019score=t2,pre2019labscore=t3,pre2019coursetype=t4,pre2019courseneed=t5,pre2019bigdpt=t6,pre2019dpt=dept,pre2019season=t8))
			db.session.commit()
			flash("添加成功!", "success")
		except:
			db.session.rollback()
			flash("添加失败!","danger")
		return render_template("addingpre.html",deptname=deptname,dept=dept,thisid=thisid,course=course)
@app.route('/dept/<thisid>/addingpre/excelread/',methods=['GET','POST'])
def excelread(thisid):
	dept=User2.query.filter_by(userid=thisid).with_entities(User2.userdept).first()[0]
	deptz = Dptdet.query.filter_by(dptdet_index=dept).with_entities(Dptdet.dptdet_name,Dptdet.dptdet_index).first()
	deptid=deptz[1]

	if request.method=='GET':
		return render_template('fileread.html',thisid=thisid)
	elif request.method=='POST':
		file=request.files.get('uploads')
		d=file.filename.split('.')[-1]
		if d!='xls':
			flash('上传失败','danger')
			return redirect('/dept/' + str(thisid) + '/addingpre/')
		f=file.read()
		data = xlrd.open_workbook(file_contents=f)
		table = data.sheets()[0]
		nrows = table.nrows  # 获取该sheet中的有效行数
		ncols = table.ncols  # 获取该sheet中的有效列数
		try:
			for i in range(nrows):
				t1=table.cell_value(i,0)
				t2=table.cell_value(i,1)
				t3=table.cell_value(i,2)
				t4=table.cell_value(i,3)
				t5=table.cell_value(i,4)
				t6=table.cell_value(i,5)
				t8=table.cell_value(i,6)
				print(t4)
				if t1 == "" or t2 == "" or t3 == "" or t4 == "" or t5 == "" or t6 == "" or t8 == "":
					flash("输入不能为空", "danger")
					db.session.rollback()
					return redirect('/dept/' + str(thisid) + '/addingpre/')
				if t8 != "春" and t8 != "夏" and t8 != "秋" and t8 != "春夏" and t8 != "夏秋" and t8 != "春秋" and t8 != "春夏秋":
					flash("输入的季节应该是春 夏 秋 春夏 夏秋 春秋 春夏秋", 'danger')
					db.session.rollback()
					return redirect('/dept/' + str(thisid) + '/addingpre/')
				if t4 != "专业基础课" and t4 != "专业必修课" and t4 != "专业实践课" and t4 != "专业选修课" and t4 != "专业基础课A" and t4 != "专业基础课B" \
						and t4 != "专业基础课C" and t4 != "专业必修课A" and t4 != "专业必修课B" and t4 != "专业必修课C" and t4 != "专业选修课A" and t4 != "专业选修课B" and t4 != "专业选修课C":
					flash("输入的课程类型不规范", "danger")
					db.session.rollback()
					return redirect('/dept/' + str(thisid) + '/addingpre/')
				db.session.add(Pre2019(pre2019coursecode=t1,pre2019score=t2,pre2019labscore=t3,pre2019coursetype=t4,pre2019courseneed=t5,pre2019bigdpt=t6,pre2019dpt=deptid,pre2019season=t8))
			db.session.commit()
		except:
			flash('上传失败', 'danger')
			db.session.rollback()
			return redirect('/dept/' + str(thisid) + '/addingpre/')
		flash('上传成功','success')
		return redirect('/dept/'+str(thisid)+'/addingpre/')
@app.route('/dept/<thisid>/submitcontent/',methods=['GET','POST'])
def submitcontent(thisid):
	#try:
	years = 2019
	dept=User2.query.filter_by(userid=thisid).with_entities(User2.userdept).first()[0]
	deptname=Dptdet.query.filter_by(dptdet_index=dept).with_entities(Dptdet.dptdet_name).first()[0]
	rz=Yearsdeptsch.query.filter_by(years=str(years),dept=dept).with_entities(Yearsdeptsch.content)
	chapterlist = []
	for i in rz:
		if i[0] is None:
			chapterlist.append('')
		else:
			chapterlist.append(i[0])
	if request.method=='GET':
		if request.args.get('t1') is not None:
			list = []
			list.append([])
			for i in range(1, 11):
				str1 = 't' + str(i)
				d=request.args.get(str1)
				if d is None :d=''
				list.append(d)
			try:
				for i in range(1, 11):
					rez=Yearsdeptsch.query.filter_by(years=str(years),dept=str(dept),part=str(i)).first()
					rez.content=list[i]
					db.session.commit()
				flash("上传成功", 'success')
			except:
				db.session.rollback()
				flash('上传失败', 'danger')
		rz = Yearsdeptsch.query.filter_by(years=str(years), dept=dept).with_entities(Yearsdeptsch.content)
		chapterlist = []
		for i in rz:
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
#############################

@app.route('/schema/input/<dep_code>',methods=['GET','POST'])
def schema_input(dep_code):

	new_schema = mySchema()
	major_id,major_name,id_set,name_set = mySchema.getJsonSchema(mydb,dep_code)
	print(major_id,major_name,id_set,name_set)
	return render_template('schema_input.html',major_id=major_id,major_name=major_name,id_set=id_set,name_set=name_set,dep_code=dep_code)
@app.route('/queryCourse/',methods=['GET','POST'])
def queryCourse():
	new_course =myCourse()
	if new_course.setById(mydb, request.values["code"]):
		print(new_course.getDic())
		return jsonify({"success": 200, "course": new_course.getDic()})
	else:
		return jsonify({"error": 1001, "msg": "查询失败"})
@app.route('/saveSchema/',methods=['GET','POST'])
def saveSchema():
	new_schema = mySchema()
	new_schema.setBySchemaInfo(json.loads(request.values["schema_info"]))
	new_schema.setByCourse(json.loads(request.values["course"]))

	if(mySchema.save(mydb,new_schema)):
		print("保存成功")
		return jsonify({"success":200})
	else:
		print("保存失败")
		return jsonify({"error": 1001,"msg":"保存失败"})
@app.route('/delSchema/',methods=['GET','POST'])
def delSchema():
	schema_id = request.values["schema_id"]
	print("schema=",schema_id)
	if(mySchema.delete(mydb,schema_id)):
		return jsonify({"success":200})
	else:
		return jsonify({"error": 1001,"msg":"保存失败"})
@app.route('/addCourseSchema/',methods=['GET','POST'])
def addCourseSchema():
	new_schema = mySchema()
	new_schema.major_id = request.values["major_id"]
	new_schema.name = request.values["name"]
	print("id=",new_schema.major_id,'name=',new_schema.name)
	new_id=mySchema.add(mydb,new_schema)
	if(new_id):
		return jsonify({"success":200,"id":new_id})
	else:
		return jsonify({"error": 1001,"msg":"新建失败"})
@app.route('/dept/<thisid>/addingpre/mailbox/',methods=['GET','POST'])
def mailbox(thisid):
	if request.method=='GET':
		mailbox=deptuser[str(thisid)].mailbox
		return render_template('mailbox.html',mailbox=mailbox)

@app.route('/querySchema/',methods=['GET','POST'])
def querySchema():
	query_id = request.values["id"]
	new_schema = mySchema()
	new_schema.setSchemaById(mydb,query_id)
	print('intro3=',new_schema.getSchemaInfo()['intro3'])
	print('intro6=', new_schema.getSchemaInfo()['intro6'])
	if(new_schema):
		return jsonify({"success":200,"schema_info":new_schema.getSchemaInfo(),"course":new_schema.getCourse(db)})
	else:
		return jsonify({"error": 1001, "msg": "查询失败"})
@app.route('/downloadSchema/',methods=['GET','POST'])
def downloadSchema():
	import os
	flag = True
	try:
		app = Flask(__name__)
		dirpath = app.root_path
		response = make_response(send_from_directory(dirpath, "schema.pdf", as_attachment=True))
		response.headers["Cache-Control"] = "no-store"
		response.headers["max-age"] = 1
	except Exception as e:
		flag = False
	if flag:
		print("response=",response)
		return response
	else:
		return jsonify({"code": "异常", "message": "{}".format(e)})

@app.route('/generateSchema/', methods=['GET', 'POST'])
def generateSchema():

	html_str = request.values["html_str"]
	print(html_str)
	confg = pdfkit.configuration(wkhtmltopdf='C:/Users/HollowKnight/Desktop/midproj/wkhtmltox/bin/wkhtmltopdf.exe')
	# 这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径
	# pdfkit.from_url(url, 'jmeter_下载文件.pdf', configuration=confg)
	# from_url这个函数是从url里面获取内容
	# 这有3个参数，第一个是url，第二个是文件名，第三个就是khtmltopdf的路径
	# pdfkit.from_string('<p>here</p><br><p>there</p>', 'jmeter_下载文件.pdf', configuration=confg)
	pdfkit.from_string(html_str, 'schema.pdf', configuration=confg)

	flag=True
	if(flag):
		return jsonify({"success":200})
	else:
		return jsonify({"error": 1001, "msg": "查询失败"})