import cx_Oracle as oci
from datetime import datetime, timedelta
import random

# 오라클 DB 접속 정보
sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'

def calculate_status(atd_time):
    # 출석 상태 계산 함수
    # 7시~8시 사이 출석(P), 9시~12시 지각(L), 그 외 결석(A)

    hour = atd_time.hour
    if 7 <= hour < 9:
        return 'P'  # 출석
    elif 9 <= hour < 13:
        return 'L'  # 지각
    else:
        return 'A'  # 결석

def random_time(current_date):
    # 랜덤 시간 생성 (7시~8시 또는 9시~12시)
    status = random.choice(['P', 'L'])
    
    if status == 'P':
        # 출석은 7시~8시 사이의 시간에 찍히게 함
        time = current_date.replace(hour=random.randint(7, 8), minute=random.randint(0, 59))
    elif status == 'L':
        # 지각은 9시~12시 사이의 시간에 찍히게 함
        time = current_date.replace(hour=random.randint(9, 12), minute=random.randint(0, 59))

    return time

def insert_june_attendance():
    print("6월 출석 데이터 삽입 시작")

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

        # 출석 데이터 생성 (2025년 6월 1일 ~ 6월 30일, 월~금만)
        attendance_data = []

        start_date = datetime(2025, 7, 1)
        end_date = datetime(2025, 7, 31)
        current_date = start_date

        total_days = 0
        total_o = 0  # 출석(동그라미)
        total_l = 0  # 지각(세모)
        l_dates = set()  # 'L' 상태의 날짜를 저장할 집합

        while current_date <= end_date:
            if current_date.weekday() < 5:  # 월~금만
                total_days += 1

                # L은 최대 3번만 발생하도록 설정
                if total_l < 3:
                    status = 'L'  # 지각
                    total_l += 1
                    l_dates.add(current_date.date())
                else:
                    status = 'P'  # 출석

                # 시간에 맞는 출석 상태 계산
                atd_time = random_time(current_date)
                status = calculate_status(atd_time)  # 출석 상태 계산

                attendance_data.append((s_no, current_date.strftime('%Y-%m-%d'), atd_time.strftime('%Y-%m-%d %H:%M:%S'), t_no, status))

            current_date += timedelta(days=1)

        # ATD 테이블에 삽입
        query = '''
            INSERT INTO ATTENDANCE.ATD (ATD_no, S_NO, ATD_DATE, ATD_TIME, T_NO, STATUS) 
            VALUES(ATTENDANCE.atd_no_seq.nextval, :1, TO_DATE(:2, 'YYYY-MM-DD'), TO_DATE(:3, 'YYYY-MM-DD HH24:MI:SS'), :4, :5)
        '''

        cursor.executemany(query, attendance_data)
        conn.commit()

        print(f"ATD 테이블에 {len(attendance_data)}개 출석 데이터 삽입 완료 (6월 한 달간, 월~금만 기록, L은 3번)")

    except Exception as e:
        print("출석 데이터 삽입 오류 발생:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # 6월 출석 데이터 삽입
    insert_june_attendance()
