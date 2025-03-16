/*
 * DML중 SELECT 이외
 * INSERT, UPDATE, DELETE 
 */
-- 기본값을 설정하면서 테이블 생성
CREATE TABLE new_table (
	NO 		NUMBER(5, 0)  PRIMARY KEY, -- PK는 지정하는게 기본
	NAME   varchar2(20)   NOT NULL, 
	jumin	char(14), 
	birth	DATE,
	salary  number(7, 0) DEFAULT 0  -- 아무값도 넣지않고 INSERT하면 NULL을 0으로 대체
);
-- INSERT 
SELECT * FROM NEW_TABLE;

-- INSERT QUERY기본
INSERT INTO new_table (NO, name, jumin, birth, salary)
VALUES (1, '홍길동', '810205-1825697', '1981-02-05', 5000);

-- 테이블 컬럼리스트와 동일한 순서, 동일한 값을 넣을때
-- 단, 컬럼리스트와 순서도 다르고, 값리스트 갯수도 다르면 컬럼리스트 생략 불가!
INSERT INTO new_table 
VALUES (2, '홍길순', '830105-2825698', '1983-01-05', 4000);

-- 컬럼리스트 순서와 갯수가 다를때는 반드시 적어줘야 함.
INSERT INTO new_table (jumin, name, no)
VALUES ('760921-1825899', '성유고', 3);

-- 값이 먼지 모를때는 NULL로 삽입
INSERT INTO new_table 
VALUES (4, '홍길태', '830105-1825699', NULL, NULL);

-- 한 테이블에 있는 데이터를 모두 옮기면서 새로운 테이블 생성
-- PK는 복사가 안됨!
CREATE TABLE professor_new
AS
 SELECT * FROM professor;

SELECT * FROM PROFESSOR_NEW;

-- 만들어진 테이블에 데이터 한꺼번에 옮기기
INSERT INTO PROFESSOR_NEW 
SELECT * FROM PROFESSOR;

-- 새로 만들어진 테이블 Professor_new 데이터를 삽입 테스트
INSERT INTO PROFESSOR_NEW (profno, name, id, POSITION, pay, hiredate)
VALUES (4008, 'Tom Cruise', 'Cruise', 'instructor', 300, '2025-03-14');

-- PROFESSOR_NEW는 PK가 없기때문에 같은 값이 들어감
INSERT INTO PROFESSOR_NEW (profno, name, id, POSITION, pay, hiredate)
VALUES (4008, 'Tom Holland', 'Holland', 'instructor', 310, '2025-03-14');

-- 대량의 데이터를 삽입. Oracle방식
INSERT ALL
	INTO new_table values (5, '홍길길', '810205-1825697', '1981-02-05', 5000)
	INTO new_table values (6, '홍길평', '810205-1825697', '1981-02-05', 5000)
	INTO new_table values (7, '홍길똥', '810205-1825697', '1981-02-05', 5000)
	INTO new_table values (8, '홍길군', '810205-1825697', '1981-02-05', 5000)
	INTO new_table values (9, '홍길치', '810205-1825697', '1981-02-05', 5000)
SELECT * FROM dual;

SELECT * FROM NEW_TABLE;

-- SET TRANSACTION READ WRITE;  -- 안써도 무방

-- 테이블 복사
CREATE TABLE REGIONS_NEW
AS
 SELECT * FROM REGIONS;

-- 커밋
COMMIT;

-- 데이터 조회
SELECT * FROM REGIONS_NEW;

-- 실수로 전부삭제
DELETE FROM REGIONS_NEW;

ROLLBACK; -- 원상복귀, 트랜잭션은 종료안됨
COMMIT; -- 확정짓고 트랜잭션이 종료!

-- 실수로 모두 동일값으로 변경
UPDATE REGIONS_NEW SET
  REGION_NAME = 'North America';

-- 데이터 조회
SELECT * FROM REGIONS_NEW;

ROLLBACK; -- 원상복귀, 트랜잭션은 종료안됨
COMMIT; -- 확정짓고 트랜잭션이 종료!

/*
 * 제약조건. 잘못된 데이터가 들어가지 않도록 막는 기능
 */
-- 제약조건 다섯가지 모두 사용한 테이블 생성 쿼리
CREATE TABLE new_emp (
	idx NUMBER PRIMARY KEY,
	name varchar2(20) NOT NULL,
	jumin varchar2(14) NOT NULL UNIQUE,
	loc_code number(1) CHECK (loc_code > 0 AND loc_code < 5), -- loc_code 1, 2, 3, 4
	dcode varchar2(6) REFERENCES dept2(dcode)
);

-- 이름에 UNIQUE 제약조건을 추가로 걸때
ALTER TABLE new_emp
  ADD CONSTRAINT uk_name UNIQUE(name);

-- 제약조건 변경
ALTER TABLE new_emp
  MODIFY (loc_code CONSTRAINT ck_loc_code CHECK (loc_code > 0 AND loc_code < 7));

-- 필요없는 제약조건 삭제
ALTER TABLE new_emp DROP CONSTRAINT "SYS_C007156";

/*
 * 인덱스 - DB검색을 효율적으로 빠르게 처리하는 기술
 */
-- 기본 테이블 생성(인덱스없음)
CREATE TABLE test_noindex (
	id NUMBER NOT NULL,
	name varchar(20) NOT NULL,
	phone varchar(20) NULL,
	rdate DATE DEFAULT sysdate
);

-- 인덱스 테이블 생성
CREATE TABLE test_index (
	id NUMBER NOT NULL PRIMARY KEY,
	name varchar(20) NOT NULL,
	phone varchar(20) NULL,
	rdate DATE DEFAULT sysdate
);

-- 유니크인덱스 테이블 생성(유니크인덱스)
CREATE TABLE test_unqindex (
	id NUMBER NOT NULL,
	name varchar(20) NOT NULL UNIQUE, 
	phone varchar(20) NULL,
	rdate DATE DEFAULT sysdate
);

-- 인덱스 생성 쿼리 테스트용 테이블 생성
CREATE TABLE test_index2 (
	id NUMBER NOT NULL,
	name varchar(20) NOT NULL,
	phone varchar(20) NULL,
	rdate DATE DEFAULT sysdate
);

-- 인덱스 생성 쿼리
CREATE INDEX idx_id ON test_index2(id);

CREATE INDEX idx_name_phone ON test_index2(name, phone);

CREATE INDEX idx_id_name2  ON test_index2(id, name);

/*
 * 인덱스 테스트. 인덱스가 없을때 검색쿼리 실행소요시간, 
 *             인덱스 구성후 검색쿼리 실행소요시간 비교
 **/
-- 인덱스 테스트 sample_t
-- 번호가 중복된게 있는지 확인 쿼리
SELECT COUNT(ID1)
  FROM sample_t
 GROUP BY ID1
HAVING COUNT(ID1) > 1;

SELECT *
  FROM sample_t WHERE ID1 = 10000000;

-- 검색
SELECT *
  FROM sample_t
 WHERE ID1 IN (976453, 934564, 174555, 6785, 146789, 897554);

SELECT *
  FROM SAMPLE_T;

-- sample_t에 PK추가
ALTER TABLE sample_t ADD PRIMARY KEY(id1);
-- 인덱스 테이블 생성으로 30초정도 시간 소요

-- date1번에서 조회
SELECT *
  FROM sample_t
 WHERE date1 = '20171206';
-- 0.45초 소요 인덱스 생성 후는 0.019초 소요

CREATE INDEX idx_date1 ON sample_t(date1);



-- test3 컬럽 값 조회 
SELECT *
  FROM sample_t
 WHERE test3 = 'A678';

-- autocommit을 끄고나면 DDL, DML(select이외) 작업후 필히 commit;수행 후 파일 저장
COMMIT;




















