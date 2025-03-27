import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
import cx_Oracle as oci

# DB 접속 정보
sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'

class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.symbols = {}  # 날짜별 기호 저장
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.parent = parent  # 부모 윈도우 참조
        self.load_attendance_data()  # 출결 데이터 로드

    def load_attendance_data(self):
        """ DB에서 출석 데이터를 가져와 달력에 표시하고 출결 카운트 업데이트 """
        try:
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()

            query = '''
                SELECT ATD_DATE, STATUS, TO_CHAR(ATD_TIME, 'HH24:MI') 
                FROM ATTENDANCE.ATD 
                WHERE S_NO = 1 
                AND EXTRACT(MONTH FROM ATD_DATE) = 2
            '''
            cursor.execute(query)
            rows = cursor.fetchall()

            # 출석 상태를 달력 기호로 변환
            status_map = {'P': 'O', 'L': '△', 'A': 'X'}

            # 출석 현황 카운트 초기화
            count_data = {'P': 0, 'L': 0, 'A': 0}

            self.symbols.clear()  # 기존 데이터 초기화

            for date, status, time in rows:
                # 디버깅: DB에서 가져온 값 확인
                print(f"[DEBUG] DB에서 가져온 값: {date}, {status}, {time}")

                qdate = QDate(date.year, date.month, date.day)
                symbol = status_map.get(status, "")

                self.symbols[qdate] = (symbol, time)

                # 상태별 카운트 증가
                if status in count_data:
                    count_data[status] += 1
                    print(f"[DEBUG] 카운팅 중: {status} → {count_data[status]}")
                else:
                    print(f"[ERROR] 알 수 없는 상태: {status}")

            # 출석 현황 라벨 업데이트
            self.parent.update_attendance_labels(count_data)

        except Exception as e:
            print("데이터베이스 오류:", e)

        finally:
            cursor.close()
            conn.close()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        if date in self.symbols:
            symbol, time = self.symbols[date]
            color_map = {'O': "blue", '△': "green", 'X': "red"}

            # 기호 색상 설정
            painter.setPen(QColor(color_map.get(symbol, "black")))

            # 기호 표시 (날짜 오른쪽)
            font = QFont("Arial", 12, QFont.Bold)  # 크기 줄임
            painter.setFont(font)
            painter.drawText(rect.adjusted(rect.width() // 3, 0, 0, 0), Qt.AlignLeft, symbol)

            # 시간 표시 (날짜 아래쪽, 더 작게)
            painter.setFont(QFont("Arial", 6))  # 폰트 크기 작게 조정
            painter.drawText(rect.adjusted(0, rect.height() // 2, 0, 0), Qt.AlignCenter, time)


class AttendanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./미니프젝/출석관리,통계.ui', self)  # UI 파일 로드

        # 달력 위젯
        old_calendar = self.findChild(QCalendarWidget, "calendarWidget")
        if old_calendar:
            self.custom_calendar = CustomCalendar(self)
            self.custom_calendar.setGeometry(old_calendar.geometry())
            self.custom_calendar.setObjectName("calendarWidget")

            layout = old_calendar.parentWidget().layout()
            if layout:
                layout.replaceWidget(old_calendar, self.custom_calendar)
            old_calendar.deleteLater()

        # QLabel 위젯
        self.present_label = self.findChild(QLabel, "출석")  # QLabel 이름이 "출석"인지 확인
        self.late_label = self.findChild(QLabel, "지각")
        self.absent_label = self.findChild(QLabel, "결석")

        # QTableWidget 설정
        self.attendance_table = self.findChild(QTableWidget, "tableWidget_2")
        if self.attendance_table:
            self.initialize_table()

    def initialize_table(self):
        """테이블 초기화"""
        self.attendance_table.setHorizontalHeaderLabels(["상태", "개수"])
        self.attendance_table.setRowCount(3)
        self.attendance_table.setItem(0, 0, QTableWidgetItem("출석"))
        self.attendance_table.setItem(1, 0, QTableWidgetItem("지각"))
        self.attendance_table.setItem(2, 0, QTableWidgetItem("결석"))

    def update_attendance_labels(self, count_data):
        """출석, 지각, 결석 개수를 QLabel과 QTableWidget에 업데이트"""
        # QLabel 업데이트
        if self.present_label:
            self.present_label.setText(str(count_data.get('P', 0)))
        if self.late_label:
            self.late_label.setText(str(count_data.get('L', 0)))
        if self.absent_label:
            self.absent_label.setText(str(count_data.get('A', 0)))

        # QTableWidget 업데이트
        if self.attendance_table:
            self.attendance_table.setItem(0, 1, QTableWidgetItem(str(count_data.get('P', 0))))
            self.attendance_table.setItem(1, 1, QTableWidgetItem(str(count_data.get('L', 0))))
            self.attendance_table.setItem(2, 1, QTableWidgetItem(str(count_data.get('A', 0))))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())