#!/usr/bin/python
#coding:utf8
from flask import Flask, render_template, url_for, request, redirect, make_response, session, abort
import MySQLdb
from flask import jsonify
from config import *
from function import *
app = Flask(__name__)


app.secret_key = '\xbc\x98B\x95\x0f\x1e\xcdr\xf8\xb0\xc1\x1a\xd3H\xdd\x86T\xff\xfdg\x80\x8b\x95\xf7'

# conn = MySQLdb.connect(user='root', passwd='1234', host='127.0.0.1', db='grape', charset='utf8')
# cursor = conn.cursor()


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
<<<<<<< HEAD
        print user_id
        user = User(user_id=user_id)
        username = user.username
        attendedGroups, ownGroups = user.get_groups()
=======
        User1 = User(user_id=user_id)
        username = User1.username
        role = User1.role
        if(role==1):
            return redirect('/admin')
        attendedGroups, ownGroups = User1.get_groups()
>>>>>>> 25731d86292efa201df354a2569eace024e30598
        for i in ownGroups:
            ownGroupsList += [Group(i).get_data()]
        for i in attendedGroups:
            if i not in ownGroups:
                attendedGroupsList += [Group(i).get_data()]

        if request.method == 'GET':
            #Find group by group_id
            group_id=request.args.get('group_id')
            print "id from front=", group_id
            if group_id:
                Group1=User1.search_group(group_id)
                if Group1:
                    members=Group1.get_members()
                    leader=Group1.leader_id 
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

@app.route('/_delete_group')
def deleteGroup():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=int))
    user = User(user_id=user_id)
    return jsonify(success=user.delete_group(group_id))

<<<<<<< HEAD
=======
@app.route('/_delete_user')
def delete_user():
    user_id = session.get('user_id')
    user_id_to_be_deleted = str(request.args.get('user_id', 0, type=int))
    print 'del user',user_id_to_be_deleted
    admin = Admin(user_id=user_id)
    return jsonify(success=admin.delete_user(user_id_to_be_deleted))
@app.route('/_delete_group_admin')
def delete_group_admin():
    user_id = session.get('user_id')
    print 233
    group_id = str(request.args.get('group_id', 0, type=int))
    admin = Admin(user_id=user_id)
    return jsonify(success=admin.delete_group(group_id))

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

>>>>>>> 25731d86292efa201df354a2569eace024e30598

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
        ownGroupList = ['none']
        attendedGroupList = ['none']
        print 1234, e
    return render_template('group.html', user_id=user_id,\
                           username=name, ownGroups=ownGroupsList, \
                           attendedGroups=attendedGroupsList)

@app.route('/group/gp<int:group_id>', methods=['GET', 'POST'])
def groupDetail(group_id):
    is_login = session.get('islogin')
    if(is_login == 0):                       #please login first!
        return make_response(redirect('/'))
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    if(user.check_id() == 0):                #user not exist?
        session.clear()
        return make_response(redirect('/'))
    user_data = user.get_data_by_id()
    #code above checks user data
    group = Group(group_id)
    group_data = group.get_data()
    if(group.exist_group()):

        # if(str(user_id) == str(group.leader_id)):
        #     role = '2'
        # elif(str(user_id) in group.get_members()):
        #     role='1'
        group_data = group.get_data()
        discussions = group.get_discussions()
        members = group.get_members()
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            if title and content:
                # print name,topic,confirmMessage,1235543
                group.create_discussion(user=user_id, title=title, content=content)
            return redirect(url_for('groupDetail', group_id=group_id))

        if(str(user_id) == str(group.leader_id)):
            return render_template('group_id.html', group_id=group_id,\
                                   group_data=group_data, discussions=discussions,\
                                   username=user_data['username'], role='2')
                                   #leader
        if({'member_id': user_id} in members):
            return render_template('group_id.html', group_id=group_id,\
                                   group_data=group_data, discussions=discussions,\
                                   username=user_data['username'], role='1')
                                   #member
        #to be continued
        else:
            role='0'
    return render_template('group_id.html', group_id=group_id, role=role,\
                           username=user_data['username'], group_data=group_data)


@app.route('/group/gp<int:group_id>/dis<int:discuss_id>',methods=['GET','POST'])
def show_discuss(group_id,discuss_id):
    is_login = session.get('islogin')
    if(is_login == 0):                       #please login first!
        return make_response(redirect('/'))
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    if(user.check_id() == 0):                #user not exist?
        session.clear()
        return make_response(redirect('/'))
    user_data = user.get_data_by_id()
    group = Group(group_id)
    discuss = Discussion(discuss_id)
    discuss_data = discuss.get_data()
    reply = discuss.get_reply()
    return render_template('discussion.html',username=user_data['username'],\
                            discuss=discuss_data,reply=reply)



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

@app.route('/_create_discussion/<int:group_id>', methods=['POST'])
def create_discussion(group_id):
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    user_id = user.user_id

    group = Group(group_id)
    group.create_discussion(user_id, title, content)

    return redirect('/group/gp'+str(group_id))

@app.route('/_delete_discussion')
def deleteDiscussion():
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    discuss_id = str(request.args.get('discuss_id', 0, type=int))
    return jsonify(success=user.delete_discussion(discuss_id))

    # make some protections here!
    discuss = Discussion(discuss_id)
    discuss.delete_discussion()
    return redirect('/group/gp'+str(group_id))

@app.route('/_reply_discussion/<discuss_id>', methods=['POST'])
def reply_discussion(discuss_id):
    # discuss_id = request.form.get('discuss_id')
    print "from reply_discussion", discuss_id
    reply_content =request.form.get('content')
    user_id = session.get('user_id')
    #seems not used?
    #user = User(user_id=user_id)

    discuss = Discussion(discuss_id)
    discuss.add_reply(user_id,reply_content)
    return redirect('/discussion')

@app.errorhandler(404)
def page_not_found(error):
    user_id = session.get('user_id')
    islogin = session.get('islogin')
    if islogin == '1':
        user = User(user_id=user_id)
        username = user.username
    else:
        username = u'请先登录'
    return render_template('page_not_found.html', user_id=user_id, islogin=islogin, username=username), 404

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    #未判断是否为admin
    is_login = session.get('islogin')
    if(is_login == 0):                       #please login first!
        return make_response(redirect('/'))
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    if(user.check_id() == 1):                #user not exist?
        session.clear()
        return make_response(redirect('/'))

    if(user.role!=1):
        abort(404)

    admin1=Admin(user_id=user_id)
    groups=admin1.show_all_groups()
    users=admin1.show_all_users()

    # admin1.delete_user(2)
    # admin1.delete_group(2)


<<<<<<< HEAD
    return render_template('admin.html', groups=groups,users=users)
=======

    return render_template('admin.html', username=user.username,groups=groups,users=users)
>>>>>>> 25731d86292efa201df354a2569eace024e30598

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
