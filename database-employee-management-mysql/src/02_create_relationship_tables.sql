-- File: 02_create_relationship_tables.sql
-- Purpose: Create group and mapping tables

CREATE TABLE `emp_groupuser` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `groupuser` VARCHAR(45) NOT NULL,
  `startdate` DATE DEFAULT NULL,
  `enddate` DATE DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `profile_groupuser` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `emp_profile_id` INT DEFAULT NULL,
  `emp_groupuser_id` INT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_emp_profile` (`emp_profile_id`),
  KEY `idx_emp_groupuser` (`emp_groupuser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;