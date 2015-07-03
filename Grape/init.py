import MySQLdb
import re
from function import *
from config import *

import datetime, time

def initdb():

	start = time.time()

	conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
	cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	
	## set utf8 encoder.
	conn.set_character_set('utf8')
	cursor.execute("SET NAMES utf8;")
	cursor.execute("SET CHARACTER SET utf8;")
	cursor.execute("SET CHARACTER SET utf8;")
	cursor.execute("SET character_set_client=utf8;")
	cursor.execute("SET character_set_database=utf8;")
	cursor.execute("SET character_set_results=utf8;")
	cursor.execute("SET character_set_server=utf8;")

	filename = "morning.sql"
	exec_sql_file(cursor,filename)

	sql = "set session sql_mode = 'NO_AUTO_VALUE_ON_ZERO';"
	cursor.execute(sql)
	sql = "insert into user(user_id, username, password, email,role) \
		   values(0, 'admin','admin','admin@sjtu.edu.cn',1);"
	cursor.execute(sql)
	conn.commit()
	conn.close()

	userList = range(5130309732, 5130309800)
	userList.append(5130309034)
	userList.append(5130309051)

	for i in userList:
		name = "%d" % (i)
		email = "%d@sjtu.edu.cn" % (i)
		password = "%d" % i
		user = User(name = name, email = email)
		status = user.register(password)


		user = User(user_id = 0)
		name = "SE Demo"
		topic = "Discussion on our demo ^_^"
		desc = "This is the discussion group on our Grape system. \
				Be free to join the discussion!"
		confirm = "We are grapers"
		status = user.create_group(name, topic, desc, confirm)
		if(status=='success'):
			print "group insert successfully!"


	for i in range(1,71):
		confirm = "We are grapers"
		user = User(user_id = i)
		status = user.join_group(group_id = 1, confirm = confirm)


	
def exec_sql_file(cursor, sql_file):

	statement = ""

	for line in open(sql_file):
	    if re.match(r'--', line):  # ignore sql comment lines
	        continue
	    if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
	        statement = statement + line
	    else:  # when you get a line ending in ';' then exec statement and reset for next statement
			statement = statement + line
			#print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
			cursor.execute(statement)
			statement = ""


