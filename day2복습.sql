/*
 * -- CONCAT
 * */
SELECT concat('Hello', 'Oracle') -- 한행 한열만 출력되는 값 : 스칼라(Scalar)값
	FROM dual;

-- 1. 고객의 풀네임 생성
SELECT CONCAT(first_name ,last_name) AS "full_name"
	FROM employees;

-- 2. 이메일 자동 생성
SELECT CONCAT(email, '@company.com') AS 이메일 FROM employees;

-- 3. 제품 코드 생성 (카테고리 + 제품번호)
-- SELECT CONCAT(category_code, '-', product_id) AS product_code FROM products;

-- 4. 배송 메시지 만들기
SELECT CONCAT('부서: ', department_id) AS message FROM departments;

-- 5. 주소 필드 결합 (도로명 + 시 + 국가)
--SELECT CONCAT(street, ', ', city, ', ', country) AS full_address FROM addresses;

/*
 * SUBSTR(문자열, 시작 위치, 길이)
 * */
-- 1. 이메일 아이디 부분만 추출
-- SELECT SUBSTR(email, 2, INSTR(email, '@') - 1) AS email_id,
--	   email
--	FROM employees;

-- 2. 주민번호 앞자리(생년월일) 가져오기
-- SELECT SUBSTR(ssn, 1, 6) AS birth_date FROM citizens;

-- 3. 전화번호 뒷자리만 가져오기
SELECT SUBSTR(phone_number, -4, 4) AS last_digits FROM employees;

-- 4. 제품 코드에서 버전 정보만 추출
-- SELECT SUBSTR(product_code, INSTR(product_code, '-V') + 2) AS version FROM products;

-- 5. 날짜에서 연도만 추출
SELECT SUBSTR(hire_date, 1, 2) AS year FROM employees;

/*
 * INSTR
 * */

-- 1. 이메일에서 '@' 위치 찾기
-- SELECT INSTR(email, '@') FROM users;

-- 2. 전화번호에서 첫 번째 '.' 위치 찾기
SELECT INSTR(phone_number, '.', 1) FROM employees; -- 4

-- 3. 전화번호에서 두 번째 '.' 위치 찾기
SELECT INSTR(phone_number, '.', 1, 2) FROM employees; --8

-- 4. 제품 코드에서 'V'의 위치 찾기
SELECT INSTR(job_id, 'IT') FROM employees;

-- 5. 파일 경로에서 마지막 '/' 위치 찾기 (파일명 추출 시 사용)
--SELECT INSTR(file_path, '/', -1, 1) FROM files;

/*
 * LPAD() / RPAD() - 자리수 맞추기
 * */
-- 1. 3자리 숫자 코드 만들기 (앞에 0 채우기)
SELECT LPAD(region_id, 3, '0') FROM countries;

-- 2. 2자리 월(MM) 포맷 맞추기
SELECT LPAD(department_id, 3, '0') FROM departments;

-- 3. 8자리 주문번호 만들기 (앞에 0 채우기)
-- SELECT LPAD(order_id, 8, '0') FROM orders;

-- 4. 오른쪽에 '-' 붙여서 포맷 맞추기
--- SELECT RPAD(category, 10, '-') FROM categories;

-- 5. 특정 길이로 이름 포맷 맞추기
SELECT RPAD(first_name, 10, ' ') FROM employees;

/*
 * TRIM() / LTRIM() / RTRIM() - 공백 제거
 * */
-- 1. 앞뒤 공백 제거
SELECT TRIM('   John Doe   ') FROM dual;

-- 2. 왼쪽 공백 제거
SELECT LTRIM('   Hello World') FROM dual;

-- 3. 오른쪽 공백 제거
SELECT RTRIM('Hello World   ') FROM dual;

-- 4. 특정 문자(#) 제거
SELECT TRIM('#' FROM '###Product###') FROM dual;

-- 5. 숫자 앞의 0 제거
SELECT LTRIM('0001234', '0') FROM dual;

/*
 * REPLACE() - 특정 문자열 변경
 * */
-- 1. 전화번호 포맷 변경 ( '-' → '.' )
SELECT REPLACE(phone_number, '-', '.') FROM contacts;

-- 2. 주민번호 마스킹 처리 (앞자리 노출, 뒷자리 * 처리)
SELECT REPLACE(ssn, SUBSTR(ssn, 8), '******') FROM citizens;

-- 3. 'old'를 'new'로 변경
SELECT REPLACE('old_product_code', 'old', 'new') FROM dual;


-- 4. 특정 HTML 태그 제거
SELECT REPLACE('<p>Hello</p>', '<p>', '') FROM dual;

-- 5. 특수문자(,) 제거 후 숫자로 변환
SELECT REPLACE('1,000,000', ',', '') FROM dual;

/*
 * 숫자함수
 * */
-- ROUND() 반올림 함수 - 파이썬 존재
-- CEIL() 올림함수, FLOOR() 내림함수, TRUNC() 내림함수 소수점
-- MOD() 나누기 나머지값 - python mode(), % 연산과 동일
-- POWER() - python ,math.pow(), power(), 2^10 승수계산 동일
SELECT 786.5427 AS res1,
	   round(786.5427) AS round0,      -- 소수점 없이 : 787    출력
	   round(786.5427, 1) AS round1,   -- 소수점 1   : 786.5  출력
	   round(786.5427, 2) AS round2,   -- 소수점 1   : 786.54 출력
	   ceil(786.5427) AS ceilRes,      -- 787
	   floor(786.5427) AS floorRes,    -- 786
	   trunc(786.5427, 3) AS truncRes, -- 786.542
	   mod(10,3) AS 나머지,              -- 1
	   power(2,10) AS "2의10승"         -- 1024
	FROM dual;

/*
 * 날짜함수, 나라마다 표현방식 다름
 * 2025-03-12 아시아
 * March/12/2025 미국, 캐나다
 * 12/March/2025 유럽, 인도
 * 포매팅을 많이 함
 * */
-- 오늘날짜
SELECT sysdate AS 오늘날짜,                        -- GMT기준, +09 필요            : 2025-03-12 01:50:47.000
	   -- 날짜 포매팅 사용되는 YY, YYYY, MM, DD, DAY 년월일
	   -- AM/PM, HH, HH24, MI, SS, W, Q(분기)
	   TO_CHAR(sysdate, 'YYYY-MM-DD') AS 한국식, -- 글자로 바뀌면서 왼쪽정렬이 되어버림  : 2025-03-12
	   TO_CHAR(sysdate, 'YYYY-MM-DD DAY') AS 한국식요일,                      -- : 2025-03-12 수요일
	   TO_CHAR(sysdate, 'PM HH24-MI-SS') AS 시간,                           -- : 오전 01-50-47   
	   TO_CHAR(sysdate, 'MON/DD/YYYY') AS 미국식,                            -- : 3월 /12/2025    
	   TO_CHAR(sysdate, 'DD/MM/YYYY') AS 영국식                              -- : 12/03/2025  
	FROM dual;

-- ADD_MONTH() 월을 추가함수
-- MON, TUE, WED, TUR, FRI, SAT, SUN
SELECT  hire_date,
		to_char(hire_date, 'yyyy-mm-dd') AS 입사일자, -- 2003-06-17
		add_months(hire_date, 3) AS 정규직일자,        -- 2003-09-17 00:00:00.000
		next_day(hire_date, '월') AS 돌아오는월요일,     -- 2003-06-23 00:00:00.000
		last_day('2025-02-01') AS 달마지막날           -- 2025-02-28 00:00:00.000
	FROM employees;

-- GMT + 9
-- 인터벌 숫자 뒤 HOUR, DAY, MONTH, YEAR
SELECT to_char(sysdate + INTERVAL '9' HOUR, 'yyyy-mm-dd hh24:mi:ss') AS seoul_time, -- 2025-03-12 11:25:39
	   to_char(sysdate + INTERVAL '9' DAY, 'yyyy-mm-dd hh24:mi:ss'),                -- 2025-03-21 02:25:39
	   to_char(sysdate + INTERVAL '9' MONTH, 'yyyy-mm-dd hh24:mi:ss'),              -- 2025-12-12 02:25:39
	   to_char(sysdate + INTERVAL '9' YEAR, 'yyyy-mm-dd hh24:mi:ss')                -- 2034-03-12 02:25:39
	FROM DUAL;

--  EXTRACT() - 날짜에서 특정 값만 추출
SELECT EXTRACT(YEAR FROM sysdate) AS "연도",
       EXTRACT(MONTH FROM sysdate) AS 월,
       EXTRACT(DAY FROM sysdate) AS 일
       --EXTRACT(QUARTER FROM sysdate) AS 분기
FROM dual;

-- ROUND() & TRUNC() - 날짜 반올림 & 절삭
SELECT sysdate,
       ROUND(sysdate, 'MONTH') AS 월반올림,  -- 2025-04-01 (가장 가까운 달의 1일로)
       ROUND(sysdate, 'YEAR') AS 년반올림,   -- 2026-01-01 (6월 30일 이후면 다음 해로 반올림)
       TRUNC(sysdate, 'MONTH') AS 월자르기, -- 2025-03-01 (해당 월의 1일)
       TRUNC(sysdate, 'YEAR') AS 년자르기   -- 2025-01-01 (해당 연도의 1월 1일)
FROM dual;

-- MONTHS_BETWEEN() - 두 날짜의 개월 차이 계산
SELECT MONTHS_BETWEEN(TO_DATE('2025-12-01', 'YYYY-MM-DD'), sysdate) AS 개월차이
FROM dual;

-- SYSDATE vs CURRENT_DATE vs SYSTIMESTAMP
SELECT SYSDATE AS 시스템날짜,
       CURRENT_DATE AS 현재날짜,
       SYSTIMESTAMP AS 전체타임스탬프
FROM dual;

-- LAST_DAY() 활용 - 월말 날짜 구하기
SELECT LAST_DAY(TO_DATE('2025-02-15', 'YYYY-MM-DD')) AS "2월마지막날",
       LAST_DAY(TO_DATE('2025-12-10', 'YYYY-MM-DD')) AS "12월마지막날"
FROM dual;

SELECT NEXT_DAY(TO_DATE('2025-03-12', 'YYYY-MM-DD'), '월요일') AS 다음월요일
FROM dual;

-- NEXT_DAY() 활용 - 특정 요일 찾기
SELECT NEXT_DAY(TO_DATE('2025-03-12', 'YYYY-MM-DD'), '월요일') AS 다음월요일
FROM dual;

-- TO_DATE() & TO_CHAR() 활용 - 날짜 변환 및 포맷 변경
SELECT TO_DATE('2025-03-12', 'YYYY-MM-DD') AS 날짜변환,
       TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') AS 포맷팅된날짜
FROM dual;

/*
 * 형변환 함수
 * */
-- TO_CHAR()
-- 숫자형을 문자형으로 변경
SELECT 1234 AS 원본,
	   to_char(12345,'9999999') AS "원본+두자리빈자리", --    12345
	   to_char(12345,'0999999') AS "원본+두자리0",    --  0012345 
	   to_char(12345,'$99999') AS "통화단위+원본",    --  $12345
	   to_char(12345,'99999.99') AS "소수점",       --  12345.00
	   to_char(12345,'99,999') AS "천단위쉼표"       --  12,345	   
	FROM dual;

-- TO_NUMBER() 문자형된 데이터를 숫자로
SELECT '5.0' * 5,
	   to_number('5.0') AS 숫자형변환
	   -- to_number('Hello) 숫자로 변경할 수 없는 형태
	FROM dual;

-- TO_DATE() 날짜형태를 문자형으로
SELECT '2025-03-12',
		to_date('2025-03-12') + 10 -- 2025-03-22 00:00:00.000 / 날짜를 문자형으로 바꾸면 연산이 가능해짐
	FROM dual;

SELECT TO_CHAR(1234567, '9,999,999') AS 천단위쉼표,
       TO_CHAR(123.45, '999.99') AS 소수점포함,
       TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') AS 현재시간,
       TO_CHAR(SYSDATE, 'YYYY"년" MM"월" DD"일"') AS 한글날짜,
       TO_CHAR(SYSDATE, 'DAY') AS 요일
FROM dual;


/*
 * 일반함수
 * */
-- NVL(컬럼|데이터, 바꿀값) 널값을 다른값으로 치환
SELECT commission_pct,
	   nvl(commission_pct, 0.0)
	FROM employees;

SELECT nvl(hire_date, sysdate) -- 입사일자가 비어있으면 오늘날짜로 대체
	FROM employees;

-- NVL2(컬럼|데이터, 널이 아닐대 처리, 널일때 처리할 부분)
SELECT commission_pct,
	   salary,
	   nvl2(commission_pct, salary + (salary * commission_pct), salary) AS 커미션급여
	FROM employees;

-- DECODE(A,B,'1','2') A가 B일 경우 1 아니면 2
-- 오라클만 있는 함수
SELECT email, phone_number, job_id,
	   decode(job_id, 'IT_PROG', '개발자만세', '개발자외') AS 캐치프레이즈
	FROM employees;
--  WHERE job_id = 'IT_PROG';

SELECT employee_id, commission_pct,
       NVL(commission_pct, 0) AS 기본값적용
FROM employees;


/*
 * CASE 구문, 정말 중요!
 * if, elif의 중복된 구문과 유사
 * */
SELECT CASE employee_id WHEN 100 THEN '사장'
						WHEN 101 THEN '부사장'
						WHEN 102 THEN '부사장'
	   END,
	   employee_id,
	   job_id
	FROM employees;

SELECT CASE job_id WHEN 'AD_PRES' THEN '사장'
				   WHEN 'AD_VP'   THEN '부사장'
				   WHEN 'IT_PROG' THEN '프로그래머'
				   WHEN 'SA_MAN'  THEN '영업사원'
				   ELSE '미분류'
	   END AS 직급,
	   employee_id,
	   job_id
	FROM employees;

SELECT employee_id,
       salary,
       CASE 
           WHEN salary >= 10000 THEN '고액 연봉'
           WHEN salary BETWEEN 5000 AND 9999 THEN '중간 연봉'
           ELSE '저연봉'
       END AS 연봉등급
FROM employees;


/*
 * 정규식(Regula Expression) - 문자열 패턴을 가지고, 동일한 패턴 데이터 추출 사용
 * ^, $, ., *, [], [^] 패턴인식할때 필요한 키워드
 * */
SELECT *
	FROM employees
  WHERE phone_number LIKE '%.%.%'; -- 세,네자리 전화번호가 구분이 안감

  -- 전화번호가 .로 구분되는 세자리 전화번호만 필터링
  -- '[1-9]{6}-[1-9]{7}' : 주민번호 패턴
SELECT *
	FROM employees
  WHERE REGEXP_LIKE(phone_number, '[1-9]{3}.[1-9]{3}.[1-9]{4}');

-- first_name이 J로 시작하고, 두번째 글자가 a나 o인 사람을 출력하시오
SELECT *
	FROM employees
  WHERE REGEXP_LIKE(first_name, '^J[a|o]');

/*
 * 복수행, GROUP BY와 가장 많이 사용
 * COUNT(), SUM(), AVG(), MIN/MAX(), STDDEV(), ...
 * ROLLUP, CUBE, RANK...
 * */
-- COUNT() - 무지무지 많이 사용함
SELECT count(*) -- scalar value
	FROM employees;

SELECT count(employee_id) -- scalar value
	FROM employees;

-- SUM(숫자형컬럼) 합계
-- employees 206 salary 8300 삭제
SELECT sum(salary)
	FROM employees;

-- AVG(숫자형컬럼) 평균
-- column 에 null 값이 있으면 제외하고 계산하기 때문에 잘못된 값이 도출
-- 금액이나 수량을 계산하는 컬럼의 null값은 항상 전처리를 해주어야한다
SELECT avg(salary)
	FROM employees;

-- null은 계산이 안됨
SELECT count(salary)
	FROM employees;

-- MIN(숫자형컬럼|문자형도 가능), MAX()
SELECT MAX(salary), min(salary)
	FROM employees;

SELECT MAX(first_name), min(first_name) -- Winston / Adam
	FROM employees;

/*
 * GROUP BY 연계, 데이터를 그룹화 시킴
 * GROUP BY 를 사용하면 SELECT 절에는 GROUP BY 에 사용한 column 과 집계함수 및 일반함수만 사용할 수 있다. 
 * */
-- 아래의 경우 department_id 이외의 컬럼은 사용불가
SELECT department_id,
	   avg(salary) AS 부서별평균급여,
	   to_char(round(avg(salary),1),'99,999.9') AS 부서별평균급여
	FROM employees
  GROUP BY department_id
  ORDER BY avg(salary) desc;

-- employees 에서 부서와 직군별 급여총액과 직원수를 출력
SELECT department_id, job_id, sum(salary) AS 부서직군별급여총액
	FROM employees
GROUP BY  department_id, job_id
ORDER BY  department_id;

-- employees 에서 부서와 직군별 급여총액과 직원수를 출력하는데
-- department_id 가 30에서 90 사이이고, 부서직군별급여총액이 20000달러 이상인 데이터만 보일것
SELECT department_id, job_id, sum(salary) AS 부서직군별급여총액
	FROM employees
WHERE department_id BETWEEN 30 AND 90
--    AND sum(salary) >= 20000 - 집계함수는 where에 사용불가
GROUP BY  department_id, job_id
HAVING sum(salary) >= 20000
ORDER BY  department_id;

-- ORDER BY에는 컬럼의 순번(1부터 시작)으로 컬럼명을 대체가능
SELECT department_id, job_id, sum(salary) AS 부서직군별급여총액, count(*)
	FROM employees
WHERE department_id BETWEEN 30 AND 90
GROUP BY  department_id, job_id
HAVING sum(salary) >= 20000
ORDER BY 3 desc;

-- ROLLUP 그룹별 소계와 총계를 표시해주는 기능
SELECT department_id, job_id, sum(salary) AS 부서직군별급여총액, count(*)
	FROM employees
WHERE department_id BETWEEN 30 AND 90
GROUP BY ROLLUP (department_id, job_id); -- 앞에 있는 department_id의 합계와 전체 합계를 보여줌
--HAVING sum(salary) >= 20000

-- CUBE
SELECT department_id, job_id, SUM(salary) AS 급여총합
FROM employees
GROUP BY CUBE(department_id, job_id); --  "부서별 합계 + 직군별 합계 + 전체 합계"

-- Groupings ??

-- PIVOT() 엑셀에 동일한 기능
-- PIVOT 안쓰고 각 달별로 입사한 사원릐 수를 표시. 12행
-- 각 입사일자에서 달만 추출
SELECT to_char(hire_date,'MM')
	FROM employees;

-- 1월 달에 입사한 사람 카운팅
SELECT CASE to_char(hire_date,'MM') WHEN '01' THEN count(*) ELSE 0 END AS "1월"
	FROM employees
  GROUP BY to_char(hire_date,'MM');

-- 옆으로 각 달별로 스프레드
SELECT CASE to_char(hire_date,'MM') WHEN '01' THEN count(*) ELSE 0 END AS "1월",
 	   CASE to_char(hire_date,'MM') WHEN '02' THEN count(*) ELSE 0 END AS "2월",
 	   CASE to_char(hire_date,'MM') WHEN '03' THEN count(*) ELSE 0 END AS "3월",
 	   CASE to_char(hire_date,'MM') WHEN '04' THEN count(*) ELSE 0 END AS "4월",
	   CASE to_char(hire_date,'MM') WHEN '05' THEN count(*) ELSE 0 END AS "5월",
   	 CASE to_char(hire_date,'MM') WHEN '06' THEN count(*) ELSE 0 END AS "6월",
 	   CASE to_char(hire_date,'MM') WHEN '07' THEN count(*) ELSE 0 END AS "7월",
 	   CASE to_char(hire_date,'MM') WHEN '08' THEN count(*) ELSE 0 END AS "8월",
	   CASE to_char(hire_date,'MM') WHEN '09' THEN count(*) ELSE 0 END AS "9월",
	   CASE to_char(hire_date,'MM') WHEN '10' THEN count(*) ELSE 0 END AS "10월",
	   CASE to_char(hire_date,'MM') WHEN '11' THEN count(*) ELSE 0 END AS "11월",
 	   CASE to_char(hire_date,'MM') WHEN '12' THEN count(*) ELSE 0 END AS "12월"
  FROM employees
  GROUP BY to_char(hire_date,'MM')
  ORDER BY to_char(hire_date,'MM');
  
  -- decode
SELECT decode (to_char(hire_date,'MM'), '01', count(*), 0) AS "1월",
 	   decode (to_char(hire_date,'MM'), '02', count(*), 0) AS "2월",
 	   decode (to_char(hire_date,'MM'), '03', count(*), 0) AS "3월",
 	   decode (to_char(hire_date,'MM'), '04', count(*), 0) AS "4월",
	   decode (to_char(hire_date,'MM'), '05', count(*), 0) AS "5월",
   	   decode (to_char(hire_date,'MM'), '06', count(*), 0) AS "6월",
 	   decode (to_char(hire_date,'MM'), '07', count(*), 0) AS "7월",
 	   decode (to_char(hire_date,'MM'), '08', count(*), 0) AS "8월",
	   decode (to_char(hire_date,'MM'), '09', count(*), 0) AS "9월",
	   decode (to_char(hire_date,'MM'), '10', count(*), 0) AS "10월",
	   decode (to_char(hire_date,'MM'), '11', count(*), 0) AS "11월",
 	   decode (to_char(hire_date,'MM'), '12', count(*), 0) AS "12월"
  FROM employees
  GROUP BY to_char(hire_date,'MM')
  ORDER BY to_char(hire_date,'MM');
  
  -- RANK() 등수 공동등수 번호 띄우기, DENSE_RANK() 등수번호가 순차적으로 올라감
-- ROW_NUMBER() 현재 데이터 행번호 출력
SELECT employee_id, last_name, salary,
	   rank() OVER (ORDER BY salary desc) AS "랭크",
	   dense_rank() OVER (ORDER BY salary desc) AS "덴스랭크",
	   row_number() OVER (ORDER BY salary desc) AS "행번호"
	 FROM employees;




















