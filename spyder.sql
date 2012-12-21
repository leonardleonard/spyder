-- phpMyAdmin SQL Dump
-- version 3.5.3
-- http://www.phpmyadmin.net
--
-- 主机: local.site
-- 生成日期: 2012 年 12 月 21 日 13:53
-- 服务器版本: 5.5.21
-- PHP 版本: 5.3.15

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `spyder`
--

-- --------------------------------------------------------

--
-- 表的结构 `field_template`
--

DROP TABLE IF EXISTS `field_template`;
CREATE TABLE IF NOT EXISTS `field_template` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT 'field name',
  `title` varchar(64) NOT NULL COMMENT 'nickname',
  `type` enum('article','game','kaifu','kaice','gift','company') NOT NULL DEFAULT 'article',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- 转存表中的数据 `field_template`
--

INSERT INTO `field_template` (`id`, `name`, `title`, `type`) VALUES
(1, 'title', '文章标题', 'article'),
(2, 'author', '作者', 'article'),
(3, 'tag', '标签', 'article'),
(4, 'source', '来源', 'article'),
(5, 'content', '正文', 'article'),
(6, 'create_time', '发表时间', 'article');

-- --------------------------------------------------------

--
-- 表的结构 `seeds`
--

DROP TABLE IF EXISTS `seeds`;
CREATE TABLE IF NOT EXISTS `seeds` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `seed_name` varchar(64) NOT NULL,
  `type` enum('article','game','kaifu','kaice','gift','company') NOT NULL DEFAULT 'article',
  `base_url` varchar(255) DEFAULT NULL,
  `charset` char(10) NOT NULL DEFAULT 'utf-8',
  `lang` char(4) NOT NULL,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `listtype` enum('html','feed') NOT NULL,
  `rule` mediumtext NOT NULL,
  `frequency` tinyint(3) unsigned NOT NULL,
  `timeout` smallint(6) NOT NULL DEFAULT '300',
  `tries` tinyint(4) NOT NULL DEFAULT '5',
  `created_time` int(11) NOT NULL,
  `update_time` int(11) NOT NULL,
  `start_time` int(11) NOT NULL,
  `finish_time` int(11) NOT NULL,
  PRIMARY KEY (`sid`),
  UNIQUE KEY `url` (`base_url`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- 转存表中的数据 `seeds`
--

INSERT INTO `seeds` (`sid`, `seed_name`, `type`, `base_url`, `charset`, `lang`, `enabled`, `listtype`, `rule`, `frequency`, `timeout`, `tries`, `created_time`, `update_time`, `start_time`, `finish_time`) VALUES
(2, 'kaifu新闻', 'article', NULL, 'utf-8', 'zhCN', 1, 'html', 'a:10:{s:7:"maxpage";s:1:"5";s:4:"step";s:2:"10";s:9:"urlformat";s:53:"http://www.kaifu.com/article-24--0-0-0-0-0-0-(*).html";s:7:"urltype";s:10:"createLink";s:7:"filters";s:0:"";s:13:"contentparent";s:57:"div[class=''fl newsinfo_topline boder_base newsinfo_left'']";s:9:"startpage";s:1:"0";s:10:"pageparent";s:0:"";s:10:"listparent";s:57:"div[class=''fl newsinfo_topline boder_base newsinfo_left'']";s:11:"entryparent";s:18:"li[class=''b_line'']";}', 255, 30, 5, 0, 1356065567, 0, 0),
(6, '34234', 'article', NULL, 'gb2312', 'zhCN', 0, 'html', 'a:10:{s:7:"maxpage";s:0:"";s:4:"step";s:0:"";s:9:"urlformat";s:5:"34234";s:7:"urltype";s:9:"inputLink";s:7:"filters";s:0:"";s:13:"contentparent";s:3:"234";s:9:"startpage";s:0:"";s:10:"pageparent";s:0:"";s:10:"listparent";s:4:"2342";s:11:"entryparent";s:5:"23423";}', 1, 30, 5, 1356065619, 1356065619, 0, 0);

-- --------------------------------------------------------

--
-- 表的结构 `seed_fields`
--

DROP TABLE IF EXISTS `seed_fields`;
CREATE TABLE IF NOT EXISTS `seed_fields` (
  `seed_id` int(11) NOT NULL,
  `field_id` int(11) NOT NULL,
  `value` varchar(64) DEFAULT NULL,
  `page_type` enum('list','content') NOT NULL COMMENT '采集目标页面的类型：列表或者内容页',
  KEY `seed_id` (`seed_id`,`field_id`),
  KEY `seed_id_2` (`seed_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `seed_fields`
--

INSERT INTO `seed_fields` (`seed_id`, `field_id`, `value`, `page_type`) VALUES
(2, 1, 'h6[class=''lh40'']', 'content'),
(2, 2, 'span[class=author]', 'content'),
(2, 3, 'span[class=tag]', 'list'),
(2, 5, 'div[class=''newsinfo_artical p14 lh24'']', 'content'),
(2, 4, '', 'content'),
(6, 1, '23423', 'content'),
(6, 2, '234234', 'content'),
(6, 3, '234234', 'list'),
(6, 4, '2342', 'content'),
(6, 5, '23423', 'list'),
(6, 6, '', 'content');

-- --------------------------------------------------------

--
-- 表的结构 `seed_logs`
--

DROP TABLE IF EXISTS `seed_logs`;
CREATE TABLE IF NOT EXISTS `seed_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sid` int(11) NOT NULL,
  `start_time` int(11) NOT NULL,
  `finish_time` int(11) NOT NULL,
  `status` tinyint(2) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `seed_tag`
--

DROP TABLE IF EXISTS `seed_tag`;
CREATE TABLE IF NOT EXISTS `seed_tag` (
  `sid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  PRIMARY KEY (`sid`,`tid`),
  UNIQUE KEY `sid` (`sid`,`tid`),
  KEY `tid` (`tid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `tags`
--

DROP TABLE IF EXISTS `tags`;
CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL DEFAULT '-1',
  `name` varchar(255) NOT NULL,
  `type` enum('tag','category') NOT NULL DEFAULT 'tag',
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `passwd` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `permissions` varchar(255) NOT NULL,
  `salt` char(10) NOT NULL,
  `createtime` int(11) NOT NULL,
  `lastlogintime` int(11) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12 ;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`uid`, `username`, `passwd`, `email`, `permissions`, `salt`, `createtime`, `lastlogintime`) VALUES
(10, 'admin', '13dbcde8ab9b640d6d725b57750ab3d6', 'admin@admin.com', 'administrator', 'gWT3', 0, 1356059738),
(11, 'fireyy', '793d2dd8ac95f086666650518c69665d', 'fireyy@admin.com', 'administrator', 'at2Y', 1356060783, 1356060967);

-- --------------------------------------------------------

--
-- 表的结构 `websites`
--

DROP TABLE IF EXISTS `websites`;
CREATE TABLE IF NOT EXISTS `websites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `descript` varchar(255) DEFAULT NULL,
  `url` varchar(255) NOT NULL,
  `sync_type` enum('mysql','api') NOT NULL,
  `sync_profile` text NOT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `websites`
--

INSERT INTO `websites` (`id`, `name`, `descript`, `url`, `sync_type`, `sync_profile`, `status`) VALUES
(1, 'sdfsdf', 'sdfsdf', 'sdf', 'mysql', 'a:7:{s:14:"mysql_password";s:0:"";s:7:"api_url";s:0:"";s:12:"mysql_dbname";s:6:"spyder";s:12:"mysql_prefix";s:0:"";s:12:"mysql_server";s:9:"127.0.0.1";s:14:"mysql_username";s:4:"root";s:9:"staticUrl";s:0:"";}', 0);

-- --------------------------------------------------------

--
-- 表的结构 `website_map`
--

DROP TABLE IF EXISTS `website_map`;
CREATE TABLE IF NOT EXISTS `website_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siteid` int(11) NOT NULL COMMENT '站点ID',
  `table_name` varchar(64) NOT NULL COMMENT '数据库名',
  `seed_id` int(11) NOT NULL COMMENT '种子ID',
  `field_id` int(11) NOT NULL COMMENT 'seed_fields中的ID',
  `site_field` varchar(64) NOT NULL COMMENT '映射目标的field name',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- 转存表中的数据 `website_map`
--

INSERT INTO `website_map` (`id`, `siteid`, `table_name`, `seed_id`, `field_id`, `site_field`) VALUES
(1, 1, 'cms_article', 0, 1, 'title'),
(2, 1, 'cms_article', 0, 2, 'author'),
(3, 1, 'cms_article', 0, 3, 'tag'),
(4, 1, 'cms_article', 0, 4, ''),
(5, 1, 'cms_article', 0, 5, '');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
