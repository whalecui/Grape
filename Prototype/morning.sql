Drop Database if exists Grape;
Create Database Grape;
use Grape;

Drop Table if exists groups;
Create Table groups(
name varchar(30) not null ,
leadername varchar(30) not null
);
insert into groups(name,leadername) values('test','myn');


Drop Table if exists groupMemberAssosiation;
Create Table groupMemberAssosiation(
groupname varchar(30) not null ,
membername varchar(30) not null
);

insert into groupMemberAssosiation(groupname,membername) values('test','myn');
insert into groupMemberAssosiation(groupname,membername) values('test','ttt');
select groupname from groupMemberAssosiation where groupname='1';
-- Drop Table if exists user;
-- Create Table user(
-- username varchar(30) not null ,
-- password varchar(30) not null ,
-- role int not null default 0,


-- );