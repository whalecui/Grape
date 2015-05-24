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


@app.route('/', methods=['GET', 'POST'])
def index():
    islogin = session.get('islogin')
    user_id = session.get('user_id')
    message1 = session.get('message1')
    message2 = session.get('message2')
    attendedGroupsList = []
    ownGroupsList = []

    html = 'index.html'
    members = None
    leader = None

    if islogin == '1':
        html = 'index-log.html'
        #get groups
        print user_id
        user = User(user_id=user_id)
        username = user.username
        attendedGroups, ownGroups = user.get_groups()
        for i in ownGroups:
            ownGroupsList += [Group(i).get_data()]
        for i in attendedGroups:
            if i not in ownGroups:
                attendedGroupsList += [Group(i).get_data()]

        User1=User(user_id=user_id)

        if request.method == 'GET':
            #Find group by group_id
            group_id=request.args.get('group_id')
            print "id from front=", group_id
            if group_id:
                Group1=User1.search_group(group_id)
                if Group1:
                    members=Group1.get_members()
                    leader=Group1.leadername
                    print leader, members, 233

        if request.method == 'POST':
            #create new group
            
            name=request.form.get('name')
            topic=request.form.get('topic')
            confirmMessage=request.form.get('confirmMessage')
            if name and topic and confirmMessage:
                # print name,topic,confirmMessage,1235543
                success=User1.create_group(name, topic, confirmMessage)

            #del group
            delname=request.form.get('delname')
            if delname:
                User1.delete_group(delname)
            #quit group
            quitname=request.form.get('quitname')
            if quitname:
                User1.quit_group(quitname)
    else:
        username = u'请先登录'

    return render_template(html, user_id=user_id, username=username, islogin=islogin,\
                            message1=message1, message2=message2,\
                            attend=attendedGroupsList, own=ownGroupsList, \
                            members=members, leader=leader)

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
            user = User(name=username, email=email)
            if user.check_e() == 0 or user.check_u() == 0:
                session['message1'] = "User already existed!"
                return response
            result = user.register(password)
            #session['username'] = result['username']
            session['islogin'] = '1'
            session['user_id'] = result['user_id']
            #session['email'] = result['email']
            return response
        else:
            session['message1'] = "Password not the same!"
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
        user = User(email=email)
        state = user.login(password)
        if state == 1:
            data = user.get_data_by_email()
            session['user_id'] = data['user_id']
            session['islogin'] = '1'
            #session['email'] = email
            return response
        if state == 0:
            session['message2'] = "Wrong password!"
            return response
        if state == -1:
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
    return jsonify(valid=user.check_u())

@app.route('/_check_email')
def check_email():
    email = request.args.get('email', 0, type=str)
    user = User(email=email)
    return jsonify(valid=user.check_e())

@app.route('/_delete')
def delete():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=int))
    user = User(user_id=user_id)
    return jsonify(success=user.delete_group(group_id))

# @app.route('/group/',methods=['GET', 'POST'])  # maybe no methods here? 
# def groupOverview():
#     is_login = session.get('islogin')
#     if(is_login == 0):                       #please login first!
#         return make_response(redirect('/'))

#     name = session.get('username')
#     user = User(name=name)

#     attendedGroups, ownGroups = user.get_groups()

#     attendedGroupsList = []
#     ownGroupsList = []

#     for i in attendedGroups:
#         attendedGroupsList += [Group(i).get_data()]
#     for i in ownGroups:
#         ownGroupsList += [Group(i).get_data()]

#     overviewList = None     # A overview on group activities.

#     return render_template('group.html', overview=1, username=name,\
#                             ownGroups=ownGroupsList, attendedGroups=attendedGroupsList)


@app.route('/group/', methods=['GET', 'POST'])
def myGroups():
    try:
        user_id = session.get('user_id')
        User1 = User(user_id=user_id)
        name=User1.username
        attendedGroups, ownGroups = User1.get_groups()
        attendedGroupsList = []
        ownGroupsList = []
        print 'att=', attendedGroups
        print 'own=', ownGroups
    ###把group对象存到了两个list中
        for i in attendedGroups:
            attendedGroupsList += [Group(i).get_data()]
        for i in ownGroups:
            ownGroupsList += [Group(i).get_data()]
        print ownGroupsList
    except Exception, e:
        name = '!none!'
        ownGroups = ['none']
        attendedGroups = ['none']
        print 1234, e
    return render_template('group.html', username=name, ownGroups=ownGroupsList, attendedGroups=attendedGroupsList)

@app.route('/group/gp<int:group_id>')
def groupDetail(group_id):
    # is_login = session.get('islogin')
    # if(is_login == 0):                       #please login first!
    #     return make_response(redirect('/'))
    # name = session.get('username')
    # user = User(name)
    # if(user.check_u() == 0):                #username not exist?
    #     session.clear()
    #     return make_response(redirect('/'))
    # user_data = user.get_data_by_name()
    #code above checks user data
    #to be continued
    return render_template('group_id.html', group_id=group_id)

@app.route('/discussion', methods=['GET', 'POST'])
def discussion_operation():
	### Verify it's already login first!!
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    attendedGroups, ownGroups = user.get_groups()
    attendedGroupsList = []
    for i in attendedGroups:
        attendedGroupsList += [Group(i).get_data()]
    discussionList = {}
    for group_id in attendedGroups:
        group = Group(group_id)
        discussionList[group_id] = group.get_discussions()
    return render_template('discussion.html', attendedGroups=attendedGroupsList, discussionList = discussionList)

@app.route('/_create_discussion', methods=['POST'])
def create_discussion():
    group_id = request.form.get('group_id')
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    user_id = user.user_id

    group = Group(group_id)
    group.create_discussion(user_id, title, content)

    return redirect('/discussion')

@app.route('/_delete_discussion/<discuss_id>')
def delete_discussion(discuss_id):
    # make some protections here!
    discuss = Discussion(discuss_id)
    discuss.delete_discussion()
    return redirect('/discussion')

@app.route('/_reply_discussion/<discuss_id>', methods=['POST'])
def reply_discussion(discuss_id):
    # discuss_id = request.form.get('discuss_id')
    print "from reply_discussion", discuss_id
    reply_content =request.form.get('content')
    user_id = session.get('user_id')
    user = User(user_id=user_id)

    discuss = Discussion(discuss_id)
    discuss.add_reply(user_id,reply_content)
    return redirect('/discussion')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
