-- Query Statement for Question 1(a)
-- Show the EMPLOYEE_ID, FIRST_NAME, LAST_NAME and DEPARTMENT_NAME of the employees 
-- who are the manager of at least one other employees in the department. 
-- The result should be sorted in ascending EMPLOYEE_ID.
select employee_id, first_name, last_name, department_name
from employees e
join departments d on e.department_id = d.department_id
where e.employee_id in 
(select manager_id from employees
where manager_id is not null)
order by employee_id;


-- Query Statement for Question 1(b)
-- For each department, show the city where the department is located and the 
-- number of employees in the department, sorted by decreasing number of 
-- employees in the department followed by ascending department name 
-- (if two departments have the same number of employees).
select t3.department_name, t3.city, t3.number_of_employees from
(
select COALESCE(t2.number_of_employees, 0) as number_of_employees, t2.department_name, l.city
from
(
select t1.number_of_employees, d.department_name, d.location_id
from
(select count(employee_id) as number_of_employees, department_id 
from employees
where department_id is not null
group by department_id) t1
right join departments d on t1.department_id = d.department_id
) t2
join locations l on t2.location_id = l.location_id
) t3
order by t3.number_of_employees desc, t3.department_name asc;


-- Query Statement for Question 1(c)
-- For each department with more than 3 employees whose salary is higher than
-- the average salary of the company, show the number the number of employees 
-- whose salary is higher than the average salary of the company.
select d.department_name, t3.number_of_employee
from
(
select * from
(
select count(t1.employee_id) as number_of_employee, t1.department_id from
(
select *
from employees 
where salary > (
select avg(salary) from employees)
) t1
where t1.department_id is not null
group by t1.department_id
) t2
where t2.number_of_employee > 3
) t3
join departments d on d.department_id = t3.department_id
order by t3.number_of_employee desc, d.department_name asc;


-- Query Statement for Question 1(d)
-- For each department, show and the first name and last name of the employee 
-- whose salary is higher than all employees in that department. The result
-- should be ordered by ascending department name. You should ignore those 
-- departments in which none of the employee’s salary is known.
select  t2.department_name, e.first_name, e.last_name from 
(
select t1.highest_salary, d.department_name, t1.department_id from
(
select max(salary) as highest_salary, department_id
from employees
group by department_id
) t1
join departments d on t1.department_id = d.department_id
) t2
inner join employees e on t2.department_id = e.department_id
where e.salary = t2.highest_salary and e.department_id = t2.department_id
order by t2.department_name;
 



