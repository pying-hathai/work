# Employee Database Management (MySQL)

## Overview
Designed and implemented a MySQL database to manage employee information in a structured and centralized system.

## Problem
Employee data was stored across multiple files and formats, making it difficult to manage, update, and ensure data consistency.

## Solution
- Designed a relational database schema for employee management
- Implemented MySQL tables with proper relationships
- Applied data normalization to reduce redundancy
- Enabled efficient querying and data maintenance

## Tools
MySQL, SQL

## Result
- Centralized employee data management
- Improved data consistency and integrity
- Simplified employee data retrieval and updates

# Employee Database Management (MySQL)

## Overview
Relational database design for managing employee master data using MySQL.

## Database Design
![ER](screenshots/er-diagram.png)

*ER diagram showing normalized tables and relationships for employee data management.*

## Key Tables
- emp_profile
- emp_contact
- dep
- emp_groupuser
- profile_groupuser

## One-to-One: Employee Profile & Contact
![One-to-One Relationship](screenshots/one-to-one-emp-profile-contact.png)

*One employee profile is linked to one contact record using a foreign key with
ON DELETE CASCADE.*

## One-to-Many: Department & Employee
![One-to-Many Relationship](screenshots/one-to-many-department-employee.png)

*One department can be associated with many employee profiles.*

## Many-to-Many: Employee & Group
![Many-to-Many Relationship](screenshots/many-to-many-employee-group.png)

*Employees can belong to multiple groups, and each group can contain multiple employees.*