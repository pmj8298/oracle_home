import cx_Oracle as oci
from faker import Faker

fake = Faker('ko-KR')

sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'

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

        teacher_no_list = []  # 생성된 T_NO 리스트 저장

        try:
            conn.begin()

            query = '''
                    INSERT INTO ATTENDANCE.TEACHER (T_NO, T_ID, T_PW, T_NAME, T_TEL, CLASS_NO) 
                    VALUES(ATTENDANCE.teacher_t_no_seq.nextval, :1, :2, :3, :4, :5)
                    '''

            data_list = [(fake.user_name(), fake.password(), fake.name(), fake.phone_number(), class_no) for class_no in class_no_list]

            print("삽입할 데이터 목록:", data_list)
            cursor.executemany(query, data_list)

            conn.commit()
            print("10개 데이터 삽입 완료")
            isSucceed = True

            # 삽입된 교사 T_NO 가져오기
            cursor.execute('SELECT T_NO, CLASS_NO FROM ATTENDANCE.TEACHER ORDER BY T_NO')
            teacher_no_list = cursor.fetchall()  # (T_NO, CLASS_NO) 튜플 리스트

            print("삽입된 TEACHER T_NO들:", teacher_no_list)

            # CLASS 테이블의 T_NO 업데이트
            update_query = '''
                UPDATE ATTENDANCE.CLASS 
                SET T_NO = :1 
                WHERE CLASS_NO = :2
            '''
            cursor.executemany(update_query, teacher_no_list)

            conn.commit()
            print("CLASS 테이블의 T_NO 업데이트 완료")

        except Exception as e:
            print("오류 발생:", e)
            conn.rollback()
            isSucceed = False
        finally:
            cursor.close()
            conn.close()

        return isSucceed


# 실행 예시
add_data = AddData()
class_no_list = add_data.addCdata()  # class 테이블에 데이터 추가 후 class_no 리스트 반환
if class_no_list:
    add_data.addTdata(class_no_list)  # teacher 테이블에 class_no를 포함한 데이터 삽입 후, class 테이블의 T_NO 업데이트
