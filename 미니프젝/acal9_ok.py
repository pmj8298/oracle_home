import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
import cx_Oracle as oci
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
import numpy as np

# 데이터베이스 연결 정보
sid = 'XE'
host = '127.0.0.1'
port = 1521
username = 'attendance'
password = '12345'

class AttendanceGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        font_path = "C:/Windows/Fonts/malgun.ttf"
        self.font_prop = self.set_korean_font(font_path)

    def set_korean_font(self, font_path):
        try:
            font = fm.FontProperties(fname=font_path)
            return font
        except Exception as e:
            print("폰트 로드 오류:", e)
            return None

    def update_hbar_graph(self, monthly_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        months = [f"{i}월" for i in range(1, 13)]
        attendance_rates = [0] * 12

        for month in range(1, 13):
            if month in monthly_data:
                data = monthly_data[month]
                total_o = data.get('O', 0)
                total_x = data.get('X', 0)
                total_triangles = data.get('△', 0)

                adjusted_x = total_x + (total_triangles // 3)
                total_attendance = total_o + adjusted_x + total_triangles

                if total_attendance > 0:
                    attendance_rates[month - 1] = (total_o / total_attendance) * 100

        y_pos = np.arange(len(months))
        colors = ['red' if rate < 80 else 'green' for rate in attendance_rates]

        ax.barh(y_pos, attendance_rates, color=colors, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(months, fontproperties=self.font_prop)
        ax.set_xlabel("출석 비율 (%)", fontproperties=self.font_prop)
        ax.set_xlim(0, 100)
        ax.set_title("월별 출석 비율", fontproperties=self.font_prop)

        self.canvas.draw()

class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.symbols = {}
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.parent = parent
        self.load_attendance_data()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        if date in self.symbols:
            symbol, time = self.symbols[date]
            color_map = {'O': "blue", '△': "green", 'X': "red"}

            painter.setPen(QColor(color_map.get(symbol, "black")))

            font = QFont("Arial", 12, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rect.adjusted(rect.width() // 3, 0, 0, 0), Qt.AlignLeft, symbol)

            if symbol != 'X':
                painter.setFont(QFont("Arial", 6))
                painter.drawText(rect.adjusted(0, rect.height() // 2, 0, 0), Qt.AlignCenter, time)

    def load_attendance_data(self):
        try:
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()
            query = '''
                SELECT ATD_DATE, STATUS, TO_CHAR(ATD_TIME, 'HH24:MI')
                FROM ATTENDANCE.ATD
                WHERE S_NO = 1
            '''
            cursor.execute(query)
            rows = cursor.fetchall()

            status_map = {'P': 'O', 'L': '△', 'A': 'X'}
            monthly_data = {}
            self.symbols.clear()

            for date, status, time in rows:
                qdate = QDate(date.year, date.month, date.day)
                month = date.month

                # 시간 비교를 통해 상태 결정
                hour, minute = map(int, time.split(':'))

                if hour < 9:
                    symbol = 'O'  # 오전 9시 이전
                elif 9<= hour < 13 :
                    symbol = '△'  # 오후 1시 이전
                else:
                    symbol = 'X'  # 오후 1시 이후

                self.symbols[qdate] = (symbol, time)

                if month not in monthly_data:
                    monthly_data[month] = {'O': 0, '△': 0, 'X': 0}
                monthly_data[month][symbol] += 1

            print("출결 데이터 로드 완료:", self.symbols)

            self.updateCells()
            self.parent.graph_widget.update_hbar_graph(monthly_data)

        except Exception as e:
            print("데이터베이스 오류:", e)

        finally:
            cursor.close()
            conn.close()

class AttendanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./미니프젝/출석관리,통계3.ui', self)

        self.graph_widget = AttendanceGraph(self)

        vertical_layout = self.findChild(QVBoxLayout, "verticalLayout")
        if vertical_layout:
            vertical_layout.addWidget(self.graph_widget)
            vertical_layout.addStretch(1)

        old_calendar = self.findChild(QCalendarWidget, "calendarWidget")
        if old_calendar:
            self.custom_calendar = CustomCalendar(self)
            self.custom_calendar.setGeometry(old_calendar.geometry())
            self.custom_calendar.setObjectName("calendarWidget")
            layout = old_calendar.parentWidget().layout()
            if layout:
                layout.replaceWidget(old_calendar, self.custom_calendar)
            old_calendar.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())
