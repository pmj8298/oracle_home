-- 전체 직원의 급여 평균보다 더 높은 급여를 받는 직원의 모든 레코드를 검색하기
select avg(sal) from emp;

select * from emp
where sal>(전체 직원의 급여 평균값);

SELECT * FROM EMP
  WHERE SAL > (select avg(sal) from emp);

-- 단일행 서브쿼리(SELECT절)
-- 직원의 이름과 해당 직원의 평균 급여 차이를 출력
SELECT ENAME, sal - (SELECT AVG(sal) FROM emp) AS "salary_difference"
FROM EMP;

-- 각 직원의 급여와 해당 부서의 평균 급여 차이를 출력
SELECT ENAME, SAL, SAL - (SELECT AVG(SAL) FROM EMP e WHERE e.DEPTNO = emp.DEPTNO) AS "dept_salary_diff"
FROM EMP emp;

/*
 * SELECT name, salary, salary - (SELECT AVG(salary) FROM employees WHERE department_id = department_id) AS dept_salary_diff
FROM employees;
이렇게 하면 **"department_id = department_id"**라는 애매한 조건이 되어 SQL이 혼란스러워짐
즉, "이 department_id는 메인 쿼리의 것이야? 서브쿼리의 것이야?" 라는 문제가 발생함
따라서 명확하게 하기 위해 메인 쿼리의 employees를 emp,
**서브쿼리의 employees를 e**라고 별칭을 붙여서
e.department_id = emp.department_id처럼 명확한 조건을 작성하는 것
 * */

-- 가장 높은 급여를 받는 직원의 이름과 급여를 출력
SELECT ENAME, SAL
FROM emp
WHERE sal = (SELECT MAX(sal) FROM emp);

-- 단일행 서브쿼리(FROM절)
-- 전체 평균 급여를 가진 가상의 테이블을 만들어 조회
SELECT *
FROM (SELECT AVG(salary) AS avg_salary FROM employees) AS salary_table;

-- 부서별 최고 급여를 가진 가상 테이블을 조회
SELECT d.department_name, max_salary_table.max_salary
FROM departments d
JOIN (SELECT department_id, MAX(salary) AS max_salary FROM employees GROUP BY department_id) AS max_salary_table
ON d.department_id = max_salary_table.department_id;

-- 가장 급여가 높은 직원들의 정보를 가진 가상의 테이블을 조회
SELECT top_employees.*
FROM (SELECT name, salary, department_id FROM employees WHERE salary = (SELECT MAX(salary) FROM employees)) AS top_employees;

-- 단일행 서브쿼리(WHERE절)
-- 전체 평균 급여보다 높은 급여를 받는 직원 조회
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 특정 부서에서 가장 높은 급여를 받는 직원 조회
SELECT name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees WHERE department_id = 10);

-- 각 부서에서 가장 높은 급여를 받는 직원 조회
SELECT name, salary, department_id
FROM employees e1
WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e1.department_id = e2.department_id);

--==========================================
-- 다중행 서브쿼리(IN 연산자)
-- 특정 부서(10, 20, 30)에 속한 직원 조회
SELECT name, department_id
FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE department_id IN (10, 20, 30));

-- 특정 직책을 가진 직원 조회
SELECT name
FROM employees
WHERE job_id IN (SELECT job_id FROM jobs WHERE job_title LIKE 'Manager%');

-- 급여가 부서별 평균 급여 이상인 직원 조회
SELECT name, salary, department_id
FROM employees
WHERE salary IN (SELECT AVG(salary) FROM employees GROUP BY department_id);

-- 다중행 서브쿼리(>ANY 연산자)
-- 특정 부서 내 최소 급여보다 높은 급여를 받는 직원 조회
SELECT name, salary
FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE department_id = 10);

-- 특정 직책을 가진 직원보다 급여가 높은 직원 조회
SELECT name, salary
FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE job_id = 'IT_PROG');

-- 전체 부서에서 최저 급여보다 높은 급여를 받는 직원 조회
SELECT name, salary
FROM employees
WHERE salary > ANY (SELECT MIN(salary) FROM employees GROUP BY department_id);

-- 다중행 서브쿼리(EXISTS 연산자)
-- 부서에 직원이 있는 경우 해당 부서 조회
SELECT department_name
FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.department_id);

-- 급여가 특정 수준 이상인 직원이 있는 부서 조회
SELECT department_name
FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.department_id AND e.salary > 5000);

-- 직원이 없는 부서 조회
SELECT department_name
FROM departments d
WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.department_id);

/*
IN → 특정 목록에 포함되는지 확인
>ANY → 서브쿼리 값 중 최소값보다 크면 참
<ANY → 서브쿼리 값 중 최대값보다 작으면 참
>ALL → 서브쿼리 값 중 최대값보다도 크면 참
<ALL → 서브쿼리 값 중 최소값보다도 작으면 참
EXISTS → 서브쿼리가 하나라도 값을 반환하면 참
*/

-- 다중행 서브쿼리(<ANY 연산자)
-- 특정 부서에서 가장 낮은 급여보다 더 낮은 급여를 받는 직원 찾기
SELECT name, salary
FROM employees
WHERE salary < ANY (SELECT salary FROM employees WHERE department_id = 20);

-- 각 부서의 평균 급여보다 낮은 급여를 받는 직원 찾기
SELECT name, salary
FROM employees
WHERE salary < ANY (SELECT AVG(salary) FROM employees GROUP BY department_id);

--  모든 관리자 급여 중 하나라도 높은 급여보다 낮은 급여를 받는 직원 찾기
SELECT name, salary
FROM employees
WHERE salary < ANY (SELECT salary FROM employees WHERE job_id = 'MANAGER');

-- 다중행 서브쿼리(<ALL 연산자)
-- 특정 부서에서 가장 낮은 급여보다 더 낮은 급여를 받는 직원 찾기
SELECT name, salary
FROM employees
WHERE salary < ALL (SELECT salary FROM employees WHERE department_id = 30);

-- 각 부서에서 가장 낮은 급여보다 더 낮은 급여를 받는 직원 찾기
SELECT name, salary
FROM employees
WHERE salary < ALL (SELECT MIN(salary) FROM employees GROUP BY department_id);

-- 모든 관리자의 최저 급여보다 낮은 급여를 받는 직원 찾기
SELECT name, salary
FROM employees
WHERE salary < ALL (SELECT salary FROM employees WHERE job_id = 'MANAGER');










































































