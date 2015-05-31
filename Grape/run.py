#!/usr/bin/python
#coding:utf8
from flask import Flask, render_template, url_for, request, redirect, make_response, session, abort
import MySQLdb
from flask import jsonify
from config import *
from function import *
import plotly.plotly as py  #easy_install plotly
from xml.sax.saxutils import escape,quoteattr  # transfer ' to \' to escape error in mysql
from plotly.graph_objs import *
import string

app = Flask(__name__)

py.sign_in('NoListen','ueixigh6gr') # API KEY

app.secret_key = '\xbc\x98B\x95\x0f\x1e\xcdr\xf8\xb0\xc1\x1a\xd3H\xdd\x86T\xff\xfdg\x80\x8b\x95\xf7'

conn = MySQLdb.connect(user='root', passwd='1234', host='127.0.0.1', db='grape', charset='utf8')
cursor = conn.cursor()

open_event_scheduler ="SET GLOBAL event_scheduler = 1;"
cursor.execute(open_event_scheduler)
conn.commit()
#open the event_scheduler to set time expiration event

@app.route('/', methods=['GET', 'POST'])
def index():
    islogin = session.get('islogin')
    user_id = session.get('user_id')
    message1 = session.get('message1')
    attendedGroupsList = []
    ownGroupsList = []
    html = 'index.html'
    members = None
    leader = None

    if islogin == '1':
        html = 'index-log.html'
        #get groups
        User1 = User(user_id=user_id)
        username = User1.username
        role = User1.role
        if(role==1):
            return redirect('/admin')
        attendedGroups, ownGroups = User1.get_groups()
        for i in ownGroups:
            ownGroupsList += [Group(i).get_data()]
        for i in attendedGroups:
            if i not in ownGroups:
                attendedGroupsList += [Group(i).get_data()]

        if request.method == 'GET':
            #Find group by group_id
            group_id=request.args.get('group_id')
            #print "id from front=", group_id
            if group_id:
            #    Group1=User1.search_group(group_id)
            #    if Group1:
            #        members=Group1.get_members()
            #        leader=Group1.leader_id
            #        print leader, members, 233
                return redirect(url_for('groupDetail', group_id=group_id))

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
            return make_response(redirect('/'))
    else:
        username = u'请先登录'

    return render_template(html, user_id=user_id, username=username, islogin=islogin,\
                            message1=message1, \
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

@app.route('/_login/', methods=['GET', 'POST'])
def login():
    session.clear()
    email = str(request.args.get('email', 0, type=str))
    password = str(request.args.get('pw', 0, type=str))
    session['islogin'] = '0'
    if(email == '' or password == ''):
        status = 'Please enter email and password!'
        return jsonify(status=status)
    user = User(email=email)
    state = user.login(password)
    if state == 1:
        data = user.get_data_by_email()
        session['user_id'] = data['user_id']
        session['islogin'] = '1'
        status = 'success'
        return jsonify(status=status)
    if state == 0:
        status = "Wrong password!"
        return jsonify(status=status)
    if state == -1:
        status = "Email not used!"
        return jsonify(status=status)

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

@app.route('/_join_group')
def join_group():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=int))
    confirm = str(request.args.get('confirm', 0, type=str))
    group = Group(group_id=group_id)
    user = User(user_id=user_id)
    status=user.join_group(group_id=group_id, confirm=confirm)
    return jsonify(status=status)

@app.route('/_quit_group')
def quit_group():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=str))
    group = Group(group_id=group_id)
    user = User(user_id=user_id)
    status=user.quit_group(group_id=group_id)
    return jsonify(status=status)

@app.route('/_delete_group')
def deleteGroup():
    user_id = session.get('user_id')
    group_id = str(request.args.get('group_id', 0, type=int))
    user = User(user_id=user_id)
    return jsonify(success=user.delete_group(group_id))

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
    if(user.check_id() == 1):                #user not exist?
        session.clear()
        return make_response(redirect('/'))
    user_data = user.get_data_by_id()
    #code above checks user data
    group = Group(group_id)
    if(group.exist_group()):
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
            return render_template('group-id.html', group_id=group_id,\
                                   group_data=group_data, discussions=discussions,\
                                   username=user_data['username'], role='2')
                                   #leader
        if({'member_id': user_id} in members):
            return render_template('group-id.html', group_id=group_id,\
                                   group_data=group_data, discussions=discussions,\
                                   username=user_data['username'], role='1')
                                   #member
        #to be continued
        return render_template('group-id.html', group_id=group_id,\
                               group_data=group_data,\
                               username=user_data['username'], role='0')
                                   #other
    #return render_template('group-id.html', group_id=group_id,\
    #                       username=user_data['username'], role='-1')
    abort(404)
                           #non-exist


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
    if(is_login == '0'):                       #please login first!
        return make_response(redirect('/'))
    user_id = session.get('user_id')
    user = User(user_id=user_id)
    if(user.check_id() == '1'):                #user not exist?
        session.clear()
        return make_response(redirect('/'))

    if(user.role!=1):
        abort(404)

    admin1=Admin(user_id=user_id)
    groups=admin1.show_all_groups()
    users=admin1.show_all_users()

    # admin1.delete_user(2)
    # admin1.delete_group(2)


    return render_template('admin.html', username=user.username,groups=groups,users=users)

@app.route('/group/gp<int:group_id>/vote', methods=['GET', 'POST'])
def vote(group_id):
    return render_template('vote_index.html',current_path=request.path)

@app.route('/group/gp<int:group_id>/vote/raise-vote',methods=['GET','POST'])
def raise_a_vote(group_id):
    return render_template('raise_a_vote.html',current_path=request.path)

@app.route('/group/gp<int:group_id>/vote/raise-vote/result',methods=['GET','POST'])
def raise_a_vote_result(group_id):
    conn = MySQLdb.connect(user='root', passwd='', host='127.0.0.1', db='grape', charset='utf8')
    cursor = conn.cursor()
    if request.method == "GET":
        vote_content = quoteattr(request.args.get('vote-content'))
        endtime_selection = request.args.get('endtime-selection')
        if (endtime_selection == "2"):
            endtime = request.args.get('datetime')
            endtime = "'%s'" % endtime
        else:
            time_split = request.args.get('timeinterval').split(':')
            endtime = "current_timestamp + interval %s hour + interval %s minute + interval %s second" % (time_split[0],time_split[1],time_split[2])
        sql = """insert into votes (group_id,vote_content,voting,endtime) values ("%s",%s,1,%s)""" % (group_id,vote_content,endtime)
        cursor.execute(sql)
        conn.commit()

        # need to add something here later
        
        cursor.execute("select LAST_INSERT_ID() from votes where group_id='%s'" % (group_id))

        voteid = cursor.fetchall()[0][0]

        sql = """ CREATE EVENT event_%s ON SCHEDULE AT %s  ENABLE DO update votes set voting=0 where vote_id=%d;""" % (voteid,endtime,voteid)
        cursor.execute(sql)
        conn.commit()

        options = string.atoi(request.args.get('vote-options-num'))
        for i in range (1,options+1):
            sql = """insert into vote_detail(vote_id,option_order,vote_option,votes) values (%d,%d,%s,0)""" % (voteid,i,quoteattr(request.args.get('vote-option-content-%s'% str(i))).encode('utf-8'))
            cursor.execute(sql)
        conn.commit()
        return redirect("/group/gp%d/vote" % group_id)

@app.route('/group/gp<int:group_id>/vote/view-votes')
def view_votes(group_id):

    votes_list_voting = []
    votes_list_end = []

    sql = "select * from votes where group_id = %d and voting = 1" % group_id
    cursor.execute(sql)
    votes_data = cursor.fetchall()

    for vote in votes_data:
        vote_pair = (vote[0],vote[2]) # id and the contents of the question
        votes_list_voting.append(vote_pair)

    sql = "select * from votes where group_id = %d and voting = 0" % group_id
    cursor.execute(sql);

    votes_data = cursor.fetchall()
    for vote in votes_data:
        vote_pair = (vote[0],vote[2])
        votes_list_end.append(vote_pair)

    return render_template('view_the_votes.html',votes_list_voting=votes_list_voting,votes_list_end=votes_list_end,current_path=request.path) # add status


@app.route('/group/gp<int:group_id>/vote/view-votes/voting<vote_id>')
def vote_operation(group_id,vote_id): # use groupid to verify the vote
    user_id = session.get('user_id')

    # ensure the vote has not voted before 
    # if the user change the status to submit it
    sql = "select * from vote_user_map where vote_id = '%s' and user_id = '%s'" % (vote_id,user_id)
    cursor.execute(sql)
    voted_status = cursor.fetchall() # it is possible the user has voted before
    is_voted = len(voted_status)
    option_voted = 0
    if is_voted != 0:
        option_voted = voted_status[0][3] # votefor

    sql = "select * from votes where vote_id = '%s'" % vote_id
    cursor.execute(sql)
    vote_content = cursor.fetchall()[0][2]
    sql = "select * from vote_detail where vote_id = '%s'" % vote_id
    cursor.execute(sql)
    vote_options_list = []
    vote_options_data = cursor.fetchall()
    for vote_option in vote_options_data: 
        vote_options_list.append(vote_option[3])

    return render_template('view_the_vote_options.html',vote_options_list=vote_options_list,vote_content=vote_content,vote_id=vote_id,is_voted=is_voted,option_voted=option_voted,current_path=request.path)


@app.route('/group/gp<int:group_id>/vote/view-votes/voting<vote_id>/vote-operation-result',methods=['GET','POST'])
def vote_operation_result(group_id,vote_id):
    if request.method == 'GET':
        user_id = session.get('user_id')
        vote_option = request.args.get('vote-option')
        vote_id = request.args.get('vote-id')

        sql = "select * from vote_user_map where vote_id = '%s' and user_id = '%s'" % (vote_id,user_id)
        cursor.execute(sql)
        voted_status = cursor.fetchall() # it is possible the user has voted before
        is_voted = len(voted_status)
        if is_voted != 0:
            return "you have voted before" 

        sql = "select votes from vote_detail where option_order='%s' and vote_id='%s'" % (vote_option,vote_id)
        cursor.execute(sql)
        votes = cursor.fetchall()[0][0]
        sql = "update vote_detail set votes=%d where option_order='%s' and vote_id='%s'" % (votes+1,vote_option,vote_id)
        cursor.execute(sql)
        conn.commit()

        sql = "insert into vote_user_map(vote_id,user_id,votefor) values('%s','%s','%s')" % (vote_id,user_id,vote_option)
        cursor.execute(sql)
        conn.commit()
    return redirect('/group/gp%d/vote' % group_id)

@app.route('/group/gp<int:group_id>/vote/view-votes/rs<vote_id>',methods=['GET','POST'])
def view_votes_result(group_id,vote_id):
    groupname ="grape"

    sql = "select * from vote_detail where vote_id='%s'" % vote_id
    cursor.execute(sql)
    votes_static = cursor.fetchall()
    vote_options_list = []
    votes_distribution = []


    option = 0;
    for vote_item in votes_static:
        vote_options_list.append('%s.' % (chr(65+option)) + '%s' % vote_item[3])
        votes_distribution.append(vote_item[4])
        option+=1

    data = Data([
        Bar(
            x=vote_options_list,
            y=votes_distribution
        )
    ])
    plot_url = py.plot(data,filename="votes-bar-%s"%vote_id,auto_open=False)+'/.embed?width=800&height=600'
    return render_template('votes_static.html',plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
