#!/usr/bin/python
#coding:utf8
from flask import Flask, render_template, url_for, request,redirect,make_response,session
import os,MySQLdb

app = Flask(__name__)

# @app.route('/')
# def hello():
#   return "hello world"

app.secret_key='\xbc\x98B\x95\x0f\x1e\xcdr\xf8\xb0\xc1\x1a\xd3H\xdd\x86T\xff\xfdg\x80\x8b\x95\xf7'

conn = MySQLdb.connect(user='root', passwd='1234', host='127.0.0.1', db='test', charset='utf8')
sql = 'create table if not exists user(\
      username varchar(128) primary key, \
      password varchar(128))'
cursor = conn.cursor()
cursor.execute(sql)

@app.route('/')
def index():
  username = request.cookies.get('username')
  if not username:
    username = u'请先登录'
  islogin = session.get('islogin')
  return render_template('index.html', username=username, islogin=islogin)


@app.route('/register', methods=['GET','POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if(password2 == password):
      sql = 'insert into user(username, password) values("%s","%s")' % (username, password)
      cursor.execute(sql)
      conn.commit()
      return render_template('/', username=username, islogin='1')
    else:
      # cursor.execute('select * from user')
      return render_template('register.html')
  else:
    return render_template('register.html')

@app.route('/login/', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute('select * from user')
    if (username, password) in cursor.fetchall():
      response = make_response(redirect('/'))
      response.set_cookie('username', value=username, max_age=300)
      session['islogin'] = '1'
      return response
    else:
      session['islogin'] = '0'
      return redirect('/login/')
  else:
    return render_template('login.html')


if __name__ == '__main__':
  app.run(debug=True,host='127.0.0.1',port=5000)