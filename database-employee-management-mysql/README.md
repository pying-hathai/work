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

## 🔹สร้าง Foreign key
สร้าง Foreign key แบบ Casecade - เมื่อ PK ถูกลบ FK จะถูกลบด้วย

Foreign key แบบ SET NULL - เมื่อ PK ถูกลบ FK จะเป็น Null

Foreign key แบบ RESTRICT - PK จะไม่ถูกลบเมื่อมี FK ห้อยตามอยู่


# SQL Sample Queries – Employee Management System

This repository contains sample SQL queries demonstrating how to retrieve and analyze data from an Employee Management System database.

The examples focus on:
- Table relationships (JOIN)
- Aggregation and grouping
- Real-world employee and department use cases

---

## 🔹 Query 1: Employee & Department

**โจทย์:**  
แสดงข้อมูลพนักงาน (Employee) และแผนก (Department)

```sql
SELECT 
    p.empusername,
    d.depname,
    d.dep_id
FROM emp_profile p
JOIN dep d
    ON p.dep_id = d.id;
```
![Query 1 Result: Employee and Department Data](screenshots/query1-employee-department.png)


## 🔹 Query 2: Department Summary & Employee Count

**โจทย์:**  
แสดงข้อมูลพนักงาน (Employee) และแผนก (Department) พร้อมนับจำนวนพนักงานในแต่ละแผนก

**Objective:**  
Display departments with employee count and employee list.

```sql
SELECT 
    d.depname AS department_name,
    d.dep_id AS department_id,
    COUNT(p.empusername) AS employee_count,
    GROUP_CONCAT(p.empusername) AS employee_usernames
FROM dep d
JOIN emp_profile p
    ON d.id = p.dep_id
GROUP BY d.depname;
```
![Query / Result: department-summary](screenshots/query2-department-summary.png)


## 🔹 Query 3: Employee Contact Information

**โจทย์:**  
แสดงข้อมูลพนักงาน (Employee) และข้อมูลการติดต่อ

**Objective:**  
Display employee profile with contact details.

```sql
SELECT 
    p.nametitle,
    p.lastname,
    p.empusername,
    c.tel,
    c.email
FROM emp_profile p
JOIN emp_contact c
    ON p.id = c.emp_profile_id;

```
![Query / Result: employee-contact](screenshots/query3-employee-contact.png)