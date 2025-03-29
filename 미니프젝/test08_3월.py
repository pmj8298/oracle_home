import cx_Oracle as oci
from datetime import datetime, timedelta
import random

# 오라클 DB 접속 정보
sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'

def random_time(current_date):
    status = random.choice(['P', 'L', 'A'])

    if status == 'P':
        time = current_date.replace(hour=random.randint(7, 8), minute=random.randint(0, 59))
    elif status == 'L':
        time = current_date.replace(hour=random.randint(9, 12), minute=random.randint(0, 59))
    else:
        time = current_date.replace(hour=random.randint(13, 23), minute=random.randint(0, 59))

    return time, status

def insert_march_attendance():
    print("3월 출석 데이터 삽입 시작")

    conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
    cursor = conn.cursor()

    try:
        conn.begin()

        # s_no = 1인 학생과 t_no = 1인 교사 확인
        cursor.execute("SELECT S_NO, CLASS_NO FROM ATTENDANCE.STUDENT WHERE S_NO = 1")
        student = cursor.fetchone()

        cursor.execute("SELECT T_NO, CLASS_NO FROM ATTENDANCE.TEACHER WHERE T_NO = 1")
        teacher = cursor.fetchone()

        if not student or not teacher:
            print("학생 또는 교사를 찾을 수 없습니다.")
            return

        s_no, student_class_no = student
        t_no, teacher_class_no = teacher

        if student_class_no != teacher_class_no:
            print("학생과 교사의 CLASS_NO가 일치하지 않습니다.")
            return

        # 출석 데이터 생성 (2025년 3월 1일 ~ 3월 31일, 월~금만)
        attendance_data = []

        start_date = datetime(2025, 3, 1)
        end_date = datetime(2025, 3, 31)
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5:  # 월~금만
                atd_time, status = random_time(current_date)
                attendance_data.append((s_no, current_date.strftime('%Y-%m-%d'), atd_time.strftime('%Y-%m-%d %H:%M:%S'), t_no, status))

            current_date += timedelta(days=1)

        # ATD 테이블에 삽입
        query = '''
            INSERT INTO ATTENDANCE.ATD (ATD_no, S_NO, ATD_DATE, ATD_TIME, T_NO, STATUS) 
            VALUES(ATTENDANCE.atd_no_seq.nextval, :1, TO_DATE(:2, 'YYYY-MM-DD'), TO_DATE(:3, 'YYYY-MM-DD HH24:MI:SS'), :4, :5)
        '''

        cursor.executemany(query, attendance_data)
        conn.commit()

        print(f"ATD 테이블에 {len(attendance_data)}개 출석 데이터 삽입 완료 (3월 한 달간, 월~금만 기록)")

    except Exception as e:
        print("출석 데이터 삽입 오류 발생:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_march_attendance()
