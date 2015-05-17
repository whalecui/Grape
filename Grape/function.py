#-*-coding:utf-8-*-
import MySQLdb
from config import *

class Group:

    def __init__(self, group_id):
        ##名字与数据库中相同
        self.group_id=str(group_id)
        data=self.get_data()
        self.name = data['name']
        self.topic=data['topic']
        self.confirmMessage=data['confirmMessage']
        self.leadername=data['leadername']

    def get_members(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select membername from groupMemberAssosiation where group_id="+"'"+self.group_id+"';")
        members=cursor.fetchall()
        conn.close()
        return members

    def create_discussion(self, user, title, content):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("insert into discussion(user, group, title, content) values(1,1,'test','test');")
        conn.commit()
        conn.close()
        return True

    def get_discussions(self, group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],\
                             user=db_config["db_user"],passwd=db_config["db_passwd"],\
                             db=db_config["db_name"],charset="utf8")

        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql = "select * from discussion where group_id = %d ;" % group_id
        cursor.execute(sql)
        discussions=cursor.fetchall()
        conn.close()
        return discussions

    def get_data(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groups where group_id="+self.group_id+";")
        data=cursor.fetchall()
        # print data
        conn.close()

        return data[0]  


class User:

    def __init__(self, name = '', email = ''):
        self.username = name
        self.email = email

    def create_group(self, groupname, topic, confirmMessage):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where name='"+groupname+"';")
        exist=cursor.fetchall()
        if(exist):
            print 'failed to create group :',groupname
            return False
        cursor.execute("insert into groups(name,topic,confirmMessage,leadername) values(%s,%s,%s,%s);",\
            (groupname,topic,confirmMessage,self.username))
        conn.commit()

        cursor.execute("select group_id from groups where name='"+groupname+"';")
        group_id=cursor.fetchone()['group_id']

        cursor.execute("insert into groupMemberAssosiation(group_id,membername) values(%s,%s);",(group_id,self.username))
        conn.commit()
        conn.close()
        print 'created group successfully:',groupname
        return True

    def delete_group(self,group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在且用户为leader
        cursor.execute("select name from groups where group_id='"+group_id+"' and leadername='"+self.username+"';")
        right=cursor.fetchall()
        if(right):
            cursor.execute("delete from groups where group_id='"+group_id+"';")
            conn.commit()
            cursor.execute("delete from groupMemberAssosiation where group_id='"+group_id+"';")
            conn.commit()
            conn.close()
            print 'deleted group successfully :',group_id
            return True
        conn.close()
        print 'failed to delete group :',group_id
        return False

    def get_groups(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select group_id from groupMemberAssosiation where membername='"+self.username+"';")
        attendedGroups=cursor.fetchall()
        cursor.execute("select group_id from groups where leadername='"+self.username+"';")
        ownGroups=cursor.fetchall()
        conn.close()
        attendedGroupsName = []
        ownGroupsName = []
        for i in attendedGroups:
            attendedGroupsName += [i['group_id']]
        for i in ownGroups:
            ownGroupsName += [i['group_id']]
        return attendedGroupsName, ownGroupsName
    #注意！！这里的返回值是所有的小组id组成的list，不是字典的list！！！

    def join_group(self,group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select name from groups where group_id='"+group_id+"';")
        exist=cursor.fetchall()
        if(exist):
            cursor.execute("insert into groupMemberAssosiation(group_id,membername) values(%s,%s);",(groupname,self.username))
            conn.commit()
            conn.close()
            print 'joined group successfully :',group_id
            return True
        conn.close()
        print 'failed to join group :',group_id
        return False

    def quit_group(self,group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select * from groupMemberAssosiation where membername='"+self.username+"' and group_id='"+group_id+"';")
        exist=cursor.fetchall()    
        if(exist):
            cursor.execute("delete from groupMemberAssosiation where membername='"+self.username+"' and group_id='"+group_id+"';")   
            conn.commit()
            #whether he's leader
            cursor.execute("select name from groups where group_id='"+group_id+"' and leadername='"+self.username+"';")            
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

        

    def search_group(self,group_id):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where group_id='"+group_id+"';")
        exist=cursor.fetchall()
        if(exist):
            Group1=Group(group_id)
            return Group1
        return None

    def check_u(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row['username'] == self.username:
                return 0
        return 1

    def check_e(self):
        conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row['email'] == self.email:
                return 0
        return 1


# class discussion:

#     def __init__(self, user_id, group_id, content = ''):
#         self.user_id = user_id
#         self.group_id = group_id
#         self.content = content


