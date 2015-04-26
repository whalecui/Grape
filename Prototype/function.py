#-*-coding:utf-8-*-
import MySQLdb

class Group:
	
	def __init__(self,default_config,name):
		self.db_host=default_config["db_host"]
		self.db_user=default_config["db_user"]
		self.db_passwd=default_config["db_passwd"]
		self.db_port=default_config["db_port"]
		self.db_name=default_config["db_name"]
		self.groupname=name

	def get_members(self):
		conn=MySQLdb.connect(host=self.db_host,port=self.db_port,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8")
		cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cursor.execute("select membername from groupMemberAssosiation where groupname="+"'"+str(self.groupname)+"';")
		members=cursor.fetchall()
		conn.commit()
		conn.close()
		return members

class User:
	
	def __init__(self,default_config,name,role):
		self.db_host=default_config["db_host"]
		self.db_user=default_config["db_user"]
		self.db_passwd=default_config["db_passwd"]
		self.db_port=default_config["db_port"]
		self.db_name=default_config["db_name"]
		self.username=name
		self.role=role

#未判断是否存在
	def create_group(self,groupname):
		conn=MySQLdb.connect(host=self.db_host,port=self.db_port,user=self.db_user,passwd=self.db_passwd,db=self.db_name,charset="utf8")
		cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cursor.execute("insert into groupMemberAssosiation(groupname,membername) values(%s,%s);",(groupname,self.username))
		conn.commit()
		cursor.execute("insert into groups(name,leadername) values(%s,%s);",(groupname,self.username))
		conn.commit()
		conn.close()
		return True