import cx_Oracle as oci
from faker import Faker
import random

fake = Faker('ko-KR')

sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'


def generate_date_of_birth():
    """ 랜덤한 생년월일 (2020~2022년) 생성 """
    year = random.choice([2020, 2021, 2022])
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 월별 일수를 고려하지 않고 28일까지만 사용
    return f"{year}-{month:02d}-{day:02d}"


class AddData:
    def addCdata(self):
        print("addCdata 함수 실행됨")

        isSucceed = False
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        class_no_list = []

        try:
            conn.begin()

            query = '''
                    INSERT INTO ATTENDANCE.CLASS(CLASS_NO, CLASS_NAME, T_NO)
                    VALUES(ATTENDANCE.class_class_no_seq.nextval, :1, NULL)
                    '''

            data_list = [(f"{i}반",) for i in range(1, 11)]  # "1반" ~ "10반"

            print("삽입할 데이터 목록:", data_list)
            cursor.executemany(query, data_list)

            conn.commit()
            print("10개 데이터 삽입 완료")
            isSucceed = True

            # 삽입된 class_no 가져오기
            cursor.execute('SELECT class_no FROM ATTENDANCE.CLASS ORDER BY class_no')
            class_no_list = [row[0] for row in cursor.fetchall()]

            print("삽입된 CLASS_NO들:", class_no_list)
            return class_no_list

        except Exception as e:
            print("오류 발생:", e)
            conn.rollback()
            isSucceed = False
        finally:
            cursor.close()
            conn.close()

        return isSucceed

    def addTdata(self, class_no_list):
        print("addTdata 함수 실행됨")

        isSucceed = False
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        teacher_no_list = []

        try:
            conn.begin()

            query = '''
                    INSERT INTO ATTENDANCE.TEACHER (T_NO, T_ID, T_PW, T_NAME, T_TEL, CLASS_NO) 
                    VALUES(ATTENDANCE.teacher_t_no_seq.nextval, :1, :2, :3, :4, :5)
                    '''

            data_list = [(fake.user_name(),  # 기존 방식 유지
                          fake.password(),
                          fake.name(),
                          fake.phone_number(),
                          class_no) for class_no in class_no_list]

            print("삽입할 데이터 목록:", data_list)
            cursor.executemany(query, data_list)

            conn.commit()
            print("교사 데이터 삽입 완료")

            # 삽입된 교사 T_NO 가져오기 (CLASS_NO와 매칭)
            cursor.execute('SELECT T_NO, CLASS_NO FROM ATTENDANCE.TEACHER ORDER BY T_NO')
            teacher_no_list = cursor.fetchall()

            print("삽입된 TEACHER T_NO들:", teacher_no_list)

            # **UPDATE 실행 전, NULL인 CLASS 테이블만 업데이트**
            update_query = '''
                UPDATE ATTENDANCE.CLASS 
                SET T_NO = :1 
                WHERE CLASS_NO = :2 AND T_NO IS NULL
            '''
            cursor.executemany(update_query, teacher_no_list)

            conn.commit()
            print("CLASS 테이블의 T_NO 업데이트 완료")

            # **UPDATE 후 검증**
            cursor.execute('SELECT CLASS_NO, T_NO FROM ATTENDANCE.CLASS ORDER BY CLASS_NO')
            updated_class_list = cursor.fetchall()
            print("업데이트된 CLASS 테이블 데이터:", updated_class_list)

        except Exception as e:
            print("오류 발생:", e)
            conn.rollback()
            isSucceed = False
        finally:
            cursor.close()
            conn.close()

        return isSucceed

    def addSdata(self, class_no_list):
        print("addSdata 함수 실행됨")

        isSucceed = False
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin()

            query = '''
                    INSERT INTO ATTENDANCE.STUDENT (S_NO, S_ID, S_PW, S_NAME, S_BIRTH, S_TEL, S_ADDR, CLASS_NO) 
                    VALUES(student_s_no_seq.nextval, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7)
                    '''

            student_data = []
            for class_no in class_no_list:
                student_count = random.randint(25, 30)  # 각 반에 25~30명 배정
                for _ in range(student_count):
                    student_data.append((
                        str(fake.random_number(digits=6)),  # 랜덤 ID
                        fake.password(),                    
                        fake.name(),                        
                        generate_date_of_birth(),  # 2020~2022 랜덤 생년월일
                        fake.phone_number(),                
                        fake.address(),                     
                        class_no                            
                    ))

            print("삽입할 학생 데이터 목록:", student_data)
            cursor.executemany(query, student_data)  

            conn.commit()  
            print(f"학생 데이터 {len(student_data)}개 삽입 완료 (각 반에 25~30명 랜덤 배정)")
            isSucceed = True

        except Exception as e:
            print("오류 발생:", e)
            conn.rollback()  
            isSucceed = False
        finally:
            cursor.close()
            conn.close()

        return isSucceed


if __name__ == "__main__":
    add_data = AddData()

    class_no_list = add_data.addCdata()
    print("addCdata 실행 후 받은 CLASS_NO 목록:", class_no_list)

    if class_no_list:
        result = add_data.addTdata(class_no_list)
        print("addTdata 실행 결과:", result)

        result = add_data.addSdata(class_no_list)
        print("addSdata 실행 결과:", result)
    else:
        print("class_no_list가 비어 있음.")
