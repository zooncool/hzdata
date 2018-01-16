# hzdata
python project

CREATE TABLE `building` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `gmt_created` date DEFAULT NULL COMMENT '创建时间',
  `gmt_modified` datetime DEFAULT NULL COMMENT '修改时间',
  `project_code` varchar(16) DEFAULT NULL COMMENT '项目编码',
  `building_code` varchar(16) DEFAULT NULL COMMENT '楼盘编码',
  `property_name` varchar(128) DEFAULT NULL COMMENT '项目名称',
  `building_name` varchar(128) DEFAULT NULL COMMENT '楼盘名称',
  `open_date` date DEFAULT NULL COMMENT '开盘时间',
  `houses` text COMMENT '楼盘房屋',
  `digest` varchar(32) DEFAULT NULL COMMENT '摘要验证',
  PRIMARY KEY (`id`),
  KEY `idx_project_code` (`project_code`),
  KEY `idx_building_code` (`building_code`),
  KEY `idx_gmt_created` (`gmt_created`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `house` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `gmt_created` datetime DEFAULT NULL COMMENT '创建时间',
  `gmt_modified` datetime DEFAULT NULL COMMENT '修改时间',
  `property_name` varchar(128) COLLATE utf8_bin DEFAULT NULL COMMENT '项目名称',
  `building_name` varchar(128) COLLATE utf8_bin DEFAULT NULL COMMENT '楼栋',
  `house_name` varchar(32) COLLATE utf8_bin DEFAULT NULL COMMENT '房号',
  `plan_purpose` varchar(8) COLLATE utf8_bin DEFAULT NULL COMMENT '规划用途',
  `house_purpose` varchar(8) COLLATE utf8_bin DEFAULT NULL COMMENT '房屋功能',
  `floor` varchar(8) COLLATE utf8_bin DEFAULT NULL COMMENT '所在楼层',
  `floor_height` double DEFAULT NULL COMMENT '层高',
  `house_orientation` varchar(8) COLLATE utf8_bin DEFAULT NULL COMMENT '房屋朝向',
  `house_construction` varchar(8) COLLATE utf8_bin DEFAULT NULL COMMENT '房屋结构',
  `is_public` tinyint(1) DEFAULT NULL COMMENT '是否公建配套',
  `is_back_moving` tinyint(1) DEFAULT NULL COMMENT '是否回迁',
  `is_oneself` tinyint(1) DEFAULT NULL COMMENT '是否自用',
  `is_pre_sell` tinyint(1) DEFAULT NULL COMMENT '批准预售状态',
  `price` double DEFAULT NULL COMMENT '商品房销售价目表',
  `pre_total_square` double DEFAULT NULL COMMENT '预测总面积',
  `actual_total_square` double DEFAULT NULL COMMENT '实测面积',
  `pre_inner_square` double DEFAULT NULL COMMENT '预测套内面积',
  `actual_inner_square` double DEFAULT NULL COMMENT '实测套内面积',
  `pre_public_square` double DEFAULT NULL COMMENT '预测公摊面积',
  `actual_public_square` double DEFAULT NULL COMMENT '实测公摊面积',
  `is_pledge` tinyint(1) DEFAULT NULL COMMENT '是否抵押',
  `is_seal` tinyint(1) DEFAULT NULL COMMENT '是否查封',
  `open_date` datetime DEFAULT NULL COMMENT '开盘时间',
  PRIMARY KEY (`id`),
  KEY `idx_property_name` (`property_name`),
  KEY `idx_building_name` (`building_name`),
  KEY `idx_open_date` (`open_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
