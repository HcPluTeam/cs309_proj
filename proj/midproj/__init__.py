from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import xlrd


app = Flask('midproj')
app.config.from_pyfile('config.py')
db=SQLAlchemy(app)
mydb = pymysql.connect(host='47.98.40.83', port=3306, user='root', passwd='sustc@123SUSTC', db='Test',
                       charset='utf8')
app.secret_key = 'hcpnb'

from midproj import view
from midproj.view import initit