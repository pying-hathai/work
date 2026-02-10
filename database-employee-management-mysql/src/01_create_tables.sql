#One to One
#Table: emp_profile

CREATE TABLE `emp_profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nametitle` varchar(10) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `empusername` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dep_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `emp_code_UNIQUE` (`empusername`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

#Table: emp_contact
CREATE TABLE `emp_contact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tel` int NOT NULL,
  `email` varchar(45) NOT NULL,
  `emp_profile_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_empcontact_empprofile_idx` (`emp_profile_id`),
  CONSTRAINT `fk_empcontact_empprofile` FOREIGN KEY (`emp_profile_id`) REFERENCES `emp_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

#One to Many
#Table: Department information
CREATE TABLE `dep` (
  `id` int NOT NULL AUTO_INCREMENT,
  `depname` varchar(45) NOT NULL,
  `dep_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `depname_UNIQUE` (`depname`),
  KEY `fk_dep_empprofile` (`dep_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

#Many to Many
#สร้าง Relational table เพื่อเชื่อมความสัมพันธ์ One to Many 2 Table เข้าด้วยกัน
#1) emp_profile to profile_group
CREATE TABLE `profile_groupuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_profile_id` int DEFAULT NULL,
  `emp_groupuser_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_profile_groupuser_to_emp_profile_idx` (`emp_profile_id`),
  KEY `fk_profile_groupuser_to_emp_groupuser_idx` (`emp_groupuser_id`),
  CONSTRAINT `fk_profile_groupuser_to_emp_groupuser` FOREIGN KEY (`emp_groupuser_id`) REFERENCES `emp_groupuser` (`id`),
  CONSTRAINT `fk_profile_groupuser_to_emp_profile` FOREIGN KEY (`emp_profile_id`) REFERENCES `emp_profile` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

#2) emp_groupuser to profile_group
CREATE TABLE `emp_groupuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `groupuser` varchar(45) NOT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

#สร้าง Foreign key
#สร้าง Foreign key แบบ Casecade - เมื่อ PK ถูกลบ FK จะถูกลบด้วย
#Foreign key แบบ SET NULL - เมื่อ PK ถูกลบ FK จะเป็น Null
#Foreign key แบบ RESTRICT - PK จะไม่ถูกลบเมื่อมี FK ห้อยตามอยู่