-- File: 03_constraints_and_notes.sql
-- Purpose: Define foreign keys and relationship rules

-- emp_profile → dep (One-to-Many)
ALTER TABLE `emp_profile`
ADD CONSTRAINT `fk_empprofile_dep`
FOREIGN KEY (`dep_id`)
REFERENCES `dep` (`id`)
ON UPDATE CASCADE
ON DELETE RESTRICT;

-- emp_contact → emp_profile (One-to-One)
ALTER TABLE `emp_contact`
ADD CONSTRAINT `fk_empcontact_empprofile`
FOREIGN KEY (`emp_profile_id`)
REFERENCES `emp_profile` (`id`)
ON UPDATE CASCADE
ON DELETE CASCADE;

-- profile_groupuser → emp_profile
ALTER TABLE `profile_groupuser`
ADD CONSTRAINT `fk_profilegroup_emp_profile`
FOREIGN KEY (`emp_profile_id`)
REFERENCES `emp_profile` (`id`)
ON UPDATE CASCADE
ON DELETE CASCADE;

-- profile_groupuser → emp_groupuser
ALTER TABLE `profile_groupuser`
ADD CONSTRAINT `fk_profilegroup_emp_groupuser`
FOREIGN KEY (`emp_groupuser_id`)
REFERENCES `emp_groupuser` (`id`)
ON UPDATE CASCADE
ON DELETE SET NULL;