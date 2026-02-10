# SQL Sample Queries – Employee Management System

## 🔹 Query 1: Employee & Department

**Objective:**  
Display employees along with their department information.

### SQL Query
```sql
SELECT 
    p.empusername,
    d.depname,
    d.dep_id
FROM emp_profile p
JOIN dep d
    ON p.dep_id = d.id;