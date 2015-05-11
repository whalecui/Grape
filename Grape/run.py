#!/usr/bin/python
#coding:utf8
from flask import Flask, render_template, url_for, request,redirect,make_response,session
import os,MySQLdb
from flask import jsonify
from config import *
from function import *
app = Flask(__name__)


app.secret_key = '\xbc\x98B\x95\x0f\x1e\xcdr\xf8\xb0\xc1\x1a\xd3H\xdd\x86T\xff\xfdg\x80\x8b\x95\xf7'

conn = MySQLdb.connect(user='root', passwd='1234', host='127.0.0.1', db='grape', charset='utf8')
cursor = conn.cursor()

# sql = 'create table if not exists user(\
#         user_id int not null primary key AUTO_INCREMENT, \
#         username varchar(128), \
#         password varchar(128), \
#         email varchar(128))'
# cursor.execute(sql)

@app.route('/', methods=['GET','POST'])
def index():
    islogin = session.get('islogin')
    username = session.get('username')
    message1 = session.get('message1')
    message2 = session.get('message2')
    html = 'index.html'
    if islogin == '1':
        html = 'index-log.html'
    else:
        username = u'请先登录'

    User1=User(username)
    members=None
    leader=None
    if request.method == 'GET':
        groupname=request.args.get('groupname')
        if groupname:
            Group1=User1.search_group(groupname)
            members=Group1.get_members()
            leader=Group1.get_leader()
            print members

    return render_template(html, username=username, islogin=islogin, message1=message1, message2=message2,\
                            members=members,leader=leader)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        session.clear()
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        response = make_response(redirect('/'))
        session['islogin'] = '0'
        if(username == '' or password == '' or email == ''):
            session['message1'] = 'fuck!'
            return response
        if password2 == password:
            sql = 'select * from user where username="%s"' % username
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                session['message1'] = "User already existed!"
                return response
            sql = 'select * from user where email="%s"' % email
            sql = 'insert into user(username, password, email) values("%s","%s","%s")' % (username, password, email)
            cursor.execute(sql)
            conn.commit()
            sql = 'select * from user where email="%s"' % email
            cursor.execute(sql)
            result = cursor.fetchall()[0]
            session['username'] = result[1]
            session['islogin'] = '1'
            session['userid'] = result[0]
            session['email'] = result[3]
            return response
        else:
            # cursor.execute('select * from user')
            session['message1'] = "Password not the same"
            return response
    else:
        return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        email = request.form.get('email')
        password = request.form.get('password')
        response = make_response(redirect('/'))
        session['islogin'] = '0'
        if(email == '' or password == ''):
            session['message2'] = 'fuck!'
            return response
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row[3] == email:
                if row[2] == password:
                    session['username'] = row[1]
                    session['userid'] = row[0]
                    session['islogin'] = '1'
                    session['email'] = email
                    return response
                else:
                    session['message2'] = "Wrong password!"
                    return response
        session['message2'] = "Email not used!"
        return response
    else:
      session['islogin'] = '0'
      return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect('/'))
    return response

@app.route('/_check_users')
def check_users():
    username = request.args.get('username', 0, type=str)
    user = User(name=username)
    return jsonify(result = user.check_u())

@app.route('/_check_email')
def check_email():
    email = request.args.get('email', 0, type=str)
    user = User(email=email)
    return jsonify(user.check_e())

@app.route('/gm/', methods=['GET', 'POST'])
def getMembers():
    name = 'test'
    Group1 = Group(name)
    members = Group1.get_members()
    name = 'myn'
    User1 = User(name)
    mark = User1.create_group('groupCreatedByPy')
    if mark:
        print "created successfully!"
    else:
        print "Already existed!"
    return render_template('gm.html', members=members)


@app.route('/group/', methods=['GET', 'POST'])
def mygroups():
    try:
        name = session.get('username')
        User1=User(name)
        attendedGroups,ownGroups=User1.get_groups()
    except Exception,e:
        name = 'none'
        ownGroups=['none']
        attendedGroups=['none']
        print e

    return render_template('group-func.html',username=name,ownGroups=ownGroups,attendedGroups=attendedGroups)


@app.route('/question', methods=['GET', 'POST'])
def question_operation():
	return render_template('question.html')


if __name__ == '__main__':
  app.run(debug=True, host=HOST, port=PORT)
