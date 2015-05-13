#-*-coding:utf-8-*-
import MySQLdb
from config import *

class Group:

    def __init__(self, name):
        self.groupname = name

    def get_members(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select membername from groupMemberAssosiation where groupname="+"'"+self.groupname+"';")
        members=cursor.fetchall()
        conn.close()
        return members
    def get_leader(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select leadername from groups where name="+"'"+self.groupname+"';")
        leadername=cursor.fetchall()
        conn.close()
        return leadername      

class User:

    def __init__(self, name = '', email = ''):
        self.username = name
        self.email = email

    def create_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where name='"+groupname+"';")
        exist=cursor.fetchall()
        if(exist):
            return False
        cursor.execute("insert into groupMemberAssosiation(groupname,membername) values(%s,%s);",(groupname,self.username))
        conn.commit()
        cursor.execute("insert into groups(name,leadername) values(%s,%s);",(groupname,self.username))
        conn.commit()
        conn.close()
        return True

    def delete_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在且用户为leader
        cursor.execute("select name from groups where name='"+groupname+"' and leadername='"+self.username+"';")
        exist=cursor.fetchall()
        if(exist):
            cursor.execute("delete from groups where name='"+groupname+"';")
            conn.commit()
            cursor.execute("delete from groupMemberAssosiation where groupname='"+groupname+"';")
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def get_groups(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select groupname from groupMemberAssosiation where membername='"+self.username+"';")
        attendedGroups=cursor.fetchall()
        cursor.execute("select name from groups where leadername='"+self.username+"';")
        ownGroups=cursor.fetchall()
        conn.close()
        return attendedGroups,ownGroups

    def join_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select name from groups where name='"+groupname+"' and leadername='"+self.username+"';")
        exist=cursor.fetchall()
        if(exist):
            cursor.execute("insert into groupMemberAssosiation(groupname,membername) values(%s,%s);",(groupname,self.username))
            conn.commit()
        conn.close()

    def search_group(self,groupname):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        #判断是否存在
        cursor.execute("select name from groups where name='"+groupname+"';")
        exist=cursor.fetchall()
        if(exist):
            Group1=Group(groupname)
            return Group1
        return None

    def check_u(self):
        conn = MySQLdb.connect(host=self.db_host,port=self.db_port,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row[1] == self.username:
                return 0
        return 1

    def check_e(self):
        conn = MySQLdb.connect(host=self.db_host,port=self.db_port,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('select * from user')
        for row in cursor.fetchall():
            if row[3] == self.email:
                return 0
        return 1


class Question:

    def __init__(self, user_id, group_id, content = ''):
        self.user_id = user_id
        self.group_id = group_id
        self.content = content

    def get_questions(self):
        conn=MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
        cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute("select membername from groupMemberAssosiation where groupname="+"'"+self.groupname+"';")
        members=cursor.fetchall()
        conn.close()
        return members
