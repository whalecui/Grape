Drop Database if exists Grape;
Create Database Grape;
use Grape;

Drop Table if exists groups;
Create Table groups(
group_id int not null primary key AUTO_INCREMENT,
name varchar(90) not null,
topic varchar(90) not null,
description varchar(90) not null default "this is my group!",
create_time timestamp not null default CURRENT_TIMESTAMP,
-- groupCapacity int not null,
confirmMessage varchar(30) not null,
leader_id int not null
)ENGINE=INNODB DEFAULT CHARSET=utf8;


Drop Table if exists groupMemberAssosiation;
Create Table groupMemberAssosiation(
group_id int not null ,
member_id int not null
);


Drop Table if exists user;
Create Table user(
user_id int not null primary key AUTO_INCREMENT,
username varchar(128) not null,
password varchar(128) not null, 
email varchar(128),
role int not null default 0
)ENGINE=INNODB DEFAULT CHARSET=utf8;

Drop Table if exists discussion;
Create Table discussion(
discuss_id int not null primary key AUTO_INCREMENT,
user_id int not null,
group_id int not null,
create_time timestamp not null default CURRENT_TIMESTAMP,
title varchar(256) not null,
content varchar(1024) not null, -- more reasonable than using TEXT.
read_num int not null default 0,
reply_num int not null default 0,
foreign key (group_id) references groups(group_id) on delete cascade
)ENGINE=INNODB DEFAULT CHARSET=utf8;

Drop Table if exists reply_discuss;
Create Table reply_discuss(
reply_id int not null primary key AUTO_INCREMENT,
discuss_id int not null,
user_id int not null,
reply_time timestamp not null default CURRENT_TIMESTAMP,
content varchar(512) not null,
constraint `DR_LINK` foreign key (discuss_id) references discussion(discuss_id) on delete cascade,
KEY `RD_MAP` (`discuss_id`)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

Drop Table if exists votes;
CREATE TABLE `votes` (
  `vote_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` text,
  `voting` tinyint(1) NOT NULL,
  `type` tinyint(1) NOT NULL,
  `begintime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `endtime` timestamp NOT NULL DEFAULT "00-00-00 00:00:00",
  PRIMARY KEY (`vote_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8;
ALTER TABLE votes ADD INDEX GV_MAP(group_id);
alter table votes add constraint VOTE_LINK foreign key (group_id) references groups(group_id) on delete cascade;

Drop Table if exists vote_contents;
CREATE TABLE `vote_contents` (
  `content_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `vote_id` bigint NOT NULL,
  `options` int(11) DEFAULT NULL,
  `content_order` int(11) DEFAULT NULL,
  `vote_content` text,
  PRIMARY KEY (`content_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8;
ALTER TABLE vote_contents ADD INDEX VC_MAP(vote_id);
ALTER table vote_contents ADD constraint CONTENT_LINK foreign key (vote_id) references votes(vote_id) on delete cascade; 

Drop Table if exists vote_detail;
CREATE TABLE `vote_detail` (
`option_id` bigint(20) NOT NULL AUTO_INCREMENT,
`content_id` bigint(20) DEFAULT NULL,
`option_order` int(11) DEFAULT NULL,
`vote_option` text,
`votes` int(11) DEFAULT NULL,
PRIMARY KEY (`option_id`)
) ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
ALTER TABLE vote_detail ADD INDEX CO_MAP(content_id);
alter table vote_detail add constraint OPTION_LINK foreign key (content_id) references vote_contents(content_id) on delete cascade;

Drop Table if exists vote_user_map;
CREATE TABLE `vote_user_map` (
`vmap_id` bigint(20) NOT NULL AUTO_INCREMENT,
`vote_id` bigint(20) DEFAULT NULL,
`user_id` int(11) DEFAULT NULL,
PRIMARY KEY (`vmap_id`)
) ENGINE=INNODB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
alter table vote_user_map add column vote_time timestamp;
ALTER TABLE vote_user_map ADD INDEX VU_MAP(vote_id);
alter table vote_user_map add constraint VOTE_USER_LINK foreign key (vote_id) references votes(vote_id) on delete cascade;

Drop Table if exists content_user_map;
CREATE TABLE `content_user_map` (
`cmap_id` bigint(20) NOT NULL AUTO_INCREMENT,
`vote_id` bigint(20) DEFAULT NULL,
`content_id` bigint(20) DEFAULT NULL,
`user_id` int(11) DEFAULT NULL,
`votefor` int(11) DEFAULT NULL,
PRIMARY KEY (`cmap_id`)
) ENGINE=INNODB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
ALTER TABLE content_user_map ADD INDEX CU_MAP(vote_id);
alter table content_user_map add constraint CONTENT_USER_LINK foreign key (vote_id) references votes(vote_id) on delete cascade;


Drop table if exists message;
Create table message (
message_id int primary key AUTO_INCREMENT,
type int not null default 0,	  -- 0 = first-time, 1 = delete from group, 
								  -- 2 = a member quits the group
								  -- 3 = delete discuss, 4 = delete reply
generator int not null default 0, -- note that always the system generate the message, 
receiver int not null,			  -- but the actual executor of the action is different.
time timestamp not null default CURRENT_TIMESTAMP,
content varchar(256) not null,
viewed tinyint(1) default 0
);



Drop Table if exists bulletin;
CREATE TABLE bulletin (
bulletin_id int not null primary key AUTO_INCREMENT,
user_id int not null,
group_id int not null,
create_time timestamp not null default CURRENT_TIMESTAMP,
title text not null,
text text not null, -- more reasonable than using TEXT.
read_num int not null default 0,
constraint `BULLETIN_LINK` foreign key (group_id) references groups(group_id) on delete cascade,
KEY `GB_MAP` (`group_id`)
) ENGINE=INNODB;
