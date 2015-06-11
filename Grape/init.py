import MySQLdb
import re
from function import *
from config import *

import datetime, time

def initdb():

	start = time.time()

	conn = MySQLdb.connect(host=db_config["db_host"],port=db_config["db_port"],user=db_config["db_user"],passwd=db_config["db_passwd"],db=db_config["db_name"],charset="utf8")
	cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
	
	filename = "morning.sql"
	exec_sql_file(cursor,filename)

	sql = "set session sql_mode = 'NO_AUTO_VALUE_ON_ZERO';"
	cursor.execute(sql)
	sql = "insert into user(user_id, username, password, email,role) \
		   values(0, 'admin','admin','admin@123.com',1);"
	cursor.execute(sql)
	conn.commit()
	conn.close()

	for i in range(1,11):
		name = "user%d" % (i)
		email = "user%d@123.com" % (i)
		password = "password"
		user = User(name = name, email = email)
		status = user.register(password)
		if(status):
			print "user%d insert successfully!"% i


	for i in range(1,11):
		user = User(user_id = i)
		name = "group%d" % i
		topic = "topic%d" % i
		desc = "description%d" % i
		confirm = "thisiskey%d" % i
		status = user.create_group(name, topic, desc, confirm)
		if(status):
			print "group%d insert successfully!"% i


	for i in range(1,11):
		confirm = "thisiskey%d" % i
		for j in range(i+1,11):			# jump the creation of the leader.
			user = User(user_id = j)
			status = user.join_group(group_id = i, confirm = confirm)
			if(status):
				print "user%d joins the group%d"% (j, i)

	count_dis = 0;
	for i in range(1,11):
		group = Group(group_id = i)
		for j in range(1,4):			# user1 is the id of 2.
			title = "title%d"% j
			content = "content%d"% j
			status = group.create_discussion(user = j, title = title, content = content)
			if(status):
				print "user%d creates discussion%d"% (j, j)
				count_dis += 1
			discuss = Discussion(count_dis)
			for k in range(i+1, 10):
				user_id = k
				reply_content = "This is reply from user%d to discussion%d of group%d" % (k,j-1,i)
				status = discuss.add_reply(user_id, reply_content)


	
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
	        try:
	            cursor.execute(statement)
	        except (OperationalError, ProgrammingError) as e:
	            print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

	        statement = ""


