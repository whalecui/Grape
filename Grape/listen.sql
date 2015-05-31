CREATE TABLE `votes` (`vote_id` bigint(20) NOT NULL AUTO_INCREMENT,`group_id` int(11) DEFAULT NULL,`vote_content` text,`voting` tinyint(1) DEFAULT NULL,`endtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (`vote_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=gbk;

CREATE TABLE `vote_detail` (`option_id` bigint(20) NOT NULL AUTO_INCREMENT,`vote_id` bigint(20) DEFAULT NULL,`option_order` int(11) DEFAULT NULL,`vote_option` text,`votes` int(11) DEFAULT NULL,PRIMARY KEY (`option_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=gbk;

CREATE TABLE `vote_user_map` (`map_id` bigint(20) NOT NULL AUTO_INCREMENT,`vote_id` bigint(20) DEFAULT NULL,`user_id` int(11) DEFAULT NULL,`votefor` int(11) DEFAULT NULL,PRIMARY KEY (`map_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=gbk;