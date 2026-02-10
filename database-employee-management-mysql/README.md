# Employee Database Management (MySQL)

## Overview
Designed and implemented a MySQL database to manage employee information.

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

## Database Design
![ER](screenshots/er-diagram.png)

*ER diagram showing normalized tables and relationships for employee data management.*

## Key Tables
- emp_profile
- emp_contact
- dep
- emp_groupuser
- profile_groupuser

## 🔗 Database Relationships

### 🔹 One-to-One: Employee Profile & Contact
Employee Profile & Contact Information

Tables
- emp_profile – stores core employee information
- emp_contact – stores employee contact details

Each employee profile has exactly one contact record.

![One-to-One Relationship](screenshots/one-to-one-emp-profile-contact.png)

T
---

### 🔹 One-to-Many: Department & Employee
Tables
- dep – department information
- emp_profile – employee profile

One department can have multiple employees,
but each employee belongs to only one department.

![One-to-Many Relationship](screenshots/one-to-many-department-employee.png)

---

### 🔹 Many-to-Many: Employee & Group
Tables
- emp_profile
- emp_groupuser
- profile_groupuser (junction table)
สร้าง joint table มา 1 table เพื่อเชื่อมต่อ จะได้ one to many 2 ตาราง

![Many-to-Many Relationship](screenshots/many-to-many-employee-group.png)

Employees can belong to multiple groups,
and each group can contain multiple employees.