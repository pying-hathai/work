--🔹 Query 1: Employee & Department
SELECT 
    p.empusername,
    d.depname,
    d.dep_id
FROM emp_profile p
JOIN dep d
    ON p.dep_id = d.id;

--🔹 Query 2: Department Summary & Employee Count
SELECT 
    d.depname AS department_name,
    d.dep_id AS department_id,
    COUNT(p.empusername) AS employee_count,
    GROUP_CONCAT(p.empusername) AS employee_usernames
FROM dep d
JOIN emp_profile p
    ON d.id = p.dep_id
GROUP BY d.depname;


--🔹 Query 3: Employee Contact Information

SELECT 
    p.nametitle,
    p.lastname,
    p.empusername,
    c.tel,
    c.email
FROM emp_profile p
JOIN emp_contact c
    ON p.id = c.emp_profile_id;
