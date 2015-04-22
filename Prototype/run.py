#!/usr/bin/python
#coding:utf8
from flask import Flask, render_template, url_for, request,redirect,make_response,session
import os,MySQLdb

app = Flask(__name__)

# @app.route('/')
# def hello():
#   return "hello world"

app.secret_key='\xbc\x98B\x95\x0f\x1e\xcdr\xf8\xb0\xc1\x1a\xd3H\xdd\x86T\xff\xfdg\x80\x8b\x95\xf7'

# <<<<<<< HEAD
conn = MySQLdb.connect(user='root', passwd='', host='127.0.0.1', db='test', charset='utf8')
cursor = conn.cursor()
sql = 'drop table user'
cursor.execute(sql)
# =======
conn = MySQLdb.connect(user='root', passwd='1234', host='127.0.0.1', db='test', charset='utf8')
# >>>>>>> 47dc9743ae9d2b3763a2f85937fa583dd3d642dc
# sql = 'create table if not exists user(\
#       username varchar(128) primary key, \
#       password varchar(128))'
# cursor.execute(sql)

@app.route('/')
def index():
  username = request.cookies.get('username')
  if not username:
    username = 'undefined'
  islogin = session.get('islogin')
  return render_template('index.html',username=username, islogin=islogin)


@app.route('/register', methods=['GET','POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    cursor.execute('select username from user')
    if(password2 == password and username not in cursor.fetchall()[0]):
      sql = 'insert into user(username, password) values("%s","%s")' % (username, password)
      cursor.execute(sql)
      conn.commit()
      response = make_response(redirect('/login'))
      return response
    else:
      # cursor.execute('select * from user')
      return render_template('register.html')
  else:
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute('select * from user')
    if (username, password) in cursor.fetchall():
      response = make_response(redirect('/'))
      response.set_cookie('username', username, max_age=10)
      session['islogin'] = '1'
      return response
    else:
      session['islogin'] = '0'
      return redirect('/login/')
  else:
    return render_template('login.html')


if __name__ == '__main__':
  app.run(debug=True,host='127.0.0.1',port=5000)