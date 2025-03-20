import cx_Oracle as oci

# DB 연결 설정변수 선언
sid = 'XE'
host = '127.0.0.1' # localhoat와 동일
# DB서버가 외부에 있다면 -> 호스트가 포함된 도메인 주소나 ip를 넣어야됨
port = 1521
username = 'madang'
password = 'madang'

# DB 연결 시작
conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
cursor = conn.cursor() # DB 커서와 동일한 역할을 하는 개체

query = 'SELECT* FROM students' # 파이썬에서 쿼리호출 시에는 ; 쓰지 않기
cursor.execute(query)

# 불러온 데이터처리
for i, item in enumerate(cursor, start=1):
    print(item)

cursor.close()
conn.close()