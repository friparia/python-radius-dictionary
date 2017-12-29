SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE `rad_attribute` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `vendor` int(11) NOT NULL,
  `code` int(11) NOT NULL,
  `encrypt` int(11) DEFAULT NULL,
  `has_tag` tinyint(1) DEFAULT NULL,
  `type` enum('string','octets','ipaddr','date','integer','signed','short','ipv6addr','ipv6prefix','ifid','integer64','abinary','ether','ipv4prefix','tlv','vsa','extended','long-extended','combo-ip') NOT NULL,
  `remark` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `rad_value` (
  `vendor` int(11) NOT NULL,
  `code` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `value` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `rad_vendor` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type_length` int(11) NOT NULL,
  `length_length` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `rad_attribute`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `vendor` (`vendor`,`code`);

ALTER TABLE `rad_value`
ADD UNIQUE KEY `vendor` (`vendor`,`code`,`name`);

ALTER TABLE `rad_vendor`
ADD PRIMARY KEY (`id`);


ALTER TABLE `rad_attribute`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29337;
