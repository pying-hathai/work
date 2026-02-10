-- Employee Database Management (MySQL)
-- File: 01_create_core_tables.sql
-- Purpose: Create core employee and department tables

CREATE TABLE `dep` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `depname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `depname_UNIQUE` (`depname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `emp_profile` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nametitle` VARCHAR(10) NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `empusername` VARCHAR(20) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dep_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `empusername_UNIQUE` (`empusername`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `emp_contact` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tel` VARCHAR(20) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `emp_profile_id` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;