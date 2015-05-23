#-*-coding:utf-8-*-
import MySQLdb
from config import *


class User:

    def __init__(self, name='', email='', user_id=2):
        self.username = name
        self.email = email
        self.user_id = user_id

    def get_data_by_id(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where user_id='" + self.user_id + "';")
        data = cursor.fetchall()
        conn.close()
        if(data != ()):
            return data[0]
        return {'user_id':0, 'username':'', 'email':''}

    def get_data_by_email(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where email='" + self.email + "';")
        data = cursor.fetchall()
        conn.close()
        if(data != ()):
            return data[0]
        return {'user_id':0, 'username':'', 'email':''}

    def get_data_by_name(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from user where username='" + self.username + "';")
        data = cursor.fetchall()
        conn.close()
        if(data != ()):
            return data[0]
        return {'user_id':0, 'username':'', 'email':''}

    def create_group(self, groupname, topic, confirmMessage):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where name='" + groupname + "';")
        exist=cursor.fetchall()
        if(exist):
            print 'failed to create group :', groupname
            return False
        cursor.execute("insert into groups(name,topic,confirmMessage,leader_id) values(%s,%s,%s,%s);",\
            (groupname, topic, confirmMessage, self.username))
        conn.commit()

        cursor.execute("select group_id from groups where name='"+groupname+"';")
        group_id=cursor.fetchone()['group_id']

        cursor.execute("insert into groupMemberAssosiation(group_id,member_id) values(%s,%s);",(group_id,self.user_id))
        conn.commit()
        conn.close()
        print 'created group successfully:', groupname
        return True

    def delete_group(self,group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在且用户为leader
        cursor.execute("select name from groups where group_id='"+group_id+"' and leader_id='"+self.username+"';")
        right=cursor.fetchall()
        if(right):
            cursor.execute("delete from groups where group_id='"+group_id+"';")
            conn.commit()
            cursor.execute("delete from groupMemberAssosiation where group_id='"+group_id+"';")
            conn.commit()
            conn.close()
            print 'deleted group successfully :', group_id
            return True
        conn.close()
        print 'failed to delete group :', group_id
        return False

    def get_groups(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select group_id from groupMemberAssosiation where member_id='"+str(self.user_id)+"';")
        # print "user_id is", self.user_id
        attendedGroups=cursor.fetchall()
        cursor.execute("select group_id from groups where leader_id='"+str(self.user_id)+"';")
        ownGroups=cursor.fetchall()
        conn.close()
        attendedGroupsName = []
        ownGroupsName = []
        for i in attendedGroups:
            attendedGroupsName += [i['group_id']]
        for i in ownGroups:
            ownGroupsName += [i['group_id']]
        # print ownGroups
        return attendedGroupsName, ownGroupsName
    #注意！！这里的返回值是所有的小组id组成的list，不是字典的list！！！

    def join_group(self, group_id):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select name from groups where group_id='"+group_id+"';")
        exist = cursor.fetchall()
        if(exist):
            cursor.execute("insert into groupMemberAssosiation(group_id,member_id) values(%s,%s) ;", (group_id, self.user_id) )
            conn.commit()
            conn.close()
            print 'joined group successfully :', group_id
            return True
        conn.close()
        print 'failed to join group :', group_id
        return False

    def quit_group(self,group_id):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groupMemberAssosiation where member_id='"+self.user_id+"' and group_id='"+group_id+"';")
        exist = cursor.fetchall()
        if(exist):
            cursor.execute("delete from groupMemberAssosiation where member_id='"+self.user_id+"' and group_id='"+group_id+"';")
            conn.commit()
            #whether he's leader
            cursor.execute("select name from groups where group_id='"+group_id+"' and leader_id='"+self.user_id+"';")
            isLeader=cursor.fetchall()  
            if(isLeader):
                print "the user trying to quit is LEADER!"
                cursor.execute("delete from groups where group_id='"+group_id+"';")
                conn.commit()

            conn.close()
            print 'quit group successfully :',group_id
            return True
        print 'failed to quit group :',group_id
        conn.close()
        return False

    def search_group(self, group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where group_id='"+group_id+"';")
        exist=cursor.fetchall()
        if(exist):
            Group1=Group(group_id)
            return Group1
        return None

    def check_u(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row['username'] == self.username:
                return 0
        return 1

    def check_e(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row['email'] == self.email:
                return 0
        return 1

    def login(self, pw):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row['email'] == self.email:
                if row['password'] == pw:
                    return 1    #匹配成功
                else:
                    return 0    #密码错误
        return -1               #邮箱不存在

    def register(self, password):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = 'insert into user(username, password, email) values("%s","%s","%s")' % (self.username, password, self.email)
        cursor.execute(sql)
        conn.commit()
        sql = 'select * from user where email="%s"' % self.email
        cursor.execute(sql)
        result = cursor.fetchall()[0]
        return result

class Group:

    def __init__(self, group_id):
        ##名字与数据库中相同
        self.group_id = str(group_id)
        data = self.get_data()
        self.name = data['name']
        self.topic = data['topic']
        self.confirmMessage = data['confirmMessage']
        self.leader_id = data['leader_id']
        #这里leader的标识也变成id了，注意！！！

    def get_members(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select member_id from groupMemberAssosiation where group_id=" + "'" + self.group_id + "';")
        members=cursor.fetchall()
        conn.close()
        return members
        #返回值是member的id！！！

    def get_discussions(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")

        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from discussion where group_id = %s ;" % self.group_id
        cursor.execute(sql)
        discussions=cursor.fetchall()
        print "discussions: ",discussions
        for discuss in discussions:
            discuss_item = Discussion(discuss['discuss_id'])
            discuss['reply'] = discuss_item.get_reply()
        conn.close()
        return discussions

    def create_discussion(self, user, title, content):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "insert into discussion(user_id, group_id, title, content) values(%d,%s,'%s','%s');"\
              % (user, self.group_id, title, content)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True


    ## renew to be done!
    def get_data(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from groups where group_id="+self.group_id+";"
        cursor.execute(sql)
        data = cursor.fetchall()

        sql = "select * from discussion where group_id="+self.group_id+";"
        cursor.execute(sql)
        discuss_list = cursor.fetchall()
        # print discuss_list
        data[0]['discuss_list'] = discuss_list
        conn.close()
        return data[0]  

class Discussion:
    def __init__(self,discuss_id):
        self.discuss_id = int(discuss_id)
        data = self.get_data()
        self.group_id = data['group_id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.content = data['content']

    def get_data(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from discussion where discuss_id="+str(self.discuss_id)+";"
        cursor.execute(sql)
        item = cursor.fetchone()
        conn.close()
        return item

    def delete_discussion(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "delete from discussion where discuss_id = %s;" % self.discuss_id
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def add_reply(self,user_id,content):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "insert into reply_discuss(discuss_id, user_id, content) values(%d,%d,'%s');"\
              % (self.discuss_id, user_id, content)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def get_reply(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select reply_id,user_id,content from reply_discuss where discuss_id = %d;" % self.discuss_id
        cursor.execute(sql)
        reply = cursor.fetchall()
        conn.close()
        return reply

