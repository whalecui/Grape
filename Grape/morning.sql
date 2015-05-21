Drop Database if exists Grape;
Create Database Grape;
use Grape;

Drop Table if exists groups;
Create Table groups(
group_id int not null primary key AUTO_INCREMENT,
name varchar(30) not null ,
topic varchar(20) not null,
-- groupCapacity int not null,
confirmMessage varchar(30) not null,
leader_id int not null
);
insert into groups(name,topic,confirmMessage,leader_id) values('group1','AI','thisiskey','2');
insert into groups(name,topic,confirmMessage,leader_id) values('group2','ML','thisiskey','2');
insert into groups(name,topic,confirmMessage,leader_id) values('group3','IR','thisiskey','2');
select * from groups;

Drop Table if exists groupMemberAssosiation;
Create Table groupMemberAssosiation(
group_id int not null ,
member_id int not null
);

insert into groupMemberAssosiation(group_id,member_id) values('1','2');
insert into groupMemberAssosiation(group_id,member_id) values('2','2');
insert into groupMemberAssosiation(group_id,member_id) values('3','2');
select * from groupMemberAssosiation;

Drop Table if exists user;
Create Table user(
user_id int not null primary key AUTO_INCREMENT,
username varchar(128) not null,
password varchar(128) not null, 
email varchar(128),
role int not null default 0
);
insert into user(username, password, email) values('123','123','123@123.com');
insert into user(username, password, email) values('myn','myn','myn@123.com');


Drop Table if exists question;
Create Table question(
question_id int not null primary key AUTO_INCREMENT,
user_id int not null,
group_id int not null,
title varchar(256) not null,
content varchar(256) not null
);
insert into question(user_id, group_id, title, content) values('1','1','Test','Is this test successful?');
