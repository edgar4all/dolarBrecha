/*
Navicat MySQL Data Transfer

Source Server         : LOCALHOST -- XAMPP --
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : panel

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2023-12-09 18:03:11
*/

SET FOREIGN_KEY_CHECKS=0;

CREATE DATABASE IF NOT EXISTS dolarbrecha;

USE dolarbrecha;

-- ----------------------------
-- Table structure for dolar
-- ----------------------------
DROP TABLE IF EXISTS `dolar`;
CREATE TABLE `dolar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `compra` decimal(10,0) DEFAULT NULL,
  `venta` decimal(10,0) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1558 DEFAULT CHARSET=latin1;
